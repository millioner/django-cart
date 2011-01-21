### -*- coding: utf-8 -*- ####################################################

from django.conf.urls.defaults import *

from .forms import ItemForm

urlpatterns = patterns('cart.views',

    url('^$', 'show_cart', {
        'template_name': 'cart/listing.html',
    }, name="show_cart"),
    
    url('^add/(?P<content_type_pk>[\d]+)/(?P<object_pk>[\d]+)/(?P<quantity>[\d]+)/$', 
        'add_to_cart', {}, name="add_to_cart"),
    
    url('^activate/(?P<item_pk>[\d]+)/$', 'switch_item', {
        'state': True,
    }, name="activate_item"),
    
    url('^disable/(?P<item_pk>[\d]+)/$', 'switch_item', {
        'state': False,
    }, name="disable_item"),
    
    url('^change_quantity/(?P<item_pk>[\w]+)/(?P<param_name>[\w]+)/$', 'change_quantity', {}, name='change_quantity'), 
    
    url('^remove/(?P<pk_param>[\d]+)/$', 'remove_item', {}, name="remove_item"),
    
    url(r'^clear/$', 'clear', name='clear_cart'),

)
