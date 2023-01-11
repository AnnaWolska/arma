import itertools
import random
import time
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.core.paginator import Paginator
from django.shortcuts import render
from tournaments.models import Tournament
from tournament_calculating.models import Group, Fight, Participant, Round
# from tournament_calculating.forms import (
#     AddParticipantForm,
#     AddGroupForm,
#     AddRoundsForm,
#     AddPointsForm,
#     GroupSummaryForm
#     )

def finals(request, group_id):

    group = Group.objects.get(pk=group_id)
    tournament = group.tournament
    participants = group.participants.all()
    # rounds_obj = group.rounds_of_group.all()
    # number = group.number
    # tournament = group.tournament
    # participants = group.participants.all().order_by("points_average")
    # fights = group.fights.all().order_by('id')
    # groups = Group.objects.filter(tournament=tournament).order_by("number")
    # first_fight = fights.first()
    temporary_list = []
    group_average_points = []
    finalists_list = []
    for participant in participants:
        group_average_points.append(participant.points_average)

    # for participant in tournament.participants.all():
        print("group_average_points", group_average_points)
    for participant in participants:
        while len(finalists_list) < group.number_outgoing:
            # print("(((((((((((((((())))))))))))))))")
            # print("group_average_points", group_average_points)
            # print("group.number_outgoing", group.number_outgoing)
            # print("len(finalists_list)",len(finalists_list))
            # print("len(finalists_list) < group.number_outgoing + 1", len(finalists_list) < group.number_outgoing + 1)
            if participant.points_average == max(group_average_points):
                print("participant.points_average == max(tournament_average_points) and participant not in finalists_list",participant.points_average == max(group_average_points) and participant not in finalists_list)
                finalists_list.append(participant)
                # time.sleep(1)
                print("finalists_list", finalists_list)
                group_average_points.remove(max(group_average_points))
                print("tournament_average_points po usunieciu",group_average_points)
            else:
                break
    print("finalists_list",finalists_list)






    return render(request, "final.html", context={
        # "number": number,
        # "tournament_id": tournament_id,
        # "group_id": group_id,
        # "participants": participants,
        # "fighters_one_names": fighters_one_names,
        # "fights_numbers": fights_numbers,
        # "fighters_two_names": fighters_two_names,
        # "rounds": rounds,
        # "fights": fights,
        # "rounds_obj": rounds_obj,
        # "groups": groups,
        # "tournaments_fighters_average": tournaments_fighters_average
    })