from django.urls import path
from finals.views import finals

app_name = "finals"
urlpatterns = [
    path('<int:group_id>/finals/', finals, name="finals"),
    # path('<int:participant_id>/partcipant/', participant_details, name="participant_details"),
    # path('<int:group_id>/group/', group_details, name="group_details"),
    # path('<int:group_id>/<int:fight_id>/fight_details', fight_details, name="fight_details"),
    #
    # path('<int:group_id>/group_details/', draw_fights, name="draw_fights"),
    #
    # path('<int:group_id>/<int:tournament_id>/<int:participant_id>/delete_group_participant/', delete_group_participant,
    #      name="delete_group_participant"),
    # path('<int:group_id>/<int:tournament_id>/delete_group/', delete_group, name="delete_group"),
    # path('<int:group_id>/<int:tournament_id>/delete_fights/', delete_fights, name="delete_fights"),
    #
    # path('<int:group_id>/add_rounds/', add_rounds, name="add_rounds"),
    # path('<int:group_id>/<int:fight_id>/<int:round_id>/add_points/', add_points, name="add_points"),
    # path('<int:group_id>/', group_summary, name="group_summary"),
]