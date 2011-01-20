### -*- coding: utf-8 -*- ####################################################

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'), default=datetime.now)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    
    user = models.OneToOneField('auth.user', blank=True, null=True)
    
    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'content_object' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['content_object']))
            kwargs['object_id'] = kwargs['content_object'].pk
            del(kwargs['content_object'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    unit_price = models.DecimalField(_('unit price'), max_digits=18, decimal_places=2, blank=True, null=True)
    
    active = models.BooleanField(_("active"), default=True)
    
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_pk')

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        order_with_respect_to = 'cart'
        unique_together = ('cart', 'content_type', 'object_pk')

    def __unicode__(self):
        return 'Content: %s, cart: %s' % (self.content_object, self.cart)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)
