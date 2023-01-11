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
    AddPointsForm,
    GroupSummaryForm
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
    participants = group.participants.all().order_by("points_average")
    fights = group.fights.all().order_by('id')
    groups = Group.objects.filter(tournament=tournament).order_by("number")
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
    # ff = fights.filter(pk=group_id)
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


# TODO:  jeszcze for jeśli na początku jest taki sam co ostatnie, bo czasem się powtorzy z przodu
def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    group_fights = group.fights.all()
    if group_fights:
        group_fights.delete()
        group.save()
        for participant in group.participants.all():
            participant.group_points = 0
            participant.save()
    tournament = group.tournament
    fights = Fight.objects.all().order_by('id')
    participants_pairs = list(itertools.chain.from_iterable(itertools.combinations(group.participants.all(), r)
                                                            for r in range(2, 2 + 1)))
    left_participants = []
    right_participants = []
    result = []
    result_to_show = []
    for participant_pair in participants_pairs:
        result.append(participant_pair)
        left_participants.append(participant_pair[0])
        right_participants.append(participant_pair[1])
    order_number = 1

    # poniżej 6 walk nie ma możliwości bez powtórzeń więc:
    if len(result) > 6:
        result_to_show.append(random.choice(result))
        result.remove(result_to_show[0])

        #dopóki lista resul to show nie jest odpowiednio długa:
        while len(result_to_show) != int(len(list(group.participants.all())) * (len(list(group.participants.all()))-1) / 2):
            if result:
                var1 = random.choice(result)
            else:
                break
            condition_one = var1[0] != result_to_show[-1][0] and var1[1] != result_to_show[-1][0]
            condition_two = var1[0] != result_to_show[-1][1] and var1[1] != result_to_show[-1][1]
            # jeżeli się nie powatarzaja zawodnicy to dodajemy:
            if condition_one and condition_two and var1 not in result_to_show:
                result_to_show.append(var1)
                result.remove(var1)
                if var1 in result:
                    result.remove(var1)
            # jak wylosowany w wyloswanym el jakiś zawodnik się powtarza, to mieszamy:
            else:
                random.shuffle(result)
                # jeśli został jeden element to go wstawię na początek
                print("wstawilem na początek")
                if len(result_to_show) ==  int(((len(list(group.participants.all()))  * (len(list(group.participants.all())) -1)  ) /2) - 1):
                    condition_one = result[0] != result_to_show[0][0]
                    condition_two = result[0] != result_to_show[0][1]
                    # ale musi się nie powtarzać z tym początku żaden zawodnik w elemencie wciskanym:
                    if condition_one and condition_two:
                        result_to_show.insert(0,result[0])
                        print("wstawilem na pierwsze")
                    else:
                        result_to_show.insert(1, result[0])
                        print("WSATAWILEM NA DRUGIE :D")
                    break
                # jeśli zostały dwa elementy i w każdym jakiś zawodnik się powtarza:
                if len(result_to_show) ==  int(((len(list(group.participants.all()))  * (len(list(group.participants.all())) -1)  ) /2) - 2):
                    print("NOOOOO trzeba dopisać, co jak zostaną dwa elementy")
                    result_to_show.insert(0, result[0])
                    result_to_show.insert(0, result[1])
                    break
                # jeśli wszystkie się wstawiły dobrze i nic nie zostało:
                if len(result_to_show) == ((len(list(group.participants.all())) * len(list(group.participants.all()))) - 1) / 2:
                    print("nic nie wstawiałem wyszło za pierwszym razem")
                    break
    else:
        print("warunek że walk > 6 nie ruszył, nie da się zmieszać")
        for el in result:
            result_to_show.append(el)
            random.shuffle(result_to_show)

    if participants_pairs:
        group_fights.delete()
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

#TODO: nie usówa zapisów dla paricipantów
def delete_fights(request, tournament_id, group_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)
    group = Group.objects.get(pk=group_id)
    participants = group.participants.all()
    fights = group.fights.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            # group = Group.objects.get(pk=group_id)
            if request.user == tournament.user:
                fights.delete()
                for participant in participants:
                    for fight in fights:
                        if participant.id == fight.fighter_one_id or participant.id == fight.fighter_two_id:
                            participant.group_points = 0
                            participant.points_average = 0
                            participant.save()
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
    if request.user.is_authenticated:
        form = AddRoundsForm(request.POST, instance=group)
        fights = group.fights.all()
        rounds_of_group = group.rounds_of_group.all()
        if request.method == "POST" and form.is_valid():
            rounds = form.cleaned_data['rounds']
            if rounds_of_group:
                for round in rounds_of_group:
                    round.delete()
            obj = form.save(commit=False)
            obj.rounds = rounds
            obj.save()
            for fight in fights:
                obj = Round(fight_id=fight.id)
                for round in range(1, rounds + 1):
                    obj = Round(
                        group = group,
                        order=round,
                        fighter_one=fight.fighter_one,
                        fighter_two=fight.fighter_two,
                        fight_id=obj.fight_id
                    )
                    obj.save()

            fights.update(rounds=rounds, group=group)
            messages.success(request, 'rundy dodane')
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

