from rest_framework import viewsets
from .models import *
from .views import *

class DHLViewset(viewsets.ModelViewSet):
    queryset = DHLParcel.objects.using('presta').raw(DHL_sql())
    serializer_class = DHLSerializer
