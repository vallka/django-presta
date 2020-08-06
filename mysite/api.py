from rest_framework import routers

from instadrome.api_views import MyUploadView

router = routers.DefaultRouter()
#router.register(r'quotes', MyUploadView,basename='quotes')