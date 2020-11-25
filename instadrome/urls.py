from django.urls import path

from .views import *

app_name = 'instadrome'

urlpatterns = [
    path('img/', ig_image, name='img'),
]
