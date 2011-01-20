### -*- coding: utf-8 -*- ####################################################

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from native_tags.decorators import function

from cart.cart import Cart

@function
def add_to_cart_url(obj):
    ct_pk = ContentType.objects.get_for_model(obj).pk
    
    return reverse('add_to_cart', content_type_pk=ct_pk, object_pk=obj.pk)


def get_cart_count(request):
    return Cart(request).cart.item_set.count()

get_cart_count = function(get_cart_count, takes_request=1)
