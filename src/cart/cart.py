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
        cart_pk = request.session.get(CART_PK)
        if cart_pk:
            try:
                cart = CartModel.objects.get(pk=cart_pk)
            except CartModel.DoesNotExist:
                self.new(request)
            
            if request.user.is_authenticated() and not cart.user:
                #Remove old cart
                oldcart = CartModel.objects.filter(user=request.user)
                if oldcart.exists():
                    oldcart.user = None
                    oldcart.save()
                
                cart.user = request.user
                cart.save()
                
        elif request.user.is_authenticated():
            try:
                cart = request.user.cart
            except CartModel.DoesNotExist:
                cart = request.user.cart.create()
        else:
            self.new(request)
        
        self.cart = cart
        

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item
    
    def new(self, request):
        cart = CartModel.objects.create()
        request.session[CART_PK] = cart.pk
        return cart
    
    def get_amount(self):
        return self.cart.get_amount()
    
    def get_count(self):
        return self.cart.item_set.count()
    
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
        self.cart.item_set.filter(active=True).delete()
