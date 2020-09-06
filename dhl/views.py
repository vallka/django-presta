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

class UPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = UPSParcel
        fields = '__all__'
