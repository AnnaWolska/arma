from django.urls import path
from .views import show_galleries_list, show_gallery_details, add_gallery, add_photo, delete_gallery

app_name = "galleries"
urlpatterns = [
    path('',show_galleries_list, name="galleries_list"),
    path('<int:gallery_id>', show_gallery_details, name="gallery_details"),
    path('add', add_gallery, name="add_gallery"),
    path('<int:gallery_id>/add_photo', add_photo, name="add_photo"),
path('<int:gallery_id>/delete_gallery', delete_gallery, name="delete_gallery"),
    ]

