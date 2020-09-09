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

        logger.info(f'DHLListView:{ho}/{ids}')
        logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)
    
        return Response(serializer.data)        

class UPSListView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)     
    serializer_class = UPSSerializer

    def get(self, request, *args, **kwargs):
        ids = kwargs.get('ids', '')

        queryset = UPSParcel.objects.using('presta').raw(UPS_sql(kwargs.get('ids', '')))

        logger.info(f'UPSListView:{ids}')
        logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)
    
        return Response(serializer.data)                


class UPSAction(generics.ListAPIView):
    parser_class = (JSONParser,)
    serializer_class = UPSSerializer

    @swagger_auto_schema(operation_description="UPS description")
    def post(self, request, format=None):

        obj = request.data

        print(obj)

        queryset = UPSParcel.objects.using('presta').raw(UPS_sql(obj['id_order']))

        logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)

        resp = processItem(serializer.data[0])

        logger.error('####' + resp["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"])

        return Response({'status': 'OK','data':resp})

def processItem(dat):
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

    #response = requests.post(' https://onlinetools.ups.com/ship/v1807/shipments',data=json.dumps(dat),headers=newHeaders)
    response = requests.post(' https://wwwcie.ups.com/ship/v1807/shipments',data=json.dumps(dat),headers=newHeaders)

    print("Status code: ", response.status_code)

    with open(f"{path}{rn}.json", "w") as file:
        file.write(response.text)

    jsn = json.loads(response.text)


    logger.error(jsn)

    pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["NegotiatedRateCharges"])

    pprint.pprint(jsn["ShipmentResponse"]["ShipmentResults"]["ShipmentIdentificationNumber"])
    

    with open(f"{path}{rn}.gif", "wb") as file:
        file.write(base64.b64decode(jsn["ShipmentResponse"]["ShipmentResults"]["PackageResults"]["ShippingLabel"]["GraphicImage"]))    

    pdf = Image.open(f"{path}{rn}.gif")    
    pdf.save(f"{path}{rn}.pdf", "PDF" ,resolution=100.0, save_all=True)

    return jsn