import itertools
import random
import math
import time
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
    tournaments_fighters_average = tournament.tournament_average
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
        "groups": groups,
        "tournaments_fighters_average": tournaments_fighters_average
    })


def fight_details(request, group_id, fight_id):

    group = Group.objects.get(pk=group_id)
    fight = Fight.objects.get(pk=fight_id)
    rounds_obj = group.rounds_of_group.all()
    number = group.number
    tournament = group.tournament
    groups = Group.objects.all(tournament=tournament)
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
        "groups": groups
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
                color_fighter_one = form.cleaned_data['color_fighter_one']
                color_fighter_two = form.cleaned_data['color_fighter_two']
                # if groups:
                if number not in many_group_numbers:
                    obj = form.save(commit=False)
                    obj.number = number
                    obj.color_fighter_one = color_fighter_one
                    obj.color_fighter_two = color_fighter_two
                    obj.save()
                    groups.create(number=number, tournament=tournament, color_fighter_one=color_fighter_one, color_fighter_two=color_fighter_two)
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


# def sorting(some_list):
#     length = len(some_list)
#     final_list = []
#     sorting_result = []
#     if length > 2:
#         final_list.append(random.choice(some_list))
#         print("final_list", final_list)
#         print("len(final_list)", len(final_list))
#         if length > 6:
#             # sorting_result.append(some_list[0])
#             # some_list.remove(some_list[0])
#             # while len(sorting_result) != length:
#             #     condition_one = sorting_result[-1][0] != some_list[0][0] and sorting_result[-1][0] != some_list[0][1]
#             #     condition_two = sorting_result[-1][1] != some_list[0][1]and sorting_result[-1][1] != some_list[0][0]
#             #     if condition_one and condition_two:
#             #         sorting_result.append(some_list[0])
#             #         some_list.remove(some_list[0])
#             #     else:
#             #         some_list.append(some_list[0])
#             #         some_list.remove(some_list[0])
#             temp_var = random.choice(some_list)
#             temp_var2 = 0
#             final_list.append(temp_var)
#             some_list.remove(temp_var)
#             while len(some_list) > 0:
#                 if some_list[0][0] == final_list[-1][0] or some_list[0][1] == final_list[-1][1]:
#                 # for el in some_list:
#                 #     print("el")
#                 #     if el[0] == final_list[-1][0] or el[1] == final_list[-1][1]:
#                     temp_var2 = random.choice(some_list)
#                     print("oj, powtarza się")
#                 else:
#                     print("oooo, nie powtarza się")
#                     final_list.append(temp_var2)
#                     some_list.remove(some_list[0])
#                     # print("final_list", final_list)
#                     sorting_result = final_list
#         else:
#             random.shuffle(some_list)
#             sorting_result = some_list
#         return sorting_result


