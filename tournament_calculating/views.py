from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournament_calculating.models import Group, Fight, Round, Participant
from tournaments.models import Tournament
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournament_calculating.forms import AddParticipantForm, SortGroupForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from tournaments.views import tournament_details
import random


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


def delete_group(request, tournament_id, group_id ):
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


def draw_fights(request, tournament_id, group_id, participant_id):
    # [(x, y) for x in range(1, 5)
    #       for y in range(4, 0, -1)]
    # [(1, 4), (1, 3), (1, 2), (1, 1), (2, 4), (2, 3), (2, 2), (2, 1), (3, 4), (3, 3), (3, 2), (3, 1), (4, 4), (4, 3),
    #  (4, 2), (4, 1)]
    # sorted(range(len(a)), key=a.__getitem__)
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    participant = Participant.objects.get(pk=participant_id)
    for participant1 in range(1,len(group.participants.all())):
        for participant2 in range(len(group.participants.all())-1,0,-1):
            print(participant1,participant2)


def group_sort(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    participants = tournament.participants.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SortGroupForm(request.POST)
            groups = tournament.groups.all()
            if form.is_valid():
                for participant in participants:
                    for group in participant.groups.all():
                        participant.add.random.choice(group)
                        form.save()
                        return HttpResponseRedirect(reverse("tournaments:tournament_details",
                                                            args=[tournament_id]))
        else:
            form = SortGroupForm()
            if request.user.is_authenticated:
                return render(request, "tournament_details.html", context=
                {
                 'tournament_id': tournament_id,
                 'tournament': tournament,
                 'participants': participants,
                 'form': form,
                 })

def tournament_calculate(request):
    pass