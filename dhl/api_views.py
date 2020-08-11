from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 

from .models import *
from .views import *

class DHLViewset(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)     

    queryset = DHLParcel.objects.using('presta').raw(DHL_sql())
    serializer_class = DHLSerializer

    def list(self, request):
        super().list(self, request)