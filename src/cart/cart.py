### -*- coding: utf-8 -*- ####################################################

import datetime

from .models import Cart as CartModel, Item

CART_PK = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart(object):
    
    def __init__(self, request):
        cart_id = request.session.get(CART_PK)
        if cart_id:
            try:
                cart = CartModel.objects.get(id=cart_id, checked_out=False)
            except CartModel.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):
        cart = CartModel.objects.create()
        request.session[CART_PK] = cart.pk
        return cart

    def add(self, content_type, object_pk, unit_price=0, quantity=1):
        return self.cart.item_set.create(content_type = content_type, 
                                   object_pk = object_pk, 
                                   unit_price = unit_price, 
                                   quantity = quantity)
        #raise ItemAlreadyExists

    def remove(self, item):
        """Removes a cart's item"""
        if item not in self.cart:
            raise ItemDoesNotExist
            
        item.delete()

    def update(self, item, price, quantity):
        """Changes an item's price and quantity"""
        if item not in self.cart:
            raise ItemDoesNotExist
        
        item.unit_price = price
        item.quantity = quantity
        item.save()

    def clear(self):
        """Clears the cart"""
        self.cart.item_set.all().delete()

    # There's all sort of info you might want to easily get from your cart
    
    def getQuantity(self, content_object):
        try: 
            item = Item.objects.get(cart = self.cart, content_object = content_object)
            return item.quantity
        except Item.DoesNotExist:
            raise ItemDoesNotExist
    
    def checkout_cart(self):
        self.cart.checked_out = True
        self.cart.save()
        return True