# pierwsi walczący mają za mało punktów
def add_points (request, group_id, fight_id, round_id):
    print("początek funkcji add_points")
    group = Group.objects.get(pk=group_id)
    fight_rounds = Round.objects.filter(fight_id=fight_id)
    fight = Fight.objects.get(pk=fight_id)
    fights = group.fights.all()
    round_of_fight = fight_rounds.get(pk=round_id)
    first_fighter_points = []
    points_sum = []
    # final_points = []
    # second_final_points = []
    second_fighter_points = []
    second_points_sum = []
    participants = group.participants.order_by('-group_points')
    # participants_average = group.participants.order_by('-points_average')
    points_result_ls = ["0","1","2","3","4","5","6","7","8","9","10","11"]

    # dodawanie punktów każdemu z przeciwników w walce
    if request.user.is_authenticated:
        form = AddPointsForm(request.POST, instance=round_of_fight)
        if request.method == "POST" and form.is_valid():
            form.save()

            for round_in_fight in fight.rounds_of_fight.all():
                if round_in_fight.points_fighter_one in points_result_ls:
                # if round_in_fight.resolved_fighter_one == True:
                    first_fighter_points.append(int(round_in_fight.points_fighter_one))
                # if round_in_fight.resolved_fighter_two == True:
                if round_in_fight.points_fighter_two in points_result_ls:
                    second_fighter_points.append(int(round_in_fight.points_fighter_two))
            # tu zbieram punkty ze wszystkich rund w danej walce dla pierwszego zawodnika
            for el in first_fighter_points:
                if type(el) == int:
                    # bo jak jest None to nie działa
                    points_sum.append(el)
            # tu zbieram punkty ze wszystkich rund w danej walce dla drugiego zawodnika
            for el in second_fighter_points:
                if type(el) == int:
                    second_points_sum.append(el)
            final_points = sum(points_sum)
            second_final_points = sum(second_points_sum)
            fight.fighter_one_points = final_points
            fight.fighter_two_points = second_final_points
            fight.save()

            for p in participants:
                print("p", p.name)
                one_more_ls_to_append = []
                for fight in fights:
                    print("fight", fight.id)
                    if p.id == fight.fighter_one_id:
                        print("p", p.name)
                        one_more_ls_to_append.append(int(fight.fighter_one_points))
                        print("&&&&&&one_more_ls_to_append", one_more_ls_to_append, p.name)
                    if p.id == fight.fighter_two_id:
                        one_more_ls_to_append.append(int(fight.fighter_two_points))
                        print("druga&&&&&&one_more_ls_to_append", one_more_ls_to_append, p.name)
                    p.group_points = sum(one_more_ls_to_append)
                    p.save()

            tournament_fights_points = []
            tournaments = Tournament.objects.all()
            # dla każdego turnieju z turniejów:
            for tournament in tournaments:
                #jeśli jego id jest takie samo jak id turnieju walk:
                if tournament.id == fight.tournament_id:
                    # dla każdej walki w tego turnieju walkacj:
                    for tournament_fight in tournament.fights.all():
                        #jeśli w tej walce pierwszy zawodnik ma jakieś punkty:
                        if tournament_fight.fighter_one_points != 0:
                            #to dla tego turnieju punkty z walki powiększ o punkty tego zawodnika
                            tournament_fights_points.append(tournament_fight.fighter_one_points)
                            #jeśli drugi zawodnik ma jakieś punkty:
                        if tournament_fight.fighter_two_points != 0:
                            # to punkt dla tego turnieju powiększ o punkty tego zawodnika
                            tournament_fights_points.append(tournament_fight.fighter_two_points)
                    # TU WYLICZAM ŚREDNIĄ DO WYJSCIA
                    if tournament_fights_points is not None:
                        tournaments_fighters_average = round(sum(tournament_fights_points) / len(tournament_fights_points), 2)
                        tournament.tournament_average = tournaments_fighters_average
                        tournament.save()
                        for participant in participants:
                            participant.points_average = participant.group_points / tournaments_fighters_average
                            participant.save()

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



def group_summary(request, group_id):
    print("cokolwiek")
    group = Group.objects.get(pk=group_id)
    tournament_id = group.tournament_id

    if request.user.is_authenticated:
        print("dalej")
        form = GroupSummaryForm(request.POST, instance=group)
        print("jest form")
        if request.method == "POST" and form.is_valid():
            print("jeszcze dalej")
            instance = form.save(commit=False)
            print(instance)
            group.number_outgoing = instance.number_outgoing
            print(instance)
            print(group.number_outgoing)
            instance.save()



            return HttpResponseRedirect(reverse(
                "finals:finals",
                args=[group_id]
            ))
        else:
            form = GroupSummaryForm(instance=group)
            return (
                render(request, "group_summary.html", context={
                    'form': form,
                    'group': group,
                })
            )
    # else:
    #     form = GroupSummaryForm
    #     return (
    #         render(request, "group_summary.html", context={
    #             'form': form,
    #             'group_id': group_id,
    #
    #         })
    #     )
