# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DailyTraffic'
        db.create_table('access_log_dailytraffic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('errors', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bandwidth', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('access_log', ['DailyTraffic'])

        # Adding model 'MonthlyTraffic'
        db.create_table('access_log_monthlytraffic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('errors', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bandwidth', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('access_log', ['MonthlyTraffic'])

        # Adding model 'HttpError'
        db.create_table('access_log_httperror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('referer', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('access_log', ['HttpError'])

        # Adding unique constraint on 'HttpError', fields ['status', 'method', 'path', 'referer']
        db.create_unique('access_log_httperror', ['status', 'method', 'path', 'referer'])

        # Adding model 'LogMiningEvent'
        db.create_table('access_log_logminingevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ran_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lines_read', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('start_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('access_log', ['LogMiningEvent'])

    def backwards(self, orm):
        # Removing unique constraint on 'HttpError', fields ['status', 'method', 'path', 'referer']
        db.delete_unique('access_log_httperror', ['status', 'method', 'path', 'referer'])

        # Deleting model 'DailyTraffic'
        db.delete_table('access_log_dailytraffic')

        # Deleting model 'MonthlyTraffic'
        db.delete_table('access_log_monthlytraffic')

        # Deleting model 'HttpError'
        db.delete_table('access_log_httperror')

        # Deleting model 'LogMiningEvent'
        db.delete_table('access_log_logminingevent')

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
            'Meta': {'ordering': "['-last_seen']", 'unique_together': "(['status', 'method', 'path', 'referer'],)", 'object_name': 'HttpError'},
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
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