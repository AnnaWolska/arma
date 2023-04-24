from django.urls import path
from .views import post_details

app_name = "posts"
urlpatterns = [
    path('<int:post_id>', post_details, name="post_details"),
    ]
