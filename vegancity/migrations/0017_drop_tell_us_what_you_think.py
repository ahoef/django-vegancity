# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        vendors = orm['vegancity.Vendor'].objects.all()
        messages = [u" This restaurant hasn't been reviewed yet-- let us know what you think!",
                    u" This restaurant hasn't been reviewed yet-- let us know what you think! ",
                    u" This restaurant hasn't been reviewed yet-- let us know what you think!  ",
                    u" This restaurant hasn't been reviewed yet-- let us know what you think!\r\n",
                    u" This restaurant has not been reviewed yet-- let us know what you think!",
                    u" This restaurant hasn\'t been reviewed yet -- let us know what you think!",
                    u" Aksum hasn't been reviewed yet--let us know what you think!",
                    u" B2 hasn't been reviewed yet-- let us know what you think!",
                    u" Benna's hasn't been reviewed yet-- let us know what you think!",
                    u" Cafe Lift hasn't been reviewed yet-- let us know what you think!",
                    u" Cake and the Beanstalk hasn't been reviewed yet-- let us know what you think!",
                    u" Cedar Point Bar & Kitchen hasn't been reviewed yet--let us know what you think!",
                    u" This vendor hasn't been reviewed yet-- let us know what you think!",
                    u" Chili Szechuan hasn't been reviewed yet--let us know what you think!",
                    u" This Chipotle location hasn't been reviewed yet-- let us know what you think!",
                    u" Citi Marketplace hasn't been reviewed yet-- let us know what you think!",
                    u" This resaurant hasn't been reviewed yet\u2014let us know what you think.",
                    u" Doobie's hasn't been reviewed yet-- let us know what you think!",
                    u" Ed's hasn't been reviewed yet-- let us know what you think!",
                    u" Essene hasn't been reviewed yet-- let us know what you think!\r\n\r\n   ",
                    u" Ethio Cafe hasn't been reviewed yet-- let us know what you think!",
                    u" Farmicia hasn't been reviewed yet-- let us know what you think!",
                    u" Fergie's Pub hasn't been reviewed yet-- let us know what you think!",
                    u" Franklin Fountain hasn't been reviewed yet-- let us know what you think!",
                    u" Govinda's hasn't been reviewed yet-- let us know what you think!",
                    u" Hibiscus hasn't been reviewed yet-- let us know what you think!",
                    u" Honey's hasn't been reviewed yet-- let us know what you think! ",
                    u" Hummus hasn't been reviewed yet-- let us know what you think!",
                    u" Jose's Tacos hasn't been reviewed yet--let us know what you think!",
                    u" Magic Carpet Foods hasn't been reviewed yet--let us know what you think!",
                    u" This place hasn't been reviewed yet-- let us know what you think!",
                    u" Northbowl hasn't been reviewed yet-- let us know what you think!",
                    u" This bakery hasn't been reviewed yet -- let us know what you think! ",
                    u" Pure Sweets hasn't been reviewed yet-- let us know what you think!",
                    u" Red Hook Coffee and Tea hasn't been reviewed yet--let us know what you think!\r\n",
                    u" Slice hasn't been reviewed yet-- let us know what you think!",
                    u" Slice hasn't been reviewed yet-- let us know what you think!",
                    u" Sweet Green hasn't been reviewed yet-- let us know what you think! ",
                    u" Watkins Drinkery hasn't been reviewed yet-- let us know what you think!  ",
                    u" Watkins Drinkery hasn't been reviewed yet-- let us know what you think!  ",
                    u" This restaurant hasn't been reviewed yet\u2014let us know what you think!",
                    u" This restaurant hasn't been reviewed yet\u2014let us know what you think! ",
                    u"A VegPhilly user hasn't visited here yet. Let us know what you think.",
        ]

        for message in messages:
            vendors_with_message = vendors.filter(notes__endswith=message)
            for vendor in vendors_with_message:
                trail_slice = len(message) * -1
                vendor.notes = vendor.notes[:trail_slice]
                vendor.save()

    def backwards(self, orm):
        pass

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'vegancity.cuisinetag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'CuisineTag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'})
        },
        u'vegancity.featuretag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'FeatureTag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'})
        },
        u'vegancity.neighborhood': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Neighborhood'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'vegancity.review': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Review'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'atmosphere_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'best_vegan_dish': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vegancity.VeganDish']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'food_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'suggested_cuisine_tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'suggested_feature_tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'unlisted_vegan_dish': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vegancity.Vendor']"})
        },
        u'vegancity.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karma_points': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mailing_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'vegancity.vegandish': {
            'Meta': {'ordering': "('name',)", 'object_name': 'VeganDish'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'})
        },
        u'vegancity.veglevel': {
            'Meta': {'object_name': 'VegLevel'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'super_category': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'vegancity.vendor': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Vendor'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approval_status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '100', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'cuisine_tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['vegancity.CuisineTag']", 'null': 'True', 'blank': 'True'}),
            'feature_tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['vegancity.FeatureTag']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'neighborhood': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vegancity.Neighborhood']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'veg_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vegancity.VegLevel']", 'null': 'True', 'blank': 'True'}),
            'vegan_dishes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['vegancity.VeganDish']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['vegancity']
    symmetrical = True
