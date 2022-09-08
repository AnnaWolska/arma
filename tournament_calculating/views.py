from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournament_calculating.models import Group, Fight, Round, Participant
from tournaments.models import Tournament
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournament_calculating.forms import AddParticipantForm, SortGroupForm, AddGroupForm, DrawFightsForm, CalculateFightForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tournaments.views import tournament_details
import random
# import itertools
from itertools import *


def participants_list(request):
    participants = Participant.objects.all().order_by('name')
    paginator = Paginator(participants, 20)
    page_number = request.GET.get('page')
    participants_list = paginator.get_page(page_number)
    context = {'participants_list': participants_list}
    return render(request, "participants_list.html", context)


def participant_details(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    name = participant.name
    school = participant.school
    image = participant.image
    groups = participant.groups.all()
    tournaments = participant.tournaments.all()
    return render(request, "participant_details.html", context={
        "name": name,
        "school": school,
        "image": image,
        "participant_id": participant_id,
        "tournaments": tournaments,
        "groups": groups
    })


def group_details(request, group_id):
    group = Group.objects.get(pk=group_id)
    number = group.number
    tournament = group.tournament
    participants = group.participants.all()
    return render(request, "group_detials.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
    })


def add_participant(request, tournament_id, group_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddParticipantForm(request.POST, request.FILES)
            group = Group.objects.get(pk=group_id)

            if form.is_valid():
                instance = form.save()
                instance.groups.add(group)
                instance.tournaments.add(tournament)
                instance.save()

            return HttpResponseRedirect(reverse("tournament_calculating:group_details", args=[group_id]))
        else:
            form = AddParticipantForm
        return (
            render(request, "add_participant.html", context={
                'form':form,
                'tournament_id':tournament_id,
                'group_id':group_id,
            })
        )


def add_group(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if request.user.is_authenticated:
        form = AddGroupForm(request.POST, instance=tournament)
        groups = tournament.groups.all()
        if request.method == "POST" and form.is_valid():
            number = form.cleaned_data['number']
            for group in groups:
                if number != group.number:
                    obj = form.save(commit=False)
                    obj.number = number
                    obj.save()
                    groups.create(number=number, tournament=tournament)
                    return HttpResponseRedirect(reverse("tournaments:tournament_details", args=[tournament_id]))
        else:
            form = AddGroupForm
            return (
                render(request, "add_group.html", context={
                    'form': form,
                    'tournament_id': tournament_id,
                })
            )


def delete_group_participant(request, tournament_id, group_id, participant_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    participant = Participant.objects.get(pk=participant_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            group = Group.objects.get(pk=group_id)
            participant = Participant.objects.get(pk=participant_id)
            if request.user == tournament.user:
                if participant in group.participants.all():
                    group.participants.remove(participant)
                    return HttpResponseRedirect(reverse("tournaments:tournament_details",
                                                        args=[tournament_id]))
        else:
            if user.is_authenticated:
                return render(request, "delete_group_participant.html", context=
                {"tournament": tournament,
                 "group": group,
                 "participant": participant,
                 'tournament_id': tournament_id,
                 'group_id': group_id,
                 'participant_id': participant_id
                 })


def delete_group(request, tournament_id, group_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            group = Group.objects.get(pk=group_id)
            if request.user == tournament.user:
                group.delete()
                return HttpResponseRedirect(reverse("tournaments:tournament_details", args=[tournament_id]))
        else:
            if user.is_authenticated:
                return render(request, "delete_group.html", context=
                {"tournament": tournament,
                 "group": group,
                 'tournament_id': tournament_id,
                 'group_id': group_id,
                 })


def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    number = group.number
    tournament = group.tournament
    participants = group.participants.all()
    participants_names = []
    for p in participants:
        participants_names.append(p.name)
    first_participant = participants[0]
    after_replace = participants.order_by('-id')
    last_participant = after_replace[0]
    listed_participants = list(participants)
    listed_names = []

    a = []
    result = []
    x = list(chain.from_iterable(combinations(participants_names, r) for r in range(2, 2+1)))
    for e in x:
        if e not in a:
            for f in x:
                if len(set(e).union(set(f))) == 2:
                    result.append(e)
    # fights = group.fights.all()
    # fights.create(group=group, tournament=tournament, fighter_one=first_participant, fighter_two=last_participant)
    return render(request, "group_sorted.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
        "first_participant": first_participant,
        "last_participant": last_participant,
        "result": result,
        "listed_names":listed_names,
        "listed_participants": listed_participants,
        "participants_names": participants_names,

    })


def group_sort(request, tournament_id):
    # tournament = Tournament.objects.get(pk=tournament_id)
    # participants = tournament.participants.all()
    # if request.user.is_authenticated:
    #     if request.method == "POST":
    #         form = SortGroupForm(request.POST)
    #         groups = tournament.groups.all()
    #         if form.is_valid():
    #             for participant in participants:
    #                 for group in participant.groups.all():
    #                     participant.add.random.choice(group)
    #                     form.save()
    #                     return HttpResponseRedirect(reverse("tournaments:tournament_details",
    #                                                         args=[tournament_id]))
    #     else:
    #         form = SortGroupForm()
    #         if request.user.is_authenticated:
    #             return render(request, "tournament_details.html", context=
    #             {
    #              'tournament_id': tournament_id,
    #              'tournament': tournament,
    #              'participants': participants,
    #              'form': form,
    #              })
    pass


def tournament_calculate(request, group_id, fight_id):
    group = Group.objects.get(pk=group_id)
    number = group.number
    tournament = group.tournament
    fight = Fight.objects.get(pk=fight_id)
    participants = group.participants.all()
    participants_names = []
    fights = group.fights.all()
    for p in participants:
        participants_names.append(p.name)
    first_participant = participants[0]
    after_replace = participants.order_by('-id')
    last_participant = after_replace[0]
    listed_participants = list(participants)
    if request.user.is_authenticated:
        form = CalculateFightForm(request.POST, instance=fight)
        if request.method == "POST":
            if form.is_valid():
                obj = form.save(commit=False)
                obj.group = group
                obj.fighter_one.name = first_participant
                obj.fighter_two.name = last_participant
                obj.save()
                fights.create(group=group, tournament=tournament)
                return HttpResponseRedirect(reverse("tournament_calculation.html", args=[group_id]))
        else:
            form = CalculateFightForm
            return (
                render(request, "add_rounds.html", context={
                    'form': form,
                    "number": number,
                    "tournament": tournament,
                    "group_id": group_id,
                    "fight_id": fight_id,
                    "participants": participants,
                    "first_participant": first_participant,
                    "last_participant": last_participant,
                    "listed_participants": listed_participants,
                    "participants_names": participants_names,
                })
            )









