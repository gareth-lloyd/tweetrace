# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'TwitterUser.description'
        db.alter_column('linkwatcher_twitteruser', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'FundRaisingPageStats.fundraiser'
        db.alter_column('linkwatcher_fundraisingpagestats', 'fundraiser_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['justgivingbadges.FundRaiserProfile'], unique=True, null=True))

        # Adding unique constraint on 'FundRaisingPageStats', fields ['fundraiser']
        db.create_unique('linkwatcher_fundraisingpagestats', ['fundraiser_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FundRaisingPageStats', fields ['fundraiser']
        db.delete_unique('linkwatcher_fundraisingpagestats', ['fundraiser_id'])

        # Changing field 'TwitterUser.description'
        db.alter_column('linkwatcher_twitteruser', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'FundRaisingPageStats.fundraiser'
        db.alter_column('linkwatcher_fundraisingpagestats', 'fundraiser_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['justgivingbadges.FundRaiserProfile'], null=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'justgivingbadges.fundraiserprofile': {
            'Meta': {'object_name': 'FundRaiserProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'access_token_secret': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'jg_page_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'page_score': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'linkwatcher.fundraisingpagestats': {
            'Meta': {'object_name': 'FundRaisingPageStats'},
            'fundraiser': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['justgivingbadges.FundRaiserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_from_jg': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'})
        },
        'linkwatcher.mention': {
            'Meta': {'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_retweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_targeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['justgivingbadges.FundRaiserProfile']"}),
            'result_from_twitter': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tweeter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkwatcher.TwitterUser']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        'linkwatcher.twitteruser': {
            'Meta': {'object_name': 'TwitterUser'},
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'followers': ('django.db.models.fields.IntegerField', [], {}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['linkwatcher']
