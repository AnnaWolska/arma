from django.urls import path
from organizers.views import organizers_list, add_organizer, delete_organizer, organizer_details


app_name = "organizers"
urlpatterns = [
    path('', organizers_list, name="organizers_list"),
    path('<int:organizer_id>', organizer_details, name="organizer_details"),
    path('add', add_organizer, name="add_organizer"),
    path('<int:organizer_id>/delete_organizer', delete_organizer, name="delete_organizer"),
    # path('<int:tournament_id>/edit_tournament/', edit_tournament, name="edit_tournament"),

]