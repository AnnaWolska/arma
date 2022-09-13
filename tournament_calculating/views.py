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
from django.db.models.aggregates import Count
from random import randint
import itertools
import random
from dataclasses import dataclass


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
#
# #

#
# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     number = group.number
#     rounds = 5
#     tournament = group.tournament
#     participants = group.participants.all()
#     fights = group.fights.all()
#     participants_names = []
#     for p in participants:
#         participants_names.append(p.name)
#     first_participant = participants[0]
#     after_replace = participants.order_by('-id')
#     last_participant = after_replace[0]
#     listed_participants = list(participants)
#     listed_names = []
#     a = []
#     result = []
#     x = list(chain.from_iterable(combinations(participants_names, r) for r in range(2, 2+1)))
#     for e in x:
#         if e not in a:
#             for f in x:
#                 if len(set(e).union(set(f))) == 2:
#                     result.append(e)
#     f_one = []
#     f_two = []
#     fight = {}
#     fights_list = []
#     for element in result:
#         f_one.append(element[0][0])
#         f_two.append(element[0][1])
#         fight = {
#         "first_fighter": Participant.objects.get(name=f_one),
#         "second_fighter": Participant.objects.get(name=f_two),
#         "tournament": tournament,
#         "group": group,
#         "rounds": rounds
#         }
#         fights_list.append(fight)
#     Fight.objects.bulk_create(fights_list)
#     print(fight)
#     print(f_two)
#     # fights.create(group=group, tournament=tournament, fighter_one=first_fighter, fighter_two=second_fighter)
#     return render(request, "group_sorted.html", context={
#         "number": number,
#         "tournament": tournament,
#         "group_id": group_id,
#         "participants": participants,
#         "first_participant": first_participant,
#         "last_participant": last_participant,
#         "result": result,
#         "listed_names":listed_names,
#         "listed_participants": listed_participants,
#         "participants_names": participants_names,
#         "fights": fights
#     })

# ostatnie z 28 nie obiektami
# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     number = group.number
#     rounds = 5
#     tournament = group.tournament
#     participants = group.participants.all()
#     fights = group.fights.all()
#     participants_names = []
#     for p in participants:
#         participants_names.append(p.name)
#     first_participant = participants[0]
#     # first_participant = Participant.objects.first()
#     after_replace = participants.order_by('-id')
#     last_participant = after_replace[0]
#     # last_participant = Participant.objects.last()
#     listed_participants = list(participants)
#     listed_names = []
#     a = []
#     result = []
#     x = list(chain.from_iterable(combinations(participants, r) for r in range(2, 2+1)))
#     for e in x:
#         if e not in a:
#             for f in x:
#                 if len(set(e).union(set(f))) == 2:
#                     result.append(e)
#     f_one = []
#     f_two = []
#     fight = {}
#     fights_list = []
#     for element in result:
#         f_one.append(element[0])
#         f_two.append(element[1])
#     #     fight = {
#     #     "first_fighter": Participant.objects.get(f_one),
#     #     "second_fighter": Participant.objects.get(f_two),
#     #     "tournament": tournament,
#     #     "group": group,
#     #     "rounds": rounds
#     #     }
#     #     fights_list.append(fight)
#     # Fight.objects.bulk_create(fights_list)
#     # print(fight)
#     # print(e)
#     # print(result)
#     # fights.create(group=group, tournament=tournament, fighter_one=first_fighter, fighter_two=second_fighter)
#     # print(e)
#     print(x)
#     # print(result[0][0])
#     return render(request, "group_sorted.html", context={
#         "number": number,
#         "tournament": tournament,
#         "group_id": group_id,
#         "participants": participants,
#         "first_participant": first_participant,
#         "last_participant": last_participant,
#         "result": result,
#         "listed_names":listed_names,
#         "listed_participants": listed_participants,
#         "participants_names": participants_names,
#         "fights": fights
#     })

# nowe


# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     number = group.number
#     tournament = group.tournament
#     participants = group.participants.all()
#     fights = group.fights.all()
#     rounds = 5
#     first_participant = Participant.objects.first()
#     last_participant = Participant.objects.last()
#     count = participants.count()
#     # print(count)
#     print(participants)
#     # print(participants[0])
#     # print(participants[-1])
#     first_random_fighter = participants[randint(0, count - 1)]
#     # print(first_random_fighter)
#     random_opponent = participants[randint(0, count -1)]
#     # print(random_opponent)
#     random_opponents = []
#     random_first_fighters = []
#     # for i in range(count):
#     for p in participants:
#         if first_random_fighter not in random_opponents:
#             if random_opponent not in random_first_fighters:
#                 if random_first_fighters not in random_first_fighters:
#                     if random_opponent not in random_opponents:
#                         if first_random_fighter != random_opponent:
#                             random_first_fighters.append(first_random_fighter)
#                             random_opponents.append(random_opponent)
#     # print(random_first_fighters)
#     # print(random_opponents)
#     return render(request, "group_sorted.html", context={
#         "number": number,
#         "tournament": tournament,
#         "group_id": group_id,
#         "participants": participants,
#         "first_participant": first_participant,
#         "last_participant": last_participant,
#         "fights": fights,
#         "first_random_fighter": first_random_fighter,
#         "random_first_fighters": random_first_fighters,
#         "random_opponent": random_opponent,
#         "random_opponents": random_opponents,
#     })

# najnowsze
def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    number = group.number
    tournament = group.tournament
    participants = group.participants.all()
    fights = group.fights.all()
    rounds = 5
    first_participant = Participant.objects.first()
    last_participant = Participant.objects.last()
    count = participants.count()
    # print(participants)
    first_random_fighter = participants[randint(0, count - 1)]
    random_opponent = participants[randint(0, count -1)]
    random_opponents = []
    random_first_fighters = []
    # for p in participants:
    #     if first_random_fighter not in random_opponents:
    #         if random_opponent not in random_first_fighters:
    #             if random_first_fighters not in random_first_fighters:
    #                 if random_opponent not in random_opponents:
    #                     if first_random_fighter != random_opponent:
    #                         random_first_fighters.append(first_random_fighter)
    #
    #                        random_opponents.append(random_opponent)
    participant_indexes = []
    # for e in participants:
    #     participant_indexes.append((e[i]))

    # print(list(itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8], 2)))
    print(itertools.combinations(participants, 2))
    cos = (itertools.combinations(participants, 2))
    # print(len(count))
    # print(range(count))
    return render(request, "group_sorted.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
        "first_participant": first_participant,
        "last_participant": last_participant,
        "fights": fights,
        "first_random_fighter": first_random_fighter,
        "random_first_fighters": random_first_fighters,
        "random_opponent": random_opponent,
        "random_opponents": random_opponents,
        "cos":cos
    })





#
# # próbuję łaczyć
# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     number = group.number
#     rounds = 5
#     tournament = group.tournament
#     participants = group.participants.all()
#     fights = group.fights.all()
#     participants_names = []
#     for p in participants:
#         participants_names.append(p.name)
#     first_participant = participants[0]
#     after_replace = participants.order_by('-id')
#     last_participant = after_replace[0]
#     listed_participants = list(participants)
#     listed_names = []
#     a = []
#     result = []
#     x = list(chain.from_iterable(combinations(participants, r) for r in range(2, 2+1)))
#     for e in x:
#         if e not in a:
#             for f in x:
#                 if len(set(e).union(set(f))) == 2:
#                     result.append(e)
#     print(x)
#     return render(request, "group_sorted.html", context={
#         "number": number,
#         "tournament": tournament,
#         "group_id": group_id,
#         "participants": participants,
#         "first_participant": first_participant,
#         "last_participant": last_participant,
#         "result": result,
#         "listed_names":listed_names,
#         "listed_participants": listed_participants,
#         "participants_names": participants_names,
#         "fights": fights
#     })



# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     fights = group.fights.all()
#     number = group.number
#     tournament = group.tournament
#     participants = group.participants.all()
#     first_participant = participants[0]
#     after_replace = participants.order_by('-id')
#     last_participant = after_replace[0]
#     result = zip(participants, after_replace)
#     return render(request, "group_sorted.html", context={
#         "number": number,
#         "tournament": tournament,
#         "group_id": group_id,
#         "participants": participants,
#         "first_participant": first_participant,
#         "last_participant": last_participant,
#         "result": result,
#     })


#
#     participants_names = []
#     for p in participants:
#         participants_names.append(p.name)
#     listed_participants = list(participants)
#     result = []
#     for index in participants:
#         if p not in after_replace:
#             for j in after_replace:
#                 if opponent not in participants:
#             # for index, element in enumerate(participants):
#             #     for opponent in participants[index + 1:]:
#                 # for j in after_replace:
#                 # for f in after_replace:
#                     # print(opponent)
#                     print(f'{p} - {opponent}')
#     fights.create(group=group, tournament=tournament)
#     for p in result:
#         print(p)
#     for index, country in enumerate(participants):
#         for opponent in countries[index + 1:]:
# "listed_names":listed_names,
# "listed_participants": listed_participants,
# "participants_names": participants_names,


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









