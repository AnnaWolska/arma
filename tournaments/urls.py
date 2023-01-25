from django.urls import path
from tournaments.views import tournaments_list, tournament_details,\
    add_tournament, delete_tournament, edit_tournament
from posts.views import add_post, edit_post, delete_post

from tournament_calculating.views import add_participant, add_group, create_participant

app_name = "tournaments"
urlpatterns = [
    path('', tournaments_list, name="tournaments_list"),
    path('<int:tournament_id>/', tournament_details, name="tournament_details"),

    # path('<int:tournament_id>/add', add_tournament, name="add_tournament"),
    path('add', add_tournament, name="add_tournament"),
    path('<int:tournament_id>/delete_tournament', delete_tournament, name="delete_tournament"),
    path('<int:tournament_id>/edit_tournament/', edit_tournament, name="edit_tournament"),

    path('<int:tournament_id>/add_post', add_post, name="add_post"),
    path('<int:tournament_id>/edit_post/<int:post_id>', edit_post, name="edit_post"),
    path('<int:tournament_id>/delete_post/<int:post_id>', delete_post, name="delete_post"),

    path('create/', create_participant, name="create_participant"),
    path('<int:tournament_id>/add_participant/<int:group_id>/', add_participant, name="add_participant"),
    path('<int:tournament_id>/add_group/', add_group, name="add_group"),
]