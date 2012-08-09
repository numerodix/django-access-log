# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'HttpError.host'
        db.alter_column('access_log_httperror', 'host', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'HttpError.host'
        raise RuntimeError("Cannot reverse this migration. 'HttpError.host' and its values cannot be restored.")

    models = {
        'access_log.dailytraffic': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'DailyTraffic'},
            'bandwidth': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'errors': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'access_log.httperror': {
            'Meta': {'ordering': "['-last_seen']", 'unique_together': "(['status', 'method', 'host', 'path', 'referer'],)", 'object_name': 'HttpError'},
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'access_log.logminingevent': {
            'Meta': {'ordering': "['-ran_at']", 'object_name': 'LogMiningEvent'},
            'end_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines_read': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ran_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'start_timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'access_log.monthlytraffic': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'MonthlyTraffic'},
            'bandwidth': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'errors': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['access_log']