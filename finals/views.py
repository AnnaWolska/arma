import itertools
import random
import time
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.core.paginator import Paginator
from django.shortcuts import render
from tournaments.models import Tournament
from finals.models import Finalist
from tournament_calculating.models import Group, Fight, Participant, Round
# from tournament_calculating.forms import (
#     AddParticipantForm,
#     AddGroupForm,
#     AddRoundsForm,
#     AddPointsForm,
#     GroupSummaryForm
#     )

def finals(request, group_id):
    prtcp_ls = []
    group = Group.objects.get(pk=group_id)
    tournament = group.tournament
    participants = group.participants.all()
    finalists = Finalist.objects.filter(group = group)
    # for f in finalists:
    # for p in participants:
    #     prtcp_ls.append( Finalist.objects.get(participant_id=p.id))
    # finalists = prtcp_ls
    # print(prtcp_ls)
    for p in participants:
        for f in finalists:
            if p.id == f.participant_id:
                prtcp_ls.append(p)


    return render(request, "final.html", context={
        "finalists": finalists,
        "prtcp_ls": prtcp_ls
    })