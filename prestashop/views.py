from django.views import generic

# Create your views here.
from .models import *

class ProductListView(generic.ListView):
    model = Ps17Product

    def get_queryset(self):
        return Ps17Product.objects.all().using('presta').order_by('-id_product')[:50]

