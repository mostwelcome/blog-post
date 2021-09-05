from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartingPage.as_view(), name='starting-page'),
    path("posts", views.PostsList.as_view(), name='post-page'),
    path("posts/<slug>", views.PostDetails.as_view(), name='single-post')
]
