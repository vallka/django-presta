from django.urls import path

from .views import *

app_name = 'prestashop'

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product'),
    path('order/', OrderListView.as_view(), name='order'),
]
