### -*- coding: utf-8 -*- ####################################################

from django.conf.urls.defaults import *

from .forms import ItemForm

urlpatterns = patterns('cart.views',

    url('^$', 'show_cart', {
        'template_name': 'cart/listing.html',
    }, name="show_cart"),
    
    url('^add/(?P<content_type_pk>[\d]+)/(?P<object_pk>[\d]+)/$', 'add_to_cart', {}, name="add_to_cart"),
    
    url('^remove/(?P<item_pk>[\d]+)/$', 'remove', {
        'form_class': ItemForm,
    }, name="remove_item"),
    
    url(r'^clear/$', 'clear', name='clear_cart'),

)
