from django.urls import path
from organizers.views import organizers_list, add_organizer


app_name = "organizers"
urlpatterns = [
    path('', organizers_list, name="organizers_list"),
    path('add', add_organizer, name="add_organizer"),
    # path('<int:tournament_id>/delete_tournament', delete_tournament, name="delete_tournament"),
    # path('<int:tournament_id>/edit_tournament/', edit_tournament, name="edit_tournament"),

]