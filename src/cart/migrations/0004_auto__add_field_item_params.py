# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Item.params'
        db.add_column('cart_item', 'params', self.gf('cart.fields.DictionaryField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Item.params'
        db.delete_column('cart_item', 'params')


    models = {
        'cart.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cart.item': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('cart', 'content_type', 'object_pk'),)", 'object_name': 'Item'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['cart.Cart']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'params': ('cart.fields.DictionaryField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cart']
