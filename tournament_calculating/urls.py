from django.urls import path
from tournament_calculating.views import participants_list, participant_details, group_details, add_participant, \
    delete_group_participant, draw_fights, \
    tournament_calculate, delete_group

app_name = "tournament_calculating"
urlpatterns = [
    path('participants/', participants_list, name="participants_list"),
    path('<int:participant_id>/partcipant/', participant_details, name="participant_details"),
    path('<int:group_id>/group/', group_details, name="group_details"),
    # path('<int:group_id>/group_sorted/', draw_fights, name="draw_fights"),
    path('<int:group_id>/group_details/', draw_fights, name="draw_fights"),
    path('<int:group_id>/<int:fight_id>/add_rounds/', tournament_calculate, name="tournament_calculate"),
    path('<int:group_id>/<int:tournament_id>/<int:participant_id>/delete_group_participant/', delete_group_participant,
         name="delete_group_participant"),
    path('<int:group_id>/<int:tournament_id>/delete_group/', delete_group, name="delete_group")
]
