from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated 

from .models import *
from .views import *

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


class DHLListView(generics.ListAPIView):
    serializer_class = DHLSerializer

    def get(self, request, *args, **kwargs):
        ids = kwargs.get('ids', '')

        queryset = DHLParcel.objects.using('presta').raw(DHL_sql())

        logger.error('DHLListView')
        logger.error(queryset)

        serializer = self.get_serializer(queryset, many=True)
    
        return Response(serializer.data)        