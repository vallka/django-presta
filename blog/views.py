from django.views import generic

from .models import *


class ListView(generic.ListView):
    model = Post

"""     def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
 """

class PostView(generic.DetailView):
    model = Post


