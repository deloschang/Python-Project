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
        ))
        db.send_create_signal('webapp', ['Experiences'])

        # Adding model 'Meme'
        db.create_table('webapp_meme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('webapp', ['Meme'])

        # Adding M2M table for field e on 'Meme'
        db.create_table('webapp_meme_e', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meme', models.ForeignKey(orm['webapp.meme'], null=False)),
            ('experiences', models.ForeignKey(orm['webapp.experiences'], null=False))
        ))
        db.create_unique('webapp_meme_e', ['meme_id', 'experiences_id'])


    def backwards(self, orm):
        # Deleting model 'Experiences'
        db.delete_table('webapp_experiences')

        # Deleting model 'Meme'
        db.delete_table('webapp_meme')

        # Removing M2M table for field e on 'Meme'
        db.delete_table('webapp_meme_e')


    models = {
        'webapp.experiences': {
            'Meta': {'object_name': 'Experiences'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'webapp.meme': {
            'Meta': {'object_name': 'Meme'},
            'e': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webapp.Experiences']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['webapp']