from django.contrib import admin
from django.template.defaultfilters import filesizeformat

from models import DailyTraffic
from models import MonthlyTraffic
from models import HttpError
from models import LogMiningEvent


class DailyTrafficAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ['timestamp', 'hits', 'errors', 'bandwidth_fmt']

    def bandwidth_fmt(self, obj):
        return filesizeformat(obj.bandwidth)
    bandwidth_fmt.short_description = 'bandwidth'


class HttpErrorAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_seen'
    list_display = ['status', 'last_seen', 'hits', 'method', 'url_link', 'referer_link']
    list_filter = ['status', 'method', 'host']

    def url_link(self, obj):
        if obj.path:
            url = 'http://%s%s' % (obj.host, obj.path)
            return '<a href="%s">%s</a>' % (url, url)
        return obj.path
    url_link.allow_tags = True

    def referer_link(self, obj):
        if obj.referer:
            return '<a href="%s">%s</a>' % (obj.referer, obj.referer)
        return obj.referer
    referer_link.allow_tags = True


class LogMiningEventAdmin(admin.ModelAdmin):
    date_hierarchy = 'ran_at'
    list_display = ['ran_at', 'lines_read', 'start_timestamp', 'end_timestamp']


admin.site.register(DailyTraffic, DailyTrafficAdmin)
admin.site.register(MonthlyTraffic, DailyTrafficAdmin)
admin.site.register(HttpError, HttpErrorAdmin)
admin.site.register(LogMiningEvent, LogMiningEventAdmin)
