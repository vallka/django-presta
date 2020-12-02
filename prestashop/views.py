from django.views import generic
from rest_framework import serializers

# Create your views here.
from .models import *

import logging
logger = logging.getLogger(__name__)

class ProductListView(generic.ListView):
    model = Ps17Product

    def get_queryset(self):
        return Ps17Product.objects.all().using('presta').order_by('-id_product')[:50]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ps17Product
        fields = '__all__'

class OrderListView(generic.ListView):

    def get_queryset(self):
        """
        """
        sql = Order.SQL()
        logger.error(f'get_queryset sql:{sql}')
        qs = Order.objects.using('presta').raw(sql)
        logger.error(qs)
        return qs

class OrderSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id_order' : instance.id_order,
            'reference' : instance.reference,
            'id_order_state' : instance.id_order_state,
            'order_state' : instance.order_state,
            'shipping_number' : instance.shipping_number,
            'firstname_customer' : instance.firstname_customer,
            'lastname_customer' : instance.lastname_customer,
            'note' : instance.note,
            'firstname' : instance.firstname,
            'lastname' : instance.lastname,
            'email' : instance.email,
            'postcode' : instance.postcode,
            'address1' : instance.address1,
            'address2' : instance.address2,
            'city' : instance.city,
            'phone' : instance.phone,
            'country' : instance.country,
            'currency_code' : instance.currency_code,
            'total_paid' : instance.total_paid,
            'total_products_wt' : instance.total_products_wt,
            'total_shipping_tax_incl' : instance.total_shipping_tax_incl,
            'date_add' : instance.date_add,
            'date_upd' : instance.date_upd,
            'id_country' : instance.id_country,
            'carrier' : instance.carrier,
            'is_new' : instance.is_new,
        }