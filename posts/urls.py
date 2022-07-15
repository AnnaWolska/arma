from django.urls import path
from .views import posts_list, post_details, add_post, edit_post

app_name = "posts"
urlpatterns = [
    # path('<int:tournament_id>/posts_list', name="posts_list"),
    path('<int:post_id>', post_details, name="post_details"),
    path('add_post',add_post, name="add_post"),
    path('<int:post_id>/edit_post', edit_post, name="edit_post"),
    ]
