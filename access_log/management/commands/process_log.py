from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import LabelCommand
from django.db.models import F
from django.db.models import Sum
from django.utils.timezone import now
from optparse import make_option

from access_log.access_parser import iter_records

from access_log.models import DailyTraffic
from access_log.models import MonthlyTraffic
from access_log.models import HttpError
from access_log.models import LogMiningEvent


class Command(LabelCommand):
    args = "access.log"
    label = 'log file'
    option_list = LabelCommand.option_list + (
        make_option('--max_read_lines', dest='max_read_lines', default=50000,
                    help="Max read lines from access log file."),
    )

    def handle_label(self, logfile, **options):
        max_read_lines = int(options.get('max_read_lines'))

        # find the previous execution
        event = None
        try:
            event = LogMiningEvent.objects.all()[0]
        except IndexError: pass

        start_time, end_time = None, None


        days = {}
        lines_read = 0
        lines_skipped = 0

        for i, record in enumerate(iter_records(logfile)):
            if not start_time:
                start_time = record.timestamp
            if record.timestamp:
                end_time = record.timestamp

            # skip this record if we have seen it before
            if (event and event.end_timestamp
                and record.timestamp <= event.end_timestamp):
                print("Skipping record #%s for %s" % (intcomma(i+1), record.timestamp))
                lines_skipped += 1
                continue

            # break if the limit has been reached
            if lines_read >= max_read_lines:
                print("Reached limit of %s lines" % max_read_lines)
                break

            lines_read += 1
            print("Processing record #%s for %s" % (intcomma(i+1), record.timestamp))


            self.create_error_line(record)

            # gather data for daily traffic
            dt = self.floor_datetime(record.timestamp)

            if not dt in days:
                days[dt] = {
                    'timestamp': dt,
                    'hits': 0,
                    'errors': 0,
                    'bandwidth': 0,
                }

            days[dt]['hits'] += 1
            days[dt]['bandwidth'] += record.length
            if self.is_error(record):
                days[dt]['errors'] += 1

        # save daily traffic
        for dt, dct in days.items():
            daily_traffic, _ = DailyTraffic.objects.get_or_create(
                timestamp=dct['timestamp'],
            )
            DailyTraffic.objects.filter(pk=daily_traffic.pk).update(
                hits=F('hits') + dct['hits'],
                errors=F('errors') + dct['errors'],
                bandwidth=F('bandwidth') + dct['bandwidth'],
            )

        # update monthly traffic
        self.compute_monthly_traffic()

        # save event
        if lines_read > 0:
            LogMiningEvent(
                ran_at=now(),
                lines_read=lines_read,
                start_timestamp=start_time,
                end_timestamp=end_time,
            ).save()

        print("Processed %s, skipped %s records, between %s and %s" %
              (intcomma(lines_read), intcomma(lines_skipped), start_time, end_time))

    def compute_monthly_traffic(self):
        months = DailyTraffic.objects.dates('timestamp', 'month')
        for dt in months:
            d = DailyTraffic.objects.filter(timestamp__month=dt.month).aggregate(
                Sum('hits'), Sum('errors'), Sum('bandwidth'))
            dt = dt.replace(day=1, hour=0, minute=0, second=0)
            (mt, _) = MonthlyTraffic.objects.get_or_create(timestamp=dt)
            MonthlyTraffic.objects.filter(pk=mt.pk).update(
                hits=d['hits__sum'],
                errors=d['errors__sum'],
                bandwidth=d['bandwidth__sum'],
            )

    def create_error_line(self, record):
        if self.is_error(record):
            error_line, created = HttpError.objects.get_or_create(
                status=record.status,
                method=record.method,
                host=record.host and record.host[:255],
                path=record.path and record.path[:512],
                referer=record.referer and record.referer[:512],
            )
            if not created:
                HttpError.objects.filter(pk=error_line.pk).update(
                    last_seen=record.timestamp,
                    hits=F('hits') + 1,
                )

    def floor_datetime(self, dt):
        dt = dt.replace(hour=0, minute=0, second=0)
        return dt

    def is_error(self, record):
        return 400 <= record.status < 600