def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    group_fights = group.fights.all()
    tournament = group.tournament
    fights = Fight.objects.all().order_by('id')
    participants = group.participants.all()
    participants_pairs = list(itertools.chain.from_iterable(itertools.combinations(group.participants.all(), r)
                                                            for r in range(2, 2 + 1)))
    left_participants = []
    right_participants = []
    result = []
    result_to_show = []
    var1 = []

    for participant_pair in participants_pairs:
        result.append(participant_pair)
        left_participants.append(participant_pair[0])
        right_participants.append(participant_pair[1])

    order_number = 1
    # print("result", result)
    # result_to_show = sorting(result)
    result_to_show.append(random.choice(result))
    result.remove(result_to_show[0])
    print(type(result_to_show))
    print("g.p.a", type(group.participants.all()))
    print("l,g,p,a", type(list(group.participants.all())))
    xxx = list(group.participants.all())
    for el in group.participants.all():
        xxx.append(el)
    print("xxx", xxx)
    print("Leeeeeeeeeeeen wzór", (len(list(group.participants.all())) * (len(list(group.participants.all()))-1)) / 2)
    # while len(result) > 0:

    while len(result_to_show) < len(list(group.participants.all())) * len(list(group.participants.all()))-1 / 2:
        print("to się ciągle pętluje")
        if result:
            var1 = random.choice(result)

        print("result początek pętli", result)

        print("var1 tupla", var1)
        print("Var[0]", var1[0].name)
        print("var[1]", var1[1].name)
        print("result_to_show[-1][0]", result_to_show[-1][0].name)
        print("result_to_show[-1][1]", result_to_show[-1][1].name)
        condition_one = var1[0] != result_to_show[-1][0] and var1[1] != result_to_show[-1][0]
        condition_two = var1[0] != result_to_show[-1][1] and var1[1] != result_to_show[-1][1]
        print("RESULT", result)
        # print(result[0][0])
        # print(result[0][1])
        print(result_to_show[-1][0])
        print(result_to_show[-1][1])
        print(condition_one)
        print(condition_two)
        time.sleep(1)
        if condition_one and condition_two and var1 not in result_to_show:
            print("oba warunki spełnione")
            result_to_show.append(var1)
            result.remove(var1)
            print("result to show po dodaniu var1", result_to_show)
            # for el in result:
            #     if el == var1:
            if var1 in result:
                print("tak el == var1 in result")
                result.remove(var1)
            print("resultttt to show in pętla", result_to_show)
            # vvv =
            # result.remove(result[0])
            print("resulttttt in pętla", result)
            # return result_to_show
            print("LLLLEEEENNNN len result i len result to show", len(result), len(result_to_show))
            time.sleep(1)
        else:
            print("jednak warunek nie jest spełniony, będzie losować var1")
            print("result to show po dodaniu var1", result_to_show)
            print(len(result_to_show))
            # if len(result_to_show) == len(list(group.participants.all())) * len(list(group.participants.all()))-1 / 2:
                # if var1 in result:
                #     print("tak el == var1 in result")
                #     result.remove(var1)
            random.shuffle(result)
            print("result after shuffle", result)
            print("LLLLEEEENNNN len result i len result to show", len(result), len(result_to_show))
            if len(result_to_show) == len(list(group.participants.all())) * len(list(group.participants.all()))-1 / 2 -1:
                result_to_show.insert(0,result[0])
                break
            if len(result_to_show) == len(list(group.participants.all())) * len(list(group.participants.all())) - 1 / 2:
                break

            time.sleep(1)
    print("TERAZ********************TERAZ będzie dodawanie do bazy", result_to_show)
    if participants_pairs:
        group_fights.delete()
        print("delete done")
        for right_participant in result_to_show:
            print("reslt to show", result_to_show)
            for el in result_to_show:
                print(el)
            print("jjjjjjjright participant", right_participant)
            fights.get_or_create(
                # id = right_participant[0][0],
                order=order_number,
                group=group,
                tournament=tournament,
                fighter_one=right_participant[0],
                fighter_two=right_participant[1]
            )
            order_number +=1
    return HttpResponseRedirect(reverse("tournament_calculating:group_details",
                                        args=[group_id]))

#


