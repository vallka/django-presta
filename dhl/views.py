from django.shortcuts import render
from django.views import generic
from rest_framework import serializers

from .models import DHLParcel,DHL_sql

# Create your views here.
class IndexView(generic.ListView):

    def get_queryset(self):
        """
        """
        return DHLParcel.objects.using('presta').raw(DHL_sql())

class DHLSerializer(serializers.ModelSerializer):
    class Meta:
        model = DHLParcel
        fields = '__all__'