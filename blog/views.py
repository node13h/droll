from django.views.generic import ListView

from .models import Post


class RollView(ListView):
    template_name = 'blog/roll.html'

    def get_queryset(self):
        return Post.objects.all()
