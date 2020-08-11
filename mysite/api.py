from rest_framework import routers

from instadrome.api_views import MyUploadView
from dhl import api_views

router = routers.DefaultRouter()
#router.register(r'quotes', MyUploadView,basename='quotes')
router.register(r'dhl', api_views.DHLViewset)
