import itertools
import random
import math
import time
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from tournaments.models import Tournament
from tournament_calculating.models import Group, Fight, Participant, Round
from tournament_calculating.forms import (
    AddParticipantForm,
    AddGroupForm,
    AddRoundsForm,
    AddPointsForm,
    GroupSummaryForm,
    # ParticipantFormSet,
    CreateParticipantForm
    )
from finals.models import Finalist


def participants_list(request):
    participants = Participant.objects.all().order_by('name')
    paginator = Paginator(participants, 20)
    page_number = request.GET.get('page')
    participants_register= paginator.get_page(page_number)
    participants_ids = []
    participants_user_ids = []
    for participant in participants:
        participants_user_ids.append(participant.user_id)
    for participant in participants:
        participants_ids.append(participant.id)
    context = {
               'participants_register': participants_register,
               'participants_ids': participants_ids,
               'participants_user_ids': participants_user_ids
               }
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


def create_participant(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateParticipantForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save()
                instance.user = request.user
                instance.save()
            return HttpResponseRedirect(reverse("tournament_calculating:participants_list"))
        else:
            form = CreateParticipantForm
        return (
            render(request, "create_participant.html", context={
                'form': form,
            })
        )

# to przykład z turniejów
# def edit_tournament(request, tournament_id):
#     tournament = Tournament.objects.get(pk=tournament_id)
#     user = request.user
#     if request.method == "POST":
#         if user.is_authenticated:
#             if user == tournament.user:
#                 form = TournamentForm(request.POST, request.FILES, instance=tournament)
#                 if form.is_valid():
#                     form.save()
#                     return HttpResponseRedirect(reverse('tournaments:tournament_details', args=[tournament_id] ))
#                 else:
#                     return redirect(reverse('login'))
#     else:
#         if user.is_authenticated:
#             if user == request.user:
#                 form = TournamentForm(instance=tournament)
#                 return render(request,"edit_tournament.html", {"form": form})



#na razie szare, zmieniam...
# def add_participant(request, tournament_id, group_id):
#     tournament = Tournament.objects.get(pk=tournament_id)
#     participants = Participant.objects.all()
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             form = AddParticipantForm(request.POST, request.FILES)
#             group = Group.objects.get(pk=group_id)
#             for participant in participants:
#                 if form.is_valid():
#                     instance = form.save()
#                     if participant == instance:
#                         # instance = form.save()
#                         # instance.name = instance.name
#                         participant.groups.add(group)
#                         participant.tournaments.add(tournament)
#                         # instance.save()
#                         participant.update()
#                 # instance.groups.add(group)
#                 # instance.name = instance.name
#                 # instance.tournaments.add(tournament)
#             return HttpResponseRedirect(reverse(
#                 "tournament_calculating:group_details",
#                 args=[group_id])
#                 )
#         else:
#             form = AddParticipantForm
#         return (
#             render(request, "add_participant.html", context={
#                 'form': form,
#                 'tournament_id': tournament_id,
#                 'group_id': group_id,
#             })
#         )
#

def add_participant(request, tournament_id, group_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    participants = Participant.objects.all()
    group = Group.objects.get(pk=group_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddParticipantForm(request.POST, request.FILES)
            if form.is_valid():
                print(form)
                print("form is valid")
                form.save()
                p_name = form.save(commit=False)
                # p_name.toutnament_id = tournament_id
                print("p_name.id",p_name.id)
                for p in participants:
                    if p.id == p_name.id:
                        print("instance",p_name.id)
                        print("p.name",p.id)
                        print(group.participants)
                        group.participants.add(p)
                        group.save()
                        form.save_m2m()
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





#TODO: dodać edycję grupy
def add_group(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    number = 0

    while number < 16:
        if request.user.is_authenticated:
            form = AddGroupForm(request.POST, instance=tournament)
            groups = tournament.groups.all()
            num_list = []
            for n in tournament.groups.all():
                num_list.append(n.number)
            # many_group_numbers = []
            # for g in groups:
            #     many_group_numbers.append(g.number)

            if request.method == "POST" and form.is_valid():
                if request.method == "POST" and form.is_valid():
                    # number = form.cleaned_data['number']

                    color_fighter_one = form.cleaned_data['color_fighter_one']
                    color_fighter_two = form.cleaned_data['color_fighter_two']
                    # if groups:
                    # if number not in many_group_numbers:

                    if number:
                        number = max(num_list)
                    else:
                        number = 0
                    number += 1
                    obj = form.save(commit=False)
                    # obj.number += 1
                    obj.color_fighter_one = color_fighter_one
                    obj.color_fighter_two = color_fighter_two

                    obj.save()
                    number += 1
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


# TODO: jeszcze for jeśli na początku jest taki sam co ostatnie, bo czasem się powtórzy z przodu
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
                    print("czy działa for")
                    # for fight in fights:
                    #     print("czy działa for")
                    #     if participant.id == fight.fighter_one_id or participant.id == fight.fighter_two_id:
                    #         participant.group_points = 0
                    #         print("participant.group_points ni e usuwa",participant.group_points)
                    #         participant.points_average = 0
                    #         participant.save()
                    participant.group_points = 0
                    participant.points_average = 0
                    participant.save()

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


def add_points (request, group_id, fight_id, round_id):
    group = Group.objects.get(pk=group_id)
    fight_rounds = Round.objects.filter(fight_id=fight_id)
    fight = Fight.objects.get(pk=fight_id)
    fights = group.fights.all()
    round_of_fight = fight_rounds.get(pk=round_id)
    first_fighter_points = []
    points_sum = []
    second_fighter_points = []
    second_points_sum = []
    participants = group.participants.order_by('-group_points')
    points_result_ls = ["0","1","2","3","4","5","6","7","8","9","10","11"]

    # dodawanie punktów każdemu z przeciwników w walce
    if request.user.is_authenticated:
        form = AddPointsForm(request.POST, instance=round_of_fight)
        if request.method == "POST" and form.is_valid():
            form.save()
            for round_in_fight in fight.rounds_of_fight.all():
                if round_in_fight.points_fighter_one in points_result_ls:
                    first_fighter_points.append(int(round_in_fight.points_fighter_one))
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
                one_more_ls_to_append = []
                for fight in fights:
                    if p.id == fight.fighter_one_id:
                        one_more_ls_to_append.append(int(fight.fighter_one_points))
                    if p.id == fight.fighter_two_id:
                        one_more_ls_to_append.append(int(fight.fighter_two_points))
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
                        if tournament_fight.fighter_one_points != 0 or tournament_fight.fighter_one_points !="dyskwalifikacja" or tournament_fight.fighter_one_points !="średnia" or tournament_fight.fighter_one_points !="kontuzja" or tournament_fight.fighter_one_points !="wycofanie":
                            #to dla tego turnieju punkty z walki powiększ o punkty tego zawodnika
                            tournament_fights_points.append(tournament_fight.fighter_one_points)
                            #jeśli drugi zawodnik ma jakieś punkty:
                        if tournament_fight.fighter_two_points != 0 or tournament_fight.fighter_one_points !="dyskwalifikacja" or tournament_fight.fighter_one_points !="średnia" or tournament_fight.fighter_one_points !="kontuzja" or tournament_fight.fighter_one_points !="wycofanie":
                            # to punkt dla tego turnieju powiększ o punkty tego zawodnika
                            tournament_fights_points.append(tournament_fight.fighter_two_points)
                    # TU WYLICZAM ŚREDNIĄ DO WYJSCIA

                    if tournament_fights_points is not None:
                    # if tournament_fights_points is not None  or tournament_fights_points !="dyskwalifikacja" or tournament_fights_points !="średnia" or tournament_fights_points !="kontuzja" or tournament_fights_points !="wycofanie" or tournament_fights_points != 0:
                        tournaments_fighters_average = round(sum(tournament_fights_points) / len(tournament_fights_points), 2)
                        tournament.tournament_average = tournaments_fighters_average
                        tournament.save()
                        for participant in participants:
                            if tournaments_fighters_average != 0:
                                participant.points_average = round((participant.group_points / tournaments_fighters_average),2)
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
                    'participants': participants,
                    'rounds': fight_rounds

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
                'participants':participants
            })
        )

"""
jeśli któryś z uczestników jest walczącym jeden w rundzie, gdzie walczącym dwa jest uczestnik,
który ma w jakiejś rundzie: kontuzję, dyskwalifikację lub wycofanie, to wtedy ten uczestnik ma punkty średnie 
równe tym ze wzoru
"""
"""
jeśli remis jest gdzieś na początku lub w środku,
to przechodzi i nie zwiększa countera, jeśli remis jest na końcu do zwiększa,
dodać dodatkowe punkty dla tych co nie walczyli z kontuzjowanymi 
i zdyskwalifikowanymi i poddanymi i nieobecnymi
"""

def group_summary(request, group_id):
    group = Group.objects.get(pk=group_id)
    participants = group.participants.all()
    group_average_points = []
    finalists_list = []
    for f in group.finalists.all():
        f.delete()
    rounds = group.rounds_of_group.all()
    maximum_amount_prtcp_rounds = []
    for participant in participants:
        for rd in rounds:
            if participant.id == rd.fighter_one_id or participant.id == rd.fighter_two_id:
                maximum_amount_prtcp_rounds.append(participant)
    # to maksymalna ilość walk w turnieju
    maximum_amount_prtcp_rounds = int(len(maximum_amount_prtcp_rounds) / len(participants))
    print(" 0 maksymalna ilość starć", maximum_amount_prtcp_rounds)
    list_of_participants = []
    for p in participants:
        list_of_participants.append(p)
    """
    dodaję punkty uzupełniające
    po participantach
    lista participantów i lista punktów
    jeśli pierwszy z listy prtcp ma tyle punktów co max z listy punktów:
    ładuję go do fianl list, jeśli nie sprawdzam to następny
    pobiera z formualrza ile uczetników z grupy ma przejść do finału, 
    kasuje tych, co już byli wytopowani, jeśli jest powtórzone działanie
    """
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            form = GroupSummaryForm(request.POST, instance=group)
            if request.method == "POST" and form.is_valid():
                instance = form.save()
                #----------------1-----------------------
                for participant in participants:
                    print("")
                    list_participant_rounds = []
                    #group_average_points (to potrzebne na końcu)
                    group_average_points.append(participant.points_average)
                    for rnd in rounds:
                        print(participant.name,"1 len(str(rnd.points_fighter_one))",len(str(rnd.points_fighter_one)))
                        print(participant.name,"2 rnd.points_fighter_one", rnd.points_fighter_one)
                        print(participant.name,"3 len(str(rnd.points_fighter_two))",len(str(rnd.points_fighter_two)))
                        print(participant.name,"4 rnd.points_fighter_two",rnd.points_fighter_two)
                        cond1 = len(str(rnd.points_fighter_one)) < 3 and len(str(rnd.points_fighter_two)) < 2
                        print(participant.name,"5 cond1",cond1)
                        # DODAWANIE ILOŚCI RUND DO PARTICIPANTÓW:
                        # jeśli zawodnik walczy jako pierwszy albo drugi w którejś z rund i w tej rundzie obaj mają przydzielone punkty:
                        if participant == rnd.fighter_one and cond1 or participant == rnd.fighter_two and cond1 :
                            list_participant_rounds.append(rnd.id)
                            participant.amount_rounds = len(list_participant_rounds)
                            print("6", participant.name, "ilość rund:",list_participant_rounds, participant.amount_rounds)
                            participant.save()

                #-------------------------2-----------------------------------------
                #teraz zamieniam napisy na wartości 0 i ze średniej:
                for participant in participants:
                    list_of_excuses = ["kontuzja","dyskwalifikacja","wycofanie", "poddanie"]
                    # jeśli brał udział w minium jednym starciu:
                    if participant.amount_rounds != 0:
                        for rnd in rounds:
                            # condition_1 = rnd.points_fighter_two == "kontuzja"
                            # condition_2 = rnd.points_fighter_two == "dyskwalifikacja"
                            # condition_3 = rnd.points_fighter_two == "wycofanie"
                            # condition_4 = rnd.points_fighter_one == "kontuzja"
                            # condition_5 = rnd.points_fighter_one == "dyskwalifikacja"
                            # condition_6 = rnd.points_fighter_one == "wycofanie"
                            # jeśli uczestnik jest pierwszym walczącym w rundzie, a drugi ma kontuzję, jest zdyswkalifikowany lub się wycofał:
                            # if participant == rnd.fighter_one and participant.amount_rounds != 0 and condition_1 or condition_2 or condition_3 :
                            if participant == rnd.fighter_one and participant.amount_rounds != 0 and  rnd.points_fighter_two in list_of_excuses :
                                # tu jest devision 0
                                # to pierwszy otrzymuje punkty ze średniej
                                participant.round_average = round(round(((round((maximum_amount_prtcp_rounds/participant.amount_rounds),2)) * participant.group_points),2)/maximum_amount_prtcp_rounds,2)
                                participant.save()
                                # a drugi otrzymuje zero (ten kontuzowany itp)
                                rnd.points_fighter_two = 0
                                rnd.points_fighter_one = participant.round_average
                                rnd.save()
                            # jeśli uczestnik jest drugim walczącym w rundzie, a pierwszy ma kontuzję, jest zdyswkalifikowany lub się wycofał:
                            # if participant == rnd.fighter_two and participant.amount_rounds != 0 and condition_4 or condition_5 or condition_6 :
                            if participant == rnd.fighter_two and participant.amount_rounds != 0 and rnd.points_fighter_one in list_of_excuses:
                                # tu też jest devision 0
                                participant.round_average = round(round(((round((maximum_amount_prtcp_rounds/participant.amount_rounds),2)) * participant.group_points),2)/maximum_amount_prtcp_rounds,2)
                                participant.save()
                                rnd.points_fighter_one = 0
                                rnd.points_fighter_two = participant.round_average
                                rnd.save()


                            #-------------------------3---------------------------------------
                            # dodawanie punktów za walki, które się nie odbyły:

                            # jeśli uczestnik nie ma w rundach pierwszych w tej grupie kontuzji tp...
                            if not "kontuzja" or "dyskwalifikacja" or "wycofanie" in participant.rounds_of_participant_one.filter(group_id=group_id):
                                for x in participant.rounds_of_participant_one.filter(group_id=group_id):
                                    print("X", x.points_fighter_one, not "kontuzja" or "dyskwalifikacja" or "wycofanie" in participant.rounds_of_participant_one.filter(group_id=group_id))
                                # jeśli zawodnnik jest pierwszym walczącym i nie ma punktów w rundzie,
                                # ale ma jakieś punkty w grupie i jakąś ilość rund, w których wziął udział
                                if participant == rnd.fighter_one \
                                        and rnd.points_fighter_one is None \
                                        and participant.group_points is not None \
                                        and participant.amount_rounds != 0:
                                    print("7",participant.name, "ilość rund i średnia", participant.amount_rounds, participant.round_average)

                                    participant.round_average = round(round(((round((maximum_amount_prtcp_rounds / participant.amount_rounds),2)) * participant.group_points), 2) / maximum_amount_prtcp_rounds, 2)
                                    if type(participant.round_average) == int:
                                        participant.save()
                                    if type(participant.round_average) == float:
                                        if participant.round_average.is_integer():
                                            participant.round_average = int(participant.round_average)
                                            participant.save()
                                        else:
                                            participant.save()
                                    rnd.points_fighter_one = participant.round_average
                                    rnd.points_fighter_two = 0
                                    print("8 jedynka", participant.name, "punkt z rund:", rnd.points_fighter_one, rnd.points_fighter_two)
                                    rnd.save()

                            else:
                                #jeśli zawodnik ma kontuzję w jakiejś rundzie drugiej i w tej rundzie jest walczącym nr jeden
                                if "kontuzja" or "dyskwalifikacja" or "wycofanie" in participant.rounds_of_participant_one.filter(group_id=group_id) \
                                and participant == rnd.fighter_one:
                                    rnd.points_fighter_one = 0
                                    rnd.points_fighter_two = 0
                                    rnd.save()

                            if not "kontuzja" or "dyskwalifikacja" or "wycofanie" in participant.rounds_of_participant_two.filter(group_id=group_id) \
                                    or "kontuzja" or "dyskwalifikacja" or "wycofanie" in participant.rounds_of_participant_one.filter(
                                group_id=group_id):
                                if participant == rnd.fighter_two \
                                        and rnd.points_fighter_two is None \
                                        and participant.group_points is not None \
                                        and participant.amount_rounds != 0 :
                                    participant.round_average = round(round(((round((maximum_amount_prtcp_rounds / participant.amount_rounds),2)) * participant.group_points), 2) / maximum_amount_prtcp_rounds, 2)
                                    if type(participant.round_average) == int:
                                        participant.save()
                                    if type(participant.round_average) == float:
                                        if participant.round_average.is_integer():
                                            participant.round_average = int(participant.round_average)
                                            participant.save()
                                        else:
                                            participant.save()
                                    rnd.points_fighter_two = participant.round_average
                                    rnd.points_fighter_one = 0
                                    print(" 9 dwójka",participant.name, "punkt z rund:", rnd.points_fighter_one, rnd.points_fighter_two)
                                    rnd.save()
                            else:
                                if "kontuzja" or "dyskwalifikacja" or "wycofanie" in participant.rounds_of_participant_two.filter(group_id=group_id) \
                                and participant == rnd.fighter_two:
                                    rnd.points_fighter_one = 0
                                    rnd.points_fighter_two = 0
                                    rnd.save()
                            # FIXME: /
                            """
                            może to musi być zamienione na jeden warunek po participant albo walczy jako drugi albo jako pierwszy...
                            """
                        print("9", participant.name, ", rundy:", participant.amount_rounds, ", punkty:",
                              participant.group_points, ", średnia:", participant.round_average)

                print("")
                for p in participants:
                    print("10 imię:", p.name, ", ilość rund", p.amount_rounds, ", punkty cząstkowe", p.group_points, ", średnia rundowa", p.round_average, ", punkty wyjściowe", p.points_average)
                for r in rounds:
                    print(r.points_fighter_one, r.fighter_one.name)
                    print(r.points_fighter_two, r.fighter_two.name)

                counter = 0
                counter = group.number_outgoing
                group.refresh_from_db()
                group.number_outgoing = instance.number_outgoing
                instance.save()
                group.refresh_from_db()
                if group.finalists:
                    for f in group.finalists.all():
                        f.delete()

                i = 0
                """
                dopóki ilość foinalistów jest mniejsza niż ilość uczestników przechodzących do finału,
                podana w formularzu 
                """
                while len(finalists_list) < int(counter):
                    """
                    jeśli są już wytypowani wcześniej finaliści:
                    """
                    if finalists_list and list_of_participants:
                        """
                        jeśli pierwszy z uczetsników w grupie nie jest na liście finalistów:
                        """
                        if list_of_participants and list_of_participants[i] not in finalists_list:
                            """
                            jeśli punkty wyjściowe pierwszego z uczestników są takie same jak
                            najwyższe punkty wyjściowe w grupie:
                            """
                            if list_of_participants[i].points_average == max(group_average_points):
                                """
                                to ten uczestnik pojawia w się w liście finalistów
                                """
                                finalists_list.append(list_of_participants[i])
                                """
                                ten uczestnik znika z lity uczestników grupy
                                """
                                list_of_participants.remove(list_of_participants[i])
                                """
                                z listy punktów wyjściowych w grupie znikają jego punkty
                                (jak to działa w przypadku remisów?)
                                """
                                group_average_points.remove(max(group_average_points))
                                random.shuffle(list_of_participants)
                                if  len(finalists_list) == counter and group_average_points and finalists_list[-1].points_average == max(group_average_points):
                                    "czwarty if"
                                    counter += 1
                            else:
                                """
                                jeśli punkty wyjściowe pierwszego z zawodników nie są takie same jak
                                najwyższe punkty wyjściowe w grupie:
                                """
                                random.shuffle(list_of_participants)
                    else:
                        """
                        jeśli nie ma listy wylosowanych już finalistów
                        """
                        """
                        jeśli uczestnik ma takie punkty wyjściowe jak najwyższe z pozostałych z listy punktów w grupie
                        """
                        if list_of_participants[i].points_average == max(group_average_points):
                            finalists_list.append(list_of_participants[i])
                            list_of_participants.remove(list_of_participants[i])
                            group_average_points.remove(max(group_average_points))
                            if  len(finalists_list) == counter and group_average_points and finalists_list[-1].points_average == max(group_average_points):
                                counter += 1
                            random.shuffle(list_of_participants)
                            """
                            jeśli uczestnik ma inne punkty wyjściowe niż najwyższe z listy punktów w grupie
                            """
                        else:
                            random.shuffle(list_of_participants)
                finalists = finalists_list
                """
                jeśli jest remis na końcu, counter (ilość finalistów) musi się zwiększyć 
                o tyle ile jest uczestników z tym samym wynikiem
                """


                for f in finalists:
                    group.finalists.create(participant=f)
                group.save()
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
