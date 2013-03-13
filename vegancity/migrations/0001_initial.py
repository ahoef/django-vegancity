# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VegLevel'
        db.create_table('vegancity_veglevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('super_category', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('vegancity', ['VegLevel'])

        # Adding model 'Neighborhood'
        db.create_table('vegancity_neighborhood', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('vegancity', ['Neighborhood'])

        # Adding model 'UserProfile'
        db.create_table('vegancity_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('mailing_list', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('karma_points', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('vegancity', ['UserProfile'])

        # Adding model 'BlogEntry'
        db.create_table('vegancity_blogentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('vegancity', ['BlogEntry'])

        # Adding model 'VeganDish'
        db.create_table('vegancity_vegandish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vegancity.Vendor'])),
        ))
        db.send_create_signal('vegancity', ['VeganDish'])

        # Adding model 'Review'
        db.create_table('vegancity_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vegancity.Vendor'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('food_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('atmosphere_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('best_vegan_dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vegancity.VeganDish'], null=True, blank=True)),
            ('unlisted_vegan_dish', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('suggested_feature_tags', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('suggested_cuisine_tags', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('vegancity', ['Review'])

        # Adding model 'Vendor'
        db.create_table('vegancity_vendor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True)),
            ('neighborhood', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vegancity.Neighborhood'], null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('veg_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vegancity.VegLevel'], null=True, blank=True)),
        ))
        db.send_create_signal('vegancity', ['Vendor'])

        # Adding M2M table for field cuisine_tags on 'Vendor'
        db.create_table('vegancity_vendor_cuisine_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vendor', models.ForeignKey(orm['vegancity.vendor'], null=False)),
            ('cuisinetag', models.ForeignKey(orm['vegancity.cuisinetag'], null=False))
        ))
        db.create_unique('vegancity_vendor_cuisine_tags', ['vendor_id', 'cuisinetag_id'])

        # Adding M2M table for field feature_tags on 'Vendor'
        db.create_table('vegancity_vendor_feature_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vendor', models.ForeignKey(orm['vegancity.vendor'], null=False)),
            ('featuretag', models.ForeignKey(orm['vegancity.featuretag'], null=False))
        ))
        db.create_unique('vegancity_vendor_feature_tags', ['vendor_id', 'featuretag_id'])

        # Adding model 'CuisineTag'
        db.create_table('vegancity_cuisinetag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('vegancity', ['CuisineTag'])

        # Adding model 'FeatureTag'
        db.create_table('vegancity_featuretag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('vegancity', ['FeatureTag'])


    def backwards(self, orm):
        # Deleting model 'VegLevel'
        db.delete_table('vegancity_veglevel')

        # Deleting model 'Neighborhood'
        db.delete_table('vegancity_neighborhood')

        # Deleting model 'UserProfile'
        db.delete_table('vegancity_userprofile')

        # Deleting model 'BlogEntry'
        db.delete_table('vegancity_blogentry')

        # Deleting model 'VeganDish'
        db.delete_table('vegancity_vegandish')

        # Deleting model 'Review'
        db.delete_table('vegancity_review')

        # Deleting model 'Vendor'
        db.delete_table('vegancity_vendor')

        # Removing M2M table for field cuisine_tags on 'Vendor'
        db.delete_table('vegancity_vendor_cuisine_tags')

        # Removing M2M table for field feature_tags on 'Vendor'
        db.delete_table('vegancity_vendor_feature_tags')

        # Deleting model 'CuisineTag'
        db.delete_table('vegancity_cuisinetag')

        # Deleting model 'FeatureTag'
        db.delete_table('vegancity_featuretag')


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
        'vegancity.blogentry': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'BlogEntry'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'vegancity.cuisinetag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'CuisineTag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vegancity.featuretag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'FeatureTag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vegancity.neighborhood': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Neighborhood'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vegancity.review': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Review'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'atmosphere_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'best_vegan_dish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vegancity.VeganDish']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'food_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'suggested_cuisine_tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'suggested_feature_tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'unlisted_vegan_dish': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vegancity.Vendor']"})
        },
        'vegancity.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karma_points': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mailing_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'vegancity.vegandish': {
            'Meta': {'ordering': "('name',)", 'object_name': 'VeganDish'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vegancity.Vendor']"})
        },
        'vegancity.veglevel': {
            'Meta': {'object_name': 'VegLevel'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'super_category': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'vegancity.vendor': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Vendor'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'cuisine_tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['vegancity.CuisineTag']", 'null': 'True', 'blank': 'True'}),
            'feature_tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['vegancity.FeatureTag']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'neighborhood': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vegancity.Neighborhood']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'veg_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vegancity.VegLevel']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['vegancity']