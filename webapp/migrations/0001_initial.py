# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Experiences'
        db.create_table('webapp_experiences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('album_pic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Meme'], null=True, blank=True)),
        ))
        db.send_create_signal('webapp', ['Experiences'])

        # Adding M2M table for field creator on 'Experiences'
        db.create_table('webapp_experiences_creator', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiences', models.ForeignKey(orm['webapp.experiences'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('webapp_experiences_creator', ['experiences_id', 'user_id'])

        # Adding model 'Meme'
        db.create_table('webapp_meme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('source_content', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('top_caption', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
            ('bottom_caption', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
        ))
        db.send_create_signal('webapp', ['Meme'])

        # Adding M2M table for field e on 'Meme'
        db.create_table('webapp_meme_e', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meme', models.ForeignKey(orm['webapp.meme'], null=False)),
            ('experiences', models.ForeignKey(orm['webapp.experiences'], null=False))
        ))
        db.create_unique('webapp_meme_e', ['meme_id', 'experiences_id'])

        # Adding model 'MemeLibrary'
        db.create_table('webapp_memelibrary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('thumb', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('top_caption', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
            ('bottom_caption', self.gf('django.db.models.fields.CharField')(max_length=180, blank=True)),
        ))
        db.send_create_signal('webapp', ['MemeLibrary'])


    def backwards(self, orm):
        # Deleting model 'Experiences'
        db.delete_table('webapp_experiences')

        # Removing M2M table for field creator on 'Experiences'
        db.delete_table('webapp_experiences_creator')

        # Deleting model 'Meme'
        db.delete_table('webapp_meme')

        # Removing M2M table for field e on 'Meme'
        db.delete_table('webapp_meme_e')

        # Deleting model 'MemeLibrary'
        db.delete_table('webapp_memelibrary')


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
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'webapp.experiences': {
            'Meta': {'object_name': 'Experiences'},
            'album_pic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webapp.Meme']", 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'webapp.meme': {
            'Meta': {'object_name': 'Meme'},
            'bottom_caption': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'e': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webapp.Experiences']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'source_content': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'top_caption': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        },
        'webapp.memelibrary': {
            'Meta': {'object_name': 'MemeLibrary'},
            'bottom_caption': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'thumb': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'top_caption': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        }
    }

    complete_apps = ['webapp']