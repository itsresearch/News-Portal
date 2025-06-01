from django.shortcuts import render

# Create your views here.

from newspaper.models import Post
from django.views.generic import ListView


class HomeView(ListView):
    model = Post
    template_name = "newsportal/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull = False, status = "active"
    ).order_by("published_at")[:4]