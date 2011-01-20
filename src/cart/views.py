### -*- coding: utf-8 -*- ####################################################

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext
from django.contrib import messages
from django.views.generic.create_update import apply_extra_context
#from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import NON_FIELD_ERRORS

from .cart import Cart, ItemAlreadyExists
from .models import Item


def show_cart(request, template_name, extra_context=None):
    """Lists cart's items"""
    
    context = {'cart': Cart(request),}
    apply_extra_context(extra_context or {}, context)
    
    return direct_to_template(request, template=template_name, extra_context=context)

def add_to_cart(request, content_type_pk, object_pk, 
                success_message=ugettext('Item was successfully added to the cart.'),
                redirect_to="show_cart"):
    """Append unique content object to card. """
    
    Cart(request).cart.item_set.create(content_type_id = content_type_pk, object_pk = object_pk)
    
    messages.success(request, success_message)
    
    #messages.error(request, form.errors[NON_FIELD_ERRORS].as_text())

    return redirect(redirect_to)

def update_item(request, item_pk, form_class, queryset=Item.objects.all(), redirect_to="show_cart"):
    
    cart = Cart(request)
    item = get_object_or_404(queryset.filter(cart=cart), pk=item_pk)
    
    form = form_class(request.POST, instance=item)
    if form.is_valid():
        item = form.save()
    
        messages.success(request, ugettext('Successfully saved.'))

    return redirect(redirect_to)

def remove_item(request, item_pk, queryset=Item.objects.all(), 
                success_message=ugettext('Successfully deleted.'), 
                redirect_to="show_cart"):
    cart = Cart(request)
    cart_item = get_object_or_404(queryset.filter(cart=cart), pk=item_pk)
    cart_item.delete()

    messages.success(request, success_message)

    return redirect(redirect_to)


def clear(request, message=ugettext(u'The cart was cleared successfully.'), redirect_to="show_cart"):
    Cart(request).clear()

    messages.success(request, message)

    return redirect(redirect_to)
