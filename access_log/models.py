from django.db import models
from django.utils.timezone import now


class DailyTraffic(models.Model):
    timestamp = models.DateTimeField()
    hits = models.PositiveIntegerField(default=0)
    errors = models.PositiveIntegerField(default=0)
    bandwidth = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'daily traffic'


class MonthlyTraffic(models.Model):
    timestamp = models.DateTimeField()
    hits = models.PositiveIntegerField(default=0)
    errors = models.PositiveIntegerField(default=0)
    bandwidth = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'monthly traffic'


class HttpError(models.Model):
    last_seen = models.DateTimeField(default=now)
    hits = models.PositiveIntegerField(default=1)
    status = models.PositiveIntegerField()
    method = models.CharField(max_length=12)
    path = models.CharField(max_length=512)
    referer = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        unique_together = ['status', 'method', 'path', 'referer']
        ordering = ['-last_seen']


class LogMiningEvent(models.Model):
    ran_at = models.DateTimeField(default=now)
    lines_read = models.PositiveIntegerField()
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-ran_at']
