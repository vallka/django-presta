import json
import pprint
import requests
import base64
import re

from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.db import connections

from .models import *
from .views import *

import logging
logger = logging.getLogger(__name__)

db = 'presta'

class ProductList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)     
    serializer_class = ProductSerializer

    @swagger_auto_schema(operation_description="Products by id (comma separated)")
    def get(self, request, *args, **kwargs):
        ids = kwargs.get('ids', '')

        queryset = Ps17Product.objects.using(db).filter(id_product__in=kwargs.get('ids', '').split(','))

        logger.info(f'ProductList:{ids}')
        #logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)
    
        return Response(serializer.data)                

class UpdateProduct(APIView):
    permission_classes = (IsAuthenticated,)     
    parser_class = (JSONParser,)

    @swagger_auto_schema(operation_description="Update product",)
    def post(self, request, format=None):

        obj = request.data
        logger.info(f"UpdateProduct:{obj['ids']} | {obj['what']} | {obj['search']} | {obj['replace']}")

        n = 0
        n_updated = 0
        if obj['ids'] and obj['what'] and obj['search']:
            ids = obj['ids'].split(',')

            if obj['what']=='reference':
                queryset = Ps17Product.objects.using(db).filter(id_product__in=ids)
                l = len(queryset)
                logger.info(f'found:{l}')
                for p in queryset:
                    n += 1
                    new_reference = re.sub(obj['search'],obj['replace'],p.reference)
                    logger.info(f"{n} {p.id_product}: {p.reference}=>{new_reference}")
                    if p.reference!=new_reference:
                        p.reference=new_reference
                        p.save()
                        n_updated += 1
                        logger.info(f'saved:{p.id_product}')

        logger.error(f'done:{n}')

        return Response({'success':1,'req':obj, 'count':n, 'updated':n_updated})                