# def sorting(some_list):
#     length = len(some_list)
#     sorting_result = []
#     if length > 2:
#         if length > 6:
#             sorting_result.append(some_list[0])
#             some_list.remove(some_list[0])
#             while len(sorting_result) != length:
#                 condition_one = sorting_result[-1][0] != some_list[0][0] and sorting_result[-1][0] != some_list[0][1]
#                 condition_two = sorting_result[-1][1] != some_list[0][1]and sorting_result[-1][1] != some_list[0][0]
#                 if condition_one and condition_two:
#                     sorting_result.append(some_list[0])
#                     some_list.remove(some_list[0])
#                 else:
#                     some_list.append(some_list[0])
#                     some_list.remove(some_list[0])
#         else:
#             random.shuffle(some_list)
#             sorting_result = some_list
#         return sorting_result
#
#
# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     tournament = group.tournament
#     fights = Fight.objects.all()
#     rounds = None
#     participants_pairs = list(itertools.chain.from_iterable(itertools.combinations(group.participants.all(), r)
#                                                             for r in range(2, 2 + 1)))
#     left_participants = []
#     right_participants = []
#     result = []
#
#     for participant_pair in participants_pairs:
#         result.append(participant_pair)
#         left_participants.append(participant_pair[0])
#         right_participants.append(participant_pair[1])
#
#     result_to_show = sorting(result)
#     if participants_pairs:
#         for right_participant in result_to_show:
#             fights.get_or_create(
#                 group=group,
#                 rounds=rounds,
#                 tournament=tournament,
#                 fighter_one=right_participant[0],
#                 fighter_two=right_participant[1]
#             )
#
#     return HttpResponseRedirect(reverse("tournament_calculating:group_details",
#                                         args=[group_id]))
#



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
    participants_average = group.participants.order_by('-points_average')
    tournaments_fighters_average = 0
    prtcp_ls = []
    points_trnm_fights = []
    points_trnm_fights2 = []

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
            # print("FINAL POINTS", final_points)
            fight.fighter_two_points = second_final_points
            fight.save()

            # sumowanie punktów dla wszystkich starć w walce?
            # tournament_fights_points = []
            # tournaments = Tournament.objects.all()
            # for tournament in tournaments:
            #     if tournament.id == fight.tournament_id:
            #         for tournament_fight in tournament.fights.all():
            #             if tournament_fight.fighter_one_points != 0:
            #                 tournament_fights_points.append(tournament_fight.fighter_one_points)
            #             if tournament_fight.fighter_two_points != 0:
            #                 tournament_fights_points.append(tournament_fight.fighter_two_points)
            #
            # tournaments_fighters_average = round(sum(tournament_fights_points) / len(tournament_fights_points), 2)
            # tournament.tournament_average = tournaments_fighters_average
            # tournament.save()
            #
            # print(tournaments_fighters_average)
            # print("tournament_fights_points", tournament_fights_points)
            # print("round(sum(tournament_fights_points)", round(sum(tournament_fights_points)))
            # print("len(tournament_fights_points), 2)", len(tournament_fights_points))
            # print("tournaments_fighters_average", tournaments_fighters_average)
            # print("round_in_fight1", round_in_fight.points_fighter_one)
            # print("round_in_fight2", round_in_fight.points_fighter_two)
            #
            # for f in fights:
            #     print("f.fighter_one.name", f.fighter_one.name)
            #
            # fight_fighter_points = []
            # fight_fighter_points2 = []
            #
            # for participant in participants:
            #     prtcp_fights = fights.filter(fighter_one=participant)
            #     for x in prtcp_fights:
            #         print(x.fighter_one_id)
            #
            #     for fight in prtcp_fights:
            #         # if participant.id == fight.fighter_one_id:
            #         if participant.name == fight.fighter_one.name:
            #             prtcp_ls.append(participant.name)
            #             print(prtcp_ls)
            #             print("partcipant.name", participant.name)
            #
            #
            #             fight_fighter_points.append(fight.fighter_one_points)
            #
            #
            #             print("fight.fighter_one_points", fight.fighter_one_points)
            #             print("fight_fighter_points",fight_fighter_points)
            #
            #             participant.group_points = sum(fight_fighter_points)
            #             participant.save()
            #         if participant.id == fight.fighter_two_id:
            #             fight_fighter_points2.append(fight.fighter_two_points)
            #             participant.group_points = sum(fight_fighter_points)
            #             participant.save()

            temp_var = []
            var2 = {}
            var3 = []
            var4 = {}
            var5 = []

            for fight in fights:
                print("fight", fight.fighter_one_points)
                for participant in participants:
                    print("participant", participant.name)

                    if participant.id == fight.fighter_one_id:
                        print("uuuuuuuuuuuuuuuuparticipant.name", participant.name)
                        var2 = {participant.name: fight.fighter_one_points}
                        var3.append(var2)
                        print("var2",var2)
                        print("var3", var3)
                        for x in var3:
                            print(x.keys())

                    if participant.id == fight.fighter_two_id:
                        print("uuuuuuuuuuuuuuuuparticipant.name", participant.name)
                        var4 = {participant.name: fight.fighter_two_points}
                        var5.append(var4)
                        print("var4", var4)
                        print("var5", var5)


                        for p_round in participant.rounds_of_participant.all():
                            print("p_round", p_round)
                            if p_round.fight_id == fight_id:
                                print("TAK")
                                # if p_round.points_fighter_one is not None:
                                temp_var.append(p_round.points_fighter_one)

                                participant.group_points = sum(temp_var)
                                print("p_round.points_fighter_one",p_round.points_fighter_one)
                                print("temp_var",temp_var)
                                print("participant.group_points",participant.group_points)
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
                    'participants_average': participants_average,
                    'tournaments_fighters_average': tournaments_fighters_average
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




