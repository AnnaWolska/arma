from django.urls import path
from tournaments.views import tournaments_list, tournament_details, add_tournament, delete_tournament
from posts.views import add_post, edit_post, delete_post

app_name = "tournaments"
urlpatterns = [
    path('', tournaments_list, name="tournaments_list"),
    path('<int:tournament_id>', tournament_details, name="tournament_details"),
    path('add', add_tournament, name="add_tournament"),
    path('<int:tournament_id>/add_post', add_post, name="add_post"),
    path('<int:tournament_id>/edit_post/<int:post_id>', edit_post, name="edit_post"),
    path('<int:tournament_id>/delete_post/<int:post_id>', delete_post, name="delete_post"),
    path('<int:tournament_id>/delete_tournament', delete_tournament, name="delete_tournament")
    # path('delete', delete_tournament, name="delete_tournament")
]