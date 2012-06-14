# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CustomUser.language'
        db.delete_column('app_customuser', 'language')


        # Changing field 'Tweet.user'
        db.alter_column('app_tweet', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.CustomUser']))

    def backwards(self, orm):
        # Adding field 'CustomUser.language'
        db.add_column('app_customuser', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=10),
                      keep_default=False)


        # Changing field 'Tweet.user'
        db.alter_column('app_tweet', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_auth.UserSocialAuth']))

    models = {
        'app.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'activity_interval': ('django.db.models.fields.IntegerField', [], {'default': '2419200'}),
            'alwaysupdate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'configured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'half_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mail_interval': ('django.db.models.fields.IntegerField', [], {'default': '1209600'}),
            'neverupdate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'next_check': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nottodayupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publish_interval': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['social_auth.UserSocialAuth']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'wait_mail': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'app.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django_fields.fields.EncryptedCharField', [], {'unique': 'True', 'max_length': '293', 'cipher': "'AES'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.CustomUser']"})
        },
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
        'social_auth.usersocialauth': {
            'Meta': {'unique_together': "(('provider', 'uid'),)", 'object_name': 'UserSocialAuth'},
            'extra_data': ('social_auth.fields.JSONField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'social_auth'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['app']