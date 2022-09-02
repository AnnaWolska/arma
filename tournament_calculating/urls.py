from django.urls import path
from tournament_calculating.views import participants_list, participant_details, group_details, add_participant, delete_group_participant, draw_fights,\
    group_sort, tournament_calculate

app_name = "tournament_calculating"
urlpatterns = [
    path('participants/', participants_list, name="participants_list"),
    path('<int:tournament_id>/calculate/', tournament_calculate, name="tournament_calculate"),
    path('<int:tournament_id>/draw_fights/', draw_fights, name="draw_fights"),
    path('<int:group_id>/group/', group_details, name="group_details"),
    path('<int:group_id>/<int:tournament_id>/<int:participant_id>/delete_group_participant/', delete_group_participant, name="delete_group_participant"),
    path('<int:participant_id>/partcipant/', participant_details, name="participant_details"),
    path('<int:tournament_id>/group_sort/',group_sort, name="group_sort"),


    # path('<int:tournament_id>/add_participant', add_participant, name="add_participant"),
    #
    # path('add', add_tournament, name="add_tournament"),
    # path('<int:tournament_id>/delete_group_participant/<int:participant_id>/<int:group_id>', delete_group_participant, name="delete_group_participant"),
    # path('<int:tournament_id>/edit_tournament/', edit_tournament, name="edit_tournament"),
    #
    # path('<int:tournament_id>/add_post', add_post, name="add_post"),
    # path('<int:tournament_id>/edit_post/<int:post_id>', edit_post, name="edit_post"),
    # path('<int:tournament_id>/delete_post/<int:post_id>', delete_post, name="delete_post")
]