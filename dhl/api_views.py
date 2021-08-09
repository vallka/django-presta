import json
import pprint
import requests
import base64
from PIL import Image

from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.db import connections

from .models import *
from .views import *

"""
class DHLViewset(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)     

    # needed here to avoid error
    queryset = DHLParcel.objects.using('presta').raw(DHL_sql())

    serializer_class = DHLSerializer

    def list(self, request, *args, **kwargs):
        # needed here to refresh results, otherwise it is cahced
        self.queryset = DHLParcel.objects.using('presta').raw(DHL_sql())

        # no clone() or all() methods...
        #self.queryset = self.queryset.clone()

        logger.error('DHLViewset list')
        logger.error(self.queryset)

        return super().list(self, request)
"""


class DHLListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)     
    serializer_class = DHLSerializer

    def get(self, request, *args, **kwargs):
        ids = kwargs.get('ids', '')
        ho = kwargs.get('ho', 'o')

        queryset = DHLParcel.objects.using('presta').raw(DHL_sql(kwargs.get('ho', 'o'),kwargs.get('ids', '')))

        #logger.info(f'DHLListView:{ho}/{ids}')
        #logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)
    
        return Response(serializer.data)        

class UPSListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)     
    serializer_class = UPSSerializer

    def get(self, request, *args, **kwargs):
        ids = kwargs.get('ids', '')

        queryset = UPSParcel.objects.using('presta').raw(UPS_sql(kwargs.get('ids', '')))

        #logger.info(f'UPSListView:{ids}')
        #logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)
    
        return Response(serializer.data)                


class UPSAction(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)     
    parser_class = (JSONParser,)
    serializer_class = UPSSerializer

    @swagger_auto_schema(operation_description="UPS description")
    def post(self, request, format=None):

        obj = request.data

        print(obj)

        queryset = UPSParcel.objects.using('presta').raw(UPS_sql(obj['id_order']))

        #logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)

        resp = processItem(serializer.data[0],obj['id_order'])

        #logger.error('####' + resp["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"])

        id_order = obj['id_order']
        shipping_no = resp["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"]

        with connections['presta'].cursor() as cursor:
            cursor.execute("UPDATE ps17_orders SET shipping_number=%s,current_state=31 WHERE id_order=%s", [shipping_no,id_order])
            cursor.execute("update ps17_order_carrier set tracking_number=%s where id_order=%s", [shipping_no,id_order])
            
            cursor.execute("insert into ps17_order_history (id_employee,id_order,id_order_state,date_add) values (%s,%s,%s,now())", [0,id_order,31])

        return Response({'status': 'OK','data':resp, 'headers':{'Access-Control-Allow-Origin':'*'}})

def processItem(dat,id_order):
    newHeaders = {
        'Content-type': 'application/json', 
        'Accept': 'application/json',
        'Username': 'info@gellifique.com',
        'Password': 'Dobroskokina1',
        'AccessLicenseNumber': 'BD878DD5B5667B91',
        'transId': 'Transaction001',
        'transactionSrc': 'test'
    }

    rn = dat['ShipmentRequest']['Shipment']['ReferenceNumber']['Value']
    path = settings.MEDIA_ROOT + '/UPS/'

    response = requests.post(' https://onlinetools.ups.com/ship/v1807/shipments',data=json.dumps(dat),headers=newHeaders)
    #response = requests.post(' https://wwwcie.ups.com/ship/v1807/shipments',data=json.dumps(dat),headers=newHeaders)

    #print("Status code: ", response.status_code)

    with open(f"{path}{id_order}.json", "w") as file:
        file.write(response.text)

    jsn = json.loads(response.text)


    #logger.error(jsn)

    #pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["NegotiatedRateCharges"]["TotalChargesWithTaxes"]["MonetaryValue"])

    #pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"])
    

    with open(f"{path}{id_order}.gif", "wb") as file:
        file.write(base64.b64decode(jsn["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]["GraphicImage"]))    

    pdf = Image.open(f"{path}{id_order}.gif")    
    pdf.save(f"{path}{id_order}.pdf", "PDF" ,resolution=100.0, save_all=True)

    return jsn

class UPSLabelAction(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)     
    parser_class = (JSONParser,)
    serializer_class = UPSLabelSerializer

    @swagger_auto_schema(operation_description="UPS description - label")
    def post(self, request, format=None):

        obj = request.data

        print(obj)

        queryset = ShippingNumber.objects.using('presta').raw(ShippingNumber_sql(obj['id_order']))

        #logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)

        resp = processLabelItem(serializer.data[0],obj['id_order'])

        #logger.error('####' + resp["LabelRecoveryResponse"]["LabelResults"]["ShipmentIdentificationNumber"])

        id_order = obj['id_order']
        shipping_no = resp["LabelRecoveryResponse"]["LabelResults"]["ShipmentIdentificationNumber"]

        return Response({'status': 'OK','data':resp, 'headers':{'Access-Control-Allow-Origin':'*'}})

def processLabelItem(dat,id_order):
    newHeaders = {
        'Content-type': 'application/json', 
        'Accept': 'application/json',
        'Username': 'info@gellifique.com',
        'Password': 'Dobroskokina1',
        'AccessLicenseNumber': 'BD878DD5B5667B91',
        'transId': 'Transaction001',
        'transactionSrc': 'test'
    }

    path = settings.MEDIA_ROOT + '/UPS/'

    response = requests.post(' https://onlinetools.ups.com/ship/v1/shipments/labels',data=json.dumps(dat),headers=newHeaders)

    print("Status code: ", response.status_code)

    with open(f"{path}{id_order}.json", "w") as file:
        file.write(response.text)

    jsn = json.loads(response.text)


    logger.error(jsn)

    #pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["NegotiatedRateCharges"]["TotalChargesWithTaxes"]["MonetaryValue"])

    #pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"])
    

    with open(f"{path}{id_order}.gif", "wb") as file:
        file.write(base64.b64decode(jsn["LabelRecoveryResponse"]["LabelResults"]["LabelImage"]["GraphicImage"]))    

    pdf = Image.open(f"{path}{id_order}.gif")    
    pdf.save(f"{path}{id_order}.pdf", "PDF" ,resolution=100.0, save_all=True)

    return jsn
