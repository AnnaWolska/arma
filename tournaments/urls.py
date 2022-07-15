from django.urls import path
from tournaments.views import tournaments_list, tournament_details, add_tournament, delete_tournament
from posts.views import add_post

app_name = "tournaments"
urlpatterns = [
    path('', tournaments_list, name="tournaments_list"),
    path('<int:tournament_id>', tournament_details, name="details"),
    path('add', add_tournament, name="add_tournament"),
    path('<int:tournament_id>/posts', add_post, name="add_posts")
    # path('delete', delete_tournament, name="delete_tournament")
]