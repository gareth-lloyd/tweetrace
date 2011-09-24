# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TwitterUser'
        db.create_table('linkwatcher_twitteruser', (
            ('uid', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('profile_picture', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('followers', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('linkwatcher', ['TwitterUser'])

        # Adding model 'Mention'
        db.create_table('linkwatcher_mention', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tweeter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkwatcher.TwitterUser'])),
            ('is_targeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_retweet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('result_from_twitter', self.gf('picklefield.fields.PickledObjectField')(null=True, blank=True)),
        ))
        db.send_create_signal('linkwatcher', ['Mention'])

        # Adding model 'FundRaisingPageStats'
        db.create_table('linkwatcher_fundraisingpagestats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('result_from_jg', self.gf('picklefield.fields.PickledObjectField')(null=True, blank=True)),
        ))
        db.send_create_signal('linkwatcher', ['FundRaisingPageStats'])


    def backwards(self, orm):
        
        # Deleting model 'TwitterUser'
        db.delete_table('linkwatcher_twitteruser')

        # Deleting model 'Mention'
        db.delete_table('linkwatcher_mention')

        # Deleting model 'FundRaisingPageStats'
        db.delete_table('linkwatcher_fundraisingpagestats')


    models = {
        'linkwatcher.fundraisingpagestats': {
            'Meta': {'object_name': 'FundRaisingPageStats'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'result_from_jg': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'})
        },
        'linkwatcher.mention': {
            'Meta': {'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_retweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_targeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'result_from_twitter': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tweeter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkwatcher.TwitterUser']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        'linkwatcher.twitteruser': {
            'Meta': {'object_name': 'TwitterUser'},
            'followers': ('django.db.models.fields.IntegerField', [], {}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['linkwatcher']
