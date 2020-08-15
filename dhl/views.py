from django.shortcuts import render
from django.views import generic
from rest_framework import serializers

import logging
logger = logging.getLogger(__name__)

from .models import DHLParcel,DHL_sql

# Create your views here.
class IndexView(generic.ListView):

    def get_queryset(self):
        """
        """
        qs = DHLParcel.objects.using('presta').raw(DHL_sql('o',''))
        logger.error('get_queryset')
        logger.error(qs)
        return qs

class DHLSerializer(serializers.ModelSerializer):
    class Meta:
        model = DHLParcel
        fields = '__all__'
        """
        fields = [
            'name_ship_from',
            'company_ship_from',
            'address_1_ship_from',
            'address_2_ship_from',
            'address_3_ship_from',
            'house_number_ship_from',
            'postal_code_ship_from',
            'city_ship_from',
            'country_code_ship_from',
            'email_address_ship_from',
            'phone_country_code_ship_from',
            'phone_number_ship_from',
            'name_ship_to',
            'company_ship_to',
            'address_1_ship_to',
            'address_2_ship_to',
            'address_3_ship_to',
            'house_number_ship_to',
            'postal_code_ship_to',
            'city_ship_to',
            'state_code_ship_to',
            'country_code_ship_to',
            'email_address_ship_to',
            'phone_country_code_ship_to',
            'phone_number_ship_to',
            'account_number_shipper',
            'total_weight',
            'declared_value_currency',
            'declared_value',
            'product_code_3_letter',
            'summary_of_contents',
            'shipment_type',
            'shipment_reference',
            'total_shipment_pieces',
            'invoice_type',
            'length',
            'width',
            'depth',
        ]
        """

