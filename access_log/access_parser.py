#!/usr/bin/env python

import re
import sys

import dateutil.parser
import dateutil.tz

### Apache Combined Log Format
# 173.208.43.20 - - [28/Apr/2012:07:24:52 -0400] "GET /numerodix/blog/index.php/2007/05/19/painless-website-backup-synchronization/ HTTP/1.1" 200 28576 "" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)"
rx_logline = re.compile(
    r'^'
    '([^\s]+)'  # ip
    '\s+'
    '([^\s]+)'  # ident / -
    '\s+'
    '([^\s]+)'  # REMOTE_USER / -
    '\s+'
    '[[](.*?)[]]'  # timestamp
    '\s+'
    '"(.*?)"'  # request string
    '\s+'
    '([^\s]+)'  # status
    '\s+'
    '([^\s]+)'  # length
    '\s+'
    '"(.*?)"'  # referer
    '\s+'
    '"(.*?)"'  # user agent
    '$'
)

# [28/Apr/2012:07:24:52 -0400]
rx_apache_timestamp = re.compile(
    r'^'
    '([0-9]+)'  # day
    '[/]'
    '([A-Za-z]+)'  # month
    '[/]'
    '([0-9]+)'  # year
    '[:]'
    '([0-9]+)'  # hour
    '[:]'
    '([0-9]+)'  # minute
    '[:]'
    '([0-9]+)'  # second
    '\s+'
    '([^\s]+)'  # timezone
    '$'
)

# "GET /numerodix/blog/index.php/2007/05/19/painless-website-backup-synchronization/ HTTP/1.1"
rx_apache_request_string = re.compile(
    r'(?i)^'
    '([^\s]+)'  # method
    '\s+'
    '(.+)'  # path
    '\s+'
    '(HTTP\/[0-9].[0-9])'  # http version
    '$'
)

UTC_ZONE = dateutil.tz.gettz('UTC')


class LogRecord(object):
    _atts = [
        'ip', 'ident', 'remote_user', 'timestamp',
        'method', 'path', 'version', 'status', 'length',
        'referer', 'user_agent'
    ]
    def __init__(self, **kwargs):
        for att in self._atts:
            setattr(self, att, None)

        for k, v in kwargs.items():
            if k not in self._atts:
                raise Exception("Unknown key: %s" % k)
            setattr(self, k, v)

    def __str__(self):
        dct = {}
        for att in self._atts:
            dct[att] = getattr(self, att, None)
        return str(dct)

def get_datetime(apache_timestamp):
    day, month, year, hour, minute, second, tz =\
            rx_apache_timestamp.findall(apache_timestamp)[0]
    fmt = '%s %s %s %s:%s:%s %s' % (month, day, year, hour, minute, second, tz)
    dt = dateutil.parser.parse(fmt)
    dt = dt.astimezone(UTC_ZONE)
    return dt

def parse_request_string(request_string):
    method, path, version = rx_apache_request_string.findall(request_string)[0]
    return method, path, version

def iter_records(filepath):
    for line in open(filepath):
        line = line.strip()

        ip, ident, remote_user, timestamp, request,\
                status, length, referer, user_agent = rx_logline.findall(line)[0]

        ident = ident != '-' and ident or None
        remote_user = remote_user != '-' and remote_user or None
        timestamp = get_datetime(timestamp)
        method, path, version = parse_request_string(request)
        status = status and int(status)
        length = length != '-' and int(length) or 0
        referer = referer != '-' and referer or None
        user_agent = user_agent or None

        record = LogRecord(
            ip=ip,
            ident=ident,
            remote_user=remote_user,
            timestamp=timestamp,
            method=method,
            path=path,
            version=version,
            status=status,
            length=length,
            referer=referer,
            user_agent=user_agent,
        )
        yield record

def main(filepath):
    for record in iter_records(filepath):
        print('%s' % record)


if __name__ == '__main__':
    main(sys.argv[1])
