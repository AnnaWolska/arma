import itertools
import random
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
from tournaments.models import Tournament
from tournament_calculating.models import Group, Fight, Participant
from tournament_calculating.forms import (
    AddParticipantForm,
    AddGroupForm,
    CalculateFightForm,
    AddFightsForm
    )


def participants_list(request):
    participants = Participant.objects.all().order_by('name')
    paginator = Paginator(participants, 20)
    page_number = request.GET.get('page')
    participants_register= paginator.get_page(page_number)
    context = {'participants_register': participants_register}
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
    participants_ids = []
    for p in participants:
        participants_ids.append(p.id)
    fights = group.fights.all()

    fighter_one_ids = []
    for f in fights:
        fighter_one_ids.append(f.fighter_one_id)

    fighter_two_ids = []
    for f in fights:
        fighter_two_ids.append((f.fighter_two_id))

    fighters_one_names = []
    for el in fighter_one_ids:
        fighters_one_names.append(participants.get(id=el))

    fighters_two_names = []
    for el in fighter_two_ids:
        fighters_two_names.append(participants.get(id=el))

    fights_numbers = []
    for i in range(1,len(fighters_one_names) + 1):
        fights_numbers.append(i)

    prtcp_to_show = []
    for p in participants:
        if p in fighters_one_names:
            prtcp_to_show.append(p)

    prtcp = []
    for element in fighters_one_names:
        prtcp.append(participants.filter(name=element.name))

    return render(request, "group_details.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
        "fighters_one_names": fighters_one_names,
        "fights_numbers": fights_numbers,
        "fighters_two_names": fighters_two_names,
        "prtcp": prtcp
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

            return HttpResponseRedirect(reverse(
                "tournament_calculating:group_details",
                args=[group_id])
                )
        else:
            form = AddParticipantForm
        return (
            render(request, "add_participant.html", context={
                'form': form,
                'tournament_id': tournament_id,
                'group_id': group_id,
            })
        )


def add_group(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)

    if request.user.is_authenticated:
        form = AddGroupForm(request.POST, instance=tournament)
        groups = tournament.groups.all()
        many_group_numbers = []
        for g in groups:
            many_group_numbers.append(g.number)
        if request.method == "POST" and form.is_valid():
            number = form.cleaned_data['number']
            if number not in many_group_numbers:
                obj = form.save(commit=False)
                obj.number = number
                obj.save()
                groups.create(number=number, tournament=tournament)
                messages.success(request, 'grupa dodana.')
                return HttpResponseRedirect(reverse(
                    "tournaments:tournament_details",
                    args=[tournament_id])
                )
            else:
                form = AddGroupForm
                return (
                    render(request, "add_group.html", context={
                        'form': form,
                        'tournament_id': tournament_id,
                    })
                )
        else:
            form = AddGroupForm
            return (
                render(request, "add_group.html", context={
                    'form': form,
                    'tournament_id': tournament_id,
                })
            )


def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    number = group.number
    tournament = group.tournament
    fights = Fight.objects.all()
    participants = group.participants.all()

    participants_names = []
    participants_ids = []
    if participants:
        for participant in participants:
            participants_names.append(participant.name)
        for participant in participants:
            participants_ids.append(participant.id)

    a = []
    result = []
    participants_pairs = list(itertools.chain.from_iterable(itertools.combinations(participants_ids, r) for r in range(2, 2 + 1)))

    participants_pairs_objects = []
    for pair in participants_pairs:
        participants_pairs_objects.append(Participant.objects.filter(pk__in=pair))

    name_to_show1 = []
    name_to_show2 = []
    left_participant = []
    right_participant = []
    for participant_pair in participants_pairs_objects:
        if participant_pair not in a:
            for f in participants_pairs_objects:
                if len(set(participant_pair).union(set(f))) == 2:
                    result.append(participant_pair)
                    left_participant.append(participant_pair[0])
                    right_participant.append(participant_pair[1])

    left_names = []
    right_names = []
    for l in left_participant:
        left_names.append(l.name)
    for r in right_participant:
        right_names.append(r.name)
    for r in result:
        name_to_show1.append(r[0])
        name_to_show2.append(r[1])

    result_to_show = []
    result_to_show.append(result[0])
    y = result_to_show[-1]
    n = 1
    while len(result_to_show) != len(result):
        if result_to_show[n - 1][0] != result[n][0] and result_to_show[n - 1][1] != result[n][1] and result[n] not in result_to_show:
            result_to_show.append(result[n])
            n += 1
        else:
            random.shuffle(result)

    print("result_to_show")
    for el in result_to_show:
        print(el)
    rounds = 0
    if participants:
        for r in result_to_show:
            print(r)
            print(r[0])
            print(r[1])
            fights.get_or_create(
                group=group,
                rounds=rounds,
                tournament=tournament,
                fighter_one=group.participants.get(id=r[0].id),
                fighter_two=group.participants.get(id=r[1].id)
            )

    fights_numbers = []
    for i in range(1,len(left_names) + 1):
        fights_numbers.append(i)

    fights_to_show = fights.filter(group_id=group_id)

    return render(request, "group_details.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
        "result": result,
        "participants_names": participants_names,
        "name_to_show1": name_to_show1,
        "name_to_show2": name_to_show2,
        "left_participant": left_participant,
        "right_participant": right_participant,
        "left_names": left_names,
        "right_names": right_names,
        "fights_numbers": fights_numbers,
        "fights": fights,
        "fights_to_show": fights_to_show,
    })


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
                return render(request, "delete_group_participant.html", context={
                 "tournament": tournament,
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
                return HttpResponseRedirect(reverse(
                    "tournaments:tournament_details",
                    args=[tournament_id])
                    )
        else:
            if user.is_authenticated:
                return render(request, "delete_group.html", context={
                 "tournament": tournament,
                 "group": group,
                 'tournament_id': tournament_id,
                 'group_id': group_id,
                 })


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


# def delete_fights(request, group_id):
#     user = request.user
#     tournament = Tournament.objects.get(pk=tournament_id)
#     group = Group.objects.get(pk=group_id)
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             tournament = Tournament.objects.get(pk=tournament_id)
#             group = Group.objects.get(pk=group_id)
#             if request.user == tournament.user:
#                 group.delete()
#                 return HttpResponseRedirect(reverse(
#                     "tournaments:tournament_details",
#                     args=[tournament_id])
#                     )
#         else:
#             if user.is_authenticated:
#                 return render(request, "delete_group.html", context={
#                  "tournament": tournament,
#                  "group": group,
#                  'tournament_id': tournament_id,
#                  'group_id': group_id,
#                  })

def delete_fights(request, tournament_id, group_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    fights = group.fights.all()
    print(fights)

    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            group = Group.objects.get(pk=group_id)
            # fights =.filter(pk=group_id)
            if request.user == tournament.user:
                    fights.delete()
                    # return HttpResponseRedirect(reverse("tournaments:tournament_details",
                    #                                     args=[tournament_id]))
                    return HttpResponseRedirect(reverse("tournament_calculating:group_details",
                                                        args=[group_id]))
        else:
            if user.is_authenticated:
                return render(request, "delete_fights.html", context={
                 "tournament": tournament,
                 "group": group,
                 "fights": fights,
                 'tournament_id': tournament_id,
                 'group_id': group_id,
                 })