# def add_points (request, group_id, fight_id, round_id):
#     group = Group.objects.get(pk=group_id)
#     fight_rounds = Round.objects.filter(fight_id=fight_id)
#     fight = Fight.objects.get(pk=fight_id)
#     fights = group.fights.all()
#     round_of_fight = fight_rounds.get(pk=round_id)
#     first_fighter_points = []
#     points_sum = []
#     final_points = []
#     second_final_points = []
#     second_fighter_points = []
#     second_points_sum = []
#     participants = group.participants.order_by('-group_points')
#     participants_avarege = group.participants.order_by('-points_average')
#     tournaments_fighters_average = 0
#
#     # dodawanie punktów każdemu z przeciwników w walce
#     if request.user.is_authenticated:
#         form = AddPointsForm(request.POST, instance=round_of_fight)
#         if request.method == "POST" and form.is_valid():
#             form.save()
#             for round_in_fight in fight.rounds_of_fight.all():
#                 first_fighter_points.append(round_in_fight.points_fighter_one)
#                 second_fighter_points.append(round_in_fight.points_fighter_two)
#             for el in first_fighter_points:
#                 if type(el) == int:
#                     points_sum.append(el)
#             for el in second_fighter_points:
#                 if type(el) == int:
#                     second_points_sum.append(el)
#             final_points = sum(points_sum)
#             second_final_points = sum(second_points_sum)
#             fight.fighter_one_points = final_points
#             fight.fighter_two_points = second_final_points
#             fight.save()
#
#             # sumowanie punktów dla wszystkich starć w walce?
#             tournament_fights_points = []
#             tournaments = Tournament.objects.all()
#             for tournament in tournaments:
#                 if tournament.id == fight.tournament_id:
#                     for tournament_fight in tournament.fights.all():
#                         if tournament_fight.fighter_one_points is not None:
#                             tournament_fights_points.append(tournament_fight.fighter_one_points)
#                         if tournament_fight.fighter_two_points is not None:
#                             tournament_fights_points.append(tournament_fight.fighter_two_points)
#                         # if tournament_fight.fighter_one_points is None:
#                         #     tournament_fights_points.append(0)
#                         # else:
#                         #     tournament_fights_points.append(tournament_fight.fighter_one_points)
#                         # if tournament_fight.fighter_two_points is None:
#                         #     tournament_fights_points.append(0)
#                         # else:
#                         #     tournament_fights_points.append(tournament_fight.fighter_two_points)
#
#             tournaments_fighters_average = round(sum(tournament_fights_points) / len(tournament_fights_points), 2)
#             print("tournament_fights_points", tournament_fights_points)
#             print("round(sum(tournament_fights_points)", round(sum(tournament_fights_points)))
#             print("len(tournament_fights_points), 2)", len(tournament_fights_points), 2)
#             print("tournaments_fighters_average", tournaments_fighters_average)
#
#             # dodawanie punktów za całęgo turnieju (ze wszystkich walk) każdemu uczestnikowi turnieju
#             for participant in participants:
#                 for round_in_fight in fight.rounds_of_fight.all():
#                     if round_in_fight.id == round_id:
#                         if fight.fighter_one_id == participant.id:
#                             if round_in_fight.points_fighter_one is None:
#                                 round_in_fight.points_fighter_one = 0
#                             participant.group_points = participant.group_points + round_in_fight.points_fighter_one
#                             participant.save(update_fields=['group_points'])
#                             participant.points_average = participant.group_points / tournaments_fighters_average
#                             participant.save()
#                         else:
#                             participant.group_points = 0
#                             participant.group_points = participant.group_points + round_in_fight.points_fighter_one
#                             participant.save(update_fields=['group_points'])
#                             participant.points_average = participant.group_points / tournaments_fighters_average
#                             participant.save()
#                         if fight.fighter_two_id == participant.id:
#                             if round_in_fight.points_fighter_two is None:
#                                 round_in_fight.points_fighter_two = 0
#                             participant.group_points = round_in_fight.points_fighter_two + participant.group_points
#                             participant.save(update_fields=['group_points'])
#                             participant.points_average = participant.group_points / tournaments_fighters_average
#                             participant.save()
#                         else:
#                             participant.group_points = 0
#                             participant.group_points = participant.group_points + round_in_fight.points_fighter_two
#                             participant.save(update_fields=['group_points'])
#                             participant.points_average = participant.group_points / tournaments_fighters_average
#                             participant.save()
#                 # participant.save()
#
#             messages.success(request, 'punkty dodane')
#
#             return HttpResponseRedirect(reverse(
#                 "tournament_calculating:group_details",
#                 args=[group_id],
#             ))
#         else:
#             form = AddPointsForm(instance=round_of_fight)
#             return (
#                 render(request, "add_points.html", context={
#                     'form': form,
#                     'group': group,
#                     'fight': fight,
#                     'group_id': group_id,
#                     'fight_id': fight_id,
#                     'round_id':round_id,
#                     'final_points':final_points,
#                     'second_final_points': second_final_points,
#                     'participants_avarege': participants_avarege,
#                     'tournaments_fighters_average': tournaments_fighters_average
#                 })
#             )
#     else:
#         form = AddPointsForm
#         return (
#             render(request, "add_points.html", context={
#                 'form': form,
#                 'group_id': group_id,
#                 'fight_id': fight_id,
#                 'round_id': round_id,
#             })
#         )