from django.views.generic import ListView, DetailView

from .models import Post


class RollView(ListView):
    template_name = 'blog/roll.html'

    def get_queryset(self):
        return Post.objects.roll(self.request.user)


class PostDetailView(DetailView):
    def get_queryset(self):
        return Post.objects.all().relevant(self.request.user)
