from django.urls import path
# from tournament_calculating.views import
from tournament_calculating.views import tournament_calculate, participants_list, participant_details


app_name = "tournament_calculating"
urlpatterns = [
    path('participants', participants_list, name="participants_list"),
    path('<int:tournament_id>/calculate', tournament_calculate, name="tournament_calculate"),

    path('<int:participant_id>', participant_details, name="participant_details"),
    #
    # path('add', add_tournament, name="add_tournament"),
    # path('<int:tournament_id>/delete_tournament', delete_tournament, name="delete_tournament"),
    # path('<int:tournament_id>/edit_tournament/', edit_tournament, name="edit_tournament"),
    #
    # path('<int:tournament_id>/add_post', add_post, name="add_post"),
    # path('<int:tournament_id>/edit_post/<int:post_id>', edit_post, name="edit_post"),
    # path('<int:tournament_id>/delete_post/<int:post_id>', delete_post, name="delete_post")
]