from django.urls import path

from .views import HomeView, PostListView, PostDetailView


urlpatterns = [
    path("", HomeView.as_view(),name="home"),
    path("post-list/",PostListView.as_view(), name= "post-list"),
    path("post-detail/<int:pk>/",PostDetailView.as_view(), name= "post-detail"),
]