from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema

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


class UPSAction(APIView):
    parser_class = (JSONParser,)

    @swagger_auto_schema(operation_description="UPS description")
    def post(self, request, format=None):

        obj = request.data

        print(obj)

        queryset = UPSParcel.objects.using('presta').raw(UPS_sql(obj['id_order']))

        logger.info(f'UPSListView:{obj['id_order']}')
        logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)


        return Response({'status': 'OK','data':serializer})
