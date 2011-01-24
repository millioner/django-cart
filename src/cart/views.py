### -*- coding: utf-8 -*- ####################################################

from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext
from django.contrib import messages
from django.views.generic.create_update import apply_extra_context
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import NON_FIELD_ERRORS

from .cart import Cart, ItemAlreadyExists
from .models import Item


def show_cart(request, template_name, extra_context=None):
    """Lists cart's items"""
    
    context = {'cart': Cart(request),}
    apply_extra_context(extra_context or {}, context)
    
    return direct_to_template(request, template=template_name, extra_context=context)

def add_to_cart(request, content_type_pk, object_pk, quantity,
                success_message=ugettext('Item was successfully added to the cart.'),
                redirect_to="show_cart"):
    """Append unique content object to card. """
    
    Cart(request).cart.item_set.create(content_type_id=content_type_pk, object_pk=object_pk, quantity=quantity)
    
    if request.is_ajax():
        return HttpResponse('true')
    else:
        messages.success(request, success_message)
        return redirect(redirect_to)


def cart__item_view(func):
    @wraps(func)
    def wrapper(request, item_pk, queryset=Item.objects.all(), 
                success_message=ugettext('Success.'),
                redirect_to="show_cart", **kwargs):
        cart = Cart(request).cart
        item = get_object_or_404(queryset.filter(cart=cart), pk=item_pk)
        
        func(item)
        
        if request.is_ajax():
            return HttpResponse('true')
        else:
            messages.success(request, success_message)
            return redirect(redirect_to)
    return wrapper

@cart__item_view
def restore_item(item):
    item.switch(True)

@cart__item_view
def disable_item(item):
    item.switch(False)


@cart__item_view
def remove_item(item):
    item.delete()
    

@require_POST
def change_quantity(request, pk_param, param_name, queryset=Item.objects.all(), redirect_to="show_cart"):
    
    item_pk = request.POST.get(pk_param)
    quantity = request.POST.get(param_name)
    
    
    cart = Cart(request).cart
    cart_item = get_object_or_404(queryset.filter(cart=cart), pk=item_pk)
    
    
    if quantity and cart_item.quantity != quantity:
        cart_item.quantity = quantity
        cart_item.save()
    
    if request.is_ajax():
        return HttpResponse(cart_item.get_amount())
    else:
        return redirect(redirect_to)


def clear(request, message=ugettext(u'The cart was cleared successfully.'), redirect_to="show_cart"):
    Cart(request).clear()

    messages.success(request, message)

    return redirect(redirect_to)


def get_amount(request):
    return HttpResponse(Cart(request).get_amount())

def get_count(request):
    return HttpResponse(Cart(request).get_count())
