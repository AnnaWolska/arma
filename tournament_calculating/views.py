import itertools
import random
import math
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
from tournaments.models import Tournament
from tournament_calculating.models import Group, Fight, Participant, Round
from tournament_calculating.forms import (
    AddParticipantForm,
    AddGroupForm,
    AddRoundsForm,
    AddPointsForm
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
    rounds_obj = group.rounds_of_group.all()
    number = group.number
    tournament = group.tournament
    participants = group.participants.all()
    fights = group.fights.all().order_by('id')
    groups = Group.objects.filter(tournament=tournament)
    first_fight = fights.first()
    rounds = 0
    if first_fight:
        rounds = first_fight.rounds

    fighter_one_ids = []
    for f in fights:
        fighter_one_ids.append(f.fighter_one_id)
    fighter_two_ids = []
    for f in fights:
        fighter_two_ids.append(f.fighter_two_id)
    fighters_one_names = []
    for el in fighter_one_ids:
        fighters_one_names.append(participants.get(id=el))
    fighters_two_names = []
    for el in fighter_two_ids:
        fighters_two_names.append(participants.get(id=el))

    fights_numbers = []
    for i in range(1,len(fighters_one_names) + 1):
        fights_numbers.append(i)

    return render(request, "group_details.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
        "fighters_one_names": fighters_one_names,
        "fights_numbers": fights_numbers,
        "fighters_two_names": fighters_two_names,
        "rounds": rounds,
        "fights": fights,
        "rounds_obj": rounds_obj,
        "groups":groups
    })


def fight_details(request, group_id, fight_id):

    group = Group.objects.get(pk=group_id)
    fight = Fight.objects.get(pk=fight_id)
    rounds_obj = group.rounds_of_group.all()
    number = group.number
    tournament = group.tournament
    grups = Group.objects.all(tournament=tournament)
    participants = group.participants.all()
    participants_ids = []
    for p in participants:
        participants_ids.append(p.id)
    fights = group.fights.all()
    first_fight = fights.first()
    ff = fights.filter(pk=group_id)
    rounds = 0
    iter_rounds = []
    for i in range(rounds):
        iter_rounds.append(i)
    if first_fight:
        rounds = first_fight.rounds

    fighter_one_ids = []
    for f in fights:
        fighter_one_ids.append(f.fighter_one_id)
    fighter_two_ids = []
    for f in fights:
        fighter_two_ids.append(f.fighter_two_id)

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
        "prtcp": prtcp,
        "rounds": rounds,
        "fights": fights,
        "fight_id":fight_id,
        "fight": fight,
        "rounds_obj": rounds_obj,
        "grups": grups
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
            if request.method == "POST" and form.is_valid():
                number = form.cleaned_data['number']
                # if groups:
                if number not in many_group_numbers:
                    obj = form.save(commit=False)
                    obj.number = number
                    obj.save()
                    groups.create(number=number, tournament=tournament)
                    messages.success(request, 'grupa dodana.')
                    return HttpResponseRedirect(reverse(
                        "tournaments:tournament_details",
                        args=[tournament_id]))

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


def sorting(some_list):
    length = len(some_list)
    sorting_result = []
    if length > 2:
        if length > 6:
            sorting_result.append(some_list[0])
            some_list.remove(some_list[0])
            while len(sorting_result) != length:
                condition_one = sorting_result[-1][0] != some_list[0][0] and sorting_result[-1][0] != some_list[0][1]
                condition_two = sorting_result[-1][1] != some_list[0][1]and sorting_result[-1][1] != some_list[0][0]
                if condition_one and condition_two:
                    sorting_result.append(some_list[0])
                    some_list.remove(some_list[0])
                else:
                    some_list.append(some_list[0])
                    some_list.remove(some_list[0])
        else:
            random.shuffle(some_list)
            sorting_result = some_list
        return sorting_result

#TODO: żeby kasowała rundy dla walki
def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    tournament = group.tournament
    fights = Fight.objects.all().order_by('id')
    participants_pairs = list(itertools.chain.from_iterable(itertools.combinations(group.participants.all(), r)
                                                            for r in range(2, 2 + 1)))
    left_participants = []
    right_participants = []
    result = []

    for participant_pair in participants_pairs:
        result.append(participant_pair)
        left_participants.append(participant_pair[0])
        right_participants.append(participant_pair[1])
    #TODO: zrobić tak, by kasował wcześniejsze wylosowane walki po ponownym losowaniu
    order_number = 1
    result_to_show = sorting(result)
    if participants_pairs:

        for right_participant in result_to_show:
            fights.get_or_create(
                order=order_number,
                group=group,
                tournament=tournament,
                fighter_one=right_participant[0],
                fighter_two=right_participant[1]
            )
            order_number +=1
    return HttpResponseRedirect(reverse("tournament_calculating:group_details",
                                        args=[group_id]))


