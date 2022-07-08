from django.urls import path
from tournaments.views import tournaments_list, tournament_details, add_tournament

app_name = "tournaments"
urlpatterns = [
    path('', tournaments_list, name="tournaments_list"),
    path('<int:tournament_id>', tournament_details, name="details"),
    path('add',add_tournament, name="add_tournamnet"),
]