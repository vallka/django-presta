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

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