def delete_group_participant(request, tournament_id, group_id, participant_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    fights = group.fights.all()
    participant = Participant.objects.get(pk=participant_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            group = Group.objects.get(pk=group_id)
            participant = Participant.objects.get(pk=participant_id)
            if request.user == tournament.user:
                if participant in group.participants.all():
                    group.participants.remove(participant)
                    fights.delete()
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


def delete_fights(request, tournament_id, group_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    participants = group.participants.all()
    fights = group.fights.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            group = Group.objects.get(pk=group_id)
            if request.user == tournament.user:
                fights.delete()
                # for participant in participants:
                #     participant.group_points = 0
                #     participant.update()

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


def add_rounds(request, group_id):
    group = Group.objects.get(pk=group_id)
    participants = Participant.objects.filter(groups=group_id)
    if request.user.is_authenticated:
        form = AddRoundsForm(request.POST, instance=group)
        fights = group.fights.all()
        rounds_of_group = group.rounds_of_group.all()
        if request.method == "POST" and form.is_valid():
            rounds = form.cleaned_data['rounds']
            obj = form.save(commit=False)
            obj.rounds = rounds
            obj.save()
            for p in participants:
                obj = Round(fighter_id=p.id)
            for fight in fights:
                obj = Round(fight_id=fight.id)
                for round in range(1, rounds + 1):
                    obj = Round(
                        group = group,
                        order=round,
                        fighter_id=obj.fighter_id,
                        fight_id=obj.fight_id
                    )
                    obj.save()

            fights.update(rounds=rounds, group=group)
            messages.success(request, 'rundy dodane')
            obj = form.save(commit=False)
            #TODO: dlaczego nie mogę dodać jednocześnie uczestników walki w rundzie
            return HttpResponseRedirect(reverse(
                "tournament_calculating:group_details",
                args=[group_id]
            ))
        else:
            form = AddRoundsForm
            return (
                render(request, "add_rounds.html", context={
                    'form': form,
                    'group_id': group_id,
                })
            )
    else:
        form = AddRoundsForm
        return (
            render(request, "add_rounds.html", context={
                'form': form,
                'group_id': group_id
            })
        )



def add_points (request, group_id, fight_id, round_id):
    group = Group.objects.get(pk=group_id)
    fight_rounds = Round.objects.filter(fight_id=fight_id)
    fight = Fight.objects.get(pk=fight_id)
    fights = group.fights.all()
    round_of_fight = fight_rounds.get(pk=round_id)
    first_fighter_points = []
    points_sum = []
    final_points = []
    second_final_points = []
    second_fighter_points = []
    second_points_sum = []
    participants = group.participants.order_by('-group_points')
    participants_avarege = group.participants.order_by('-points_average')

    # dodawanie punktów każdemu z przeciwników w walce
    if request.user.is_authenticated:
        form = AddPointsForm(request.POST, instance=round_of_fight)
        if request.method == "POST" and form.is_valid():
            form.save()
            for round_in_fight in fight.rounds_of_fight.all():
                first_fighter_points.append(round_in_fight.points_fighter_one)
                second_fighter_points.append(round_in_fight.points_fighter_two)
            for el in first_fighter_points:
                if type(el) == int:
                    points_sum.append(el)
            for el in second_fighter_points:
                if type(el) == int:
                    second_points_sum.append(el)
            final_points = sum(points_sum)
            second_final_points = sum(second_points_sum)
            fight.fighter_one_points = final_points
            fight.fighter_two_points = second_final_points
            fight.save()

            # sumowanie punktów dla wszystkich starć w walce?
            tournament_fights_points = []
            tournaments = Tournament.objects.all()
            for tournament in tournaments:
                if tournament.id == fight.tournament_id:
                    for tournament_fight in tournament.fights.all():
                        if tournament_fight.fighter_one_points is not None:
                            tournament_fights_points.append(tournament_fight.fighter_one_points)
                        if tournament_fight.fighter_two_points is not None:
                            tournament_fights_points.append(tournament_fight.fighter_two_points)
                        # if tournament_fight.fighter_one_points is None:
                        #     tournament_fights_points.append(0)
                        # else:
                        #     tournament_fights_points.append(tournament_fight.fighter_one_points)
                        # if tournament_fight.fighter_two_points is None:
                        #     tournament_fights_points.append(0)
                        # else:
                        #     tournament_fights_points.append(tournament_fight.fighter_two_points)

            tournaments_fighters_average = round(sum(tournament_fights_points) / len(tournament_fights_points), 2)
            print(tournaments_fighters_average)

            # dodawanie punktów za całęgo turnieju (ze wszystkich walk) każdemu uczestnikowi turnieju
            for participant in participants:
                for round_in_fight in fight.rounds_of_fight.all():
                    if round_in_fight.id == round_id:
                        print("round_in_fight", round_in_fight)
                        if fight.fighter_one_id == participant.id:
                            if round_in_fight.points_fighter_one is None:
                                round_in_fight.points_fighter_one = 0
                            # if round_in_fight.points_fighter_one is not None:
                                # round_in_fight.points_fighter_one = 0
                            participant.group_points = participant.group_points + round_in_fight.points_fighter_one
                            participant.points_average = participant.group_points / tournaments_fighters_average
                        if fight.fighter_two_id == participant.id:
                            if round_in_fight.points_fighter_two is None:
                            # if round_in_fight.points_fighter_two is not None:
                                round_in_fight.points_fighter_two = 0
                            participant.group_points = round_in_fight.points_fighter_two + participant.group_points
                            participant.points_average = participant.group_points / tournaments_fighters_average
                participant.save()

            messages.success(request, 'punkty dodane')

            return HttpResponseRedirect(reverse(
                "tournament_calculating:group_details",
                args=[group_id],
            ))
        else:
            form = AddPointsForm(instance=round_of_fight)
            return (
                render(request, "add_points.html", context={
                    'form': form,
                    'group': group,
                    'fight': fight,
                    'group_id': group_id,
                    'fight_id': fight_id,
                    'round_id':round_id,
                    'final_points':final_points,
                    'second_final_points': second_final_points,
                    'participants_avarege': participants_avarege
                })
            )
    else:
        form = AddPointsForm
        return (
            render(request, "add_points.html", context={
                'form': form,
                'group_id': group_id,
                'fight_id': fight_id,
                'round_id': round_id,
            })
        )