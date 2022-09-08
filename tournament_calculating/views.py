from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournament_calculating.models import Group, Fight, Round, Participant
from tournaments.models import Tournament
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournament_calculating.forms import AddParticipantForm, SortGroupForm, AddGroupForm, DrawFightsForm
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


    # obj = MyModel.objects.get(...)
    # return redirect(obj)
# Category.objects.get(id=1)
# def draw_fights(request, tournament_id, group_id):
#     tournament = Tournament.objects.get(pk=tournament_id)
#     group = Group.objects.get(pk=group_id)
#     participants = group.participants.all()
#     first_participant = participants.get(id=31)
#     user = request.user
#     if request.user.is_authenticated:
#             tournament = Tournament.objects.get(pk=tournament_id)
#             group = Group.objects.get(pk=group_id)
#             if user == tournament.user:
#                 print(first_participant.name)
#                 return redirect(tournament_details, first_participant.name)

                # return HttpResponseRedirect(reverse('tournaments:group_sorted', args=[tournament_id]))


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

    my_li = []
    # for first_player, opponent in itertools.combinations(participants_names, 2):
    #     cos = f'{first_player} - {opponent}'
    a = []
    result = []
    x = list(chain.from_iterable(combinations(participants_names, r) for r in range(2, 2+1)))
    # x = list(chain.from_iterable(combinations(participants_names, r) for r in range))
    for e in x:
        if e not in a:
            for f in x:
                if len(set(e).union(set(f))) == 2:
                    result.append(e)
                    # result = result
                    # random_result = []
                    # for i in range(len((result)):
                        # random_result
                    # random.choice(result)
                    # result = random.choice
                    # sorted(result)
                    # a.append(e)
                    # a.append(f)
    # {f'{ff} - {opponent}'}
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
        "my_li":my_li
    })

        # def powerset(iterable, n):
        #     a = []
        #     w = []
        #     x = list(chain.from_iterable(combinations(iterable, r) for r in range(n, n + 1)))
        #     for e in x:
        #         if e not in a:
        #             for f in x:
        #                 if len(set(e).union(set(f))) == 2 * n:
        #                     w.append([e, f])
        #                     a.append(e)
        #                     a.append(f)
        #     return w

        # my_li.append(f'{ff} - {opponent}')
    # for index, ff in enumerate(participants_names):
    #     for opponent in participants_names[index + 1:]:
    #
    #         result = {f'{ff} - {opponent}'}
    #     for i in range(len(result)):
    #         my_li.append(result)
# for i in range(len(Rainbow)):
#     print(Rainbow[i])
    # for prtcp in listed_participants:
    #     listed_names.append(prtcp)
    # for x in range(len(participants)):
    #     for y in range(len(participants) - 1, 0, -1):
    #         result = [(x,y)]
    # for index, first_fighter in enumerate(participants):

# for index, country in enumerate(countries):
#     for opponent in countries[index + 1:]:
#         print(f'{country} - {opponent}')
# def draw_fights(request, tournament_id, group_id, participant_id):

#     # [(x, y) for x in range(1, 5)
#     #       for y in range(4, 0, -1)]
#     # [(1, 4), (1, 3), (1, 2), (1, 1), (2, 4), (2, 3), (2, 2), (2, 1), (3, 4), (3, 3), (3, 2), (3, 1), (4, 4), (4, 3),
#     #  (4, 2), (4, 1)]
#     # sorted(range(len(a)), key=a.__getitem__)

#     tournament = Tournament.objects.get(pk=tournament_id)
#     group = Group.objects.get(pk=group_id)
#     participant = Participant.objects.get(pk=participant_id)
#     for participant1 in range(1,len(group.participants.all())):
#         for participant2 in range(len(group.participants.all())-1,0,-1):
#             print(participant1,participant2)
#


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


# def tournament_calculate(request, tournament_id):
def tournament_calculate(request, group_id):
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
    # return render(request, "tournament_calculation.html", context={
    #     "number": number,
    #     "tournament": tournament,
    #     "group_id": group_id,
    #     "participants": participants,
    #     "first_participant": first_participant,
    #     "last_participant": last_participant,
    #     # "result": result,
    #     # "listed_names":listed_names,
    #     "listed_participants": listed_participants,
    #     "participants_names": participants_names,
    #     # "my_li":my_li
    # })
    if request.user.is_authenticated:
        form = CalculateFightForm(request.POST, instance=tournament)
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








    # tournament = Tournament.objects.get(pk=tournament_id)
    # if request.user.is_authenticated:
    #     if request.method == "POST":
    #         form = SortGroupForm(request.POST)
    #         # groups = tournament.groups.all()
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
    # pass



