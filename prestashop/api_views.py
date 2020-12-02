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

class OrderList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)     
    serializer_class = OrderSerializer

    @swagger_auto_schema(operation_description="Orders")
    def get(self, request, *args, **kwargs):

        sql = Order.SQL()
        logger.error(f'get sql:{sql}')
        qs = Order.objects.using(db).raw(sql)
        logger.error(len(qs))
        serializer = self.get_serializer(qs, many=True)
    
        return Response(serializer.data)                

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

            if obj['what'][0:4]=='name':
                id_lang = int(obj['what'][5:])
                logger.info(f'id_lang:{id_lang}')
                queryset = Ps17ProductLang.objects.using(db).filter(id_product__in=ids,id_lang=id_lang,)
                l = len(queryset)
                logger.info(f'found:{l}')
                for p in queryset:
                    n += 1
                    new_name = re.sub(obj['search'],obj['replace'],p.name)
                    logger.info(f"{n} {p.id_product}: {p.name}=>{new_name}")
                    if p.name!=new_name:
                        p.name=new_name
                        
                        #p.save()
                        # DOSN'T WORK AS ps_product_lang uses composite pk!

                        logger.info("update ps17_product_lang set name=%s where id_product=%s and id_lang=%s and is_shop=%s")
                        logger.info(f"pars:{new_name},{p.id_product},{p.id_lang},{p.id_shop}")


                        with connections[db].cursor() as cursor:
                            cursor.execute("update ps17_product_lang set name=%s where id_product=%s and id_lang=%s and id_shop=%s",
                                [new_name,p.id_product,p.id_lang,p.id_shop])

                        n_updated += 1
                        logger.info(f'saved:{p.id_product},{p.id_lang},{p.id_shop}')

            if obj['what']=='price':
                queryset = Ps17Product.objects.using(db).filter(id_product__in=ids,)
                l = len(queryset)
                logger.info(f'found:{l}')
                for p in queryset:
                    n += 1
                    new_price = obj['replace']
                    logger.info(f"{n} {p.id_product}: {p.price}=>{new_price}")
                    if p.price!=new_price:

                        logger.info("update ps17_product_shop set price=%s where id_product=%s and id_shop=%s")
                        logger.info(f"pars:{new_price},{p.id_product},1")


                        with connections[db].cursor() as cursor:
                            cursor.execute("update ps17_product_shop set price=%s where id_product=%s and id_shop=%s",[new_price,p.id_product,1])
                            cursor.execute("update ps17_product set price=%s where id_product=%s",[new_price,p.id_product])

                        n_updated += 1
                        logger.info(f'saved:{p.id_product}')

        logger.error(f'done:{n}/{n_updated}')

        return Response({'success':1,'req':obj, 'count':n, 'updated':n_updated})                

    
