import itertools
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
    return render(request, "group_details.html", context={
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
        if request.method == "POST" and form.is_valid():
            number = form.cleaned_data['number']
            for group in groups:
                if number != group.number:
                    obj = form.save(commit=False)
                    obj.number = number
                    obj.save()
                    groups.create(number=number, tournament=tournament)
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

# fight = {
# "group":wylosowana_grupa,
# "fighter_one":pierwszy_fighter,
# "fighter_two" :drugi_fighter,
# "tournament" : tournament ,
# "rounds" : rounds
# }
# Teraz jakos w petli dodajesz tak tworzone slowniki do listy i nastepnie z lista robisz
# Fight.objects.bulk_create(lista_slownikow)


# tylko podzielić zawodników


# nie działa
def add_fights(request, group_id):
    # pass
    group = Group.objects.get(pk=group_id)
    tournament = group.tournament
    participants = group.participants.all()
    participants_ids = participants.values('id')
    only_ids_ls = [i.get('id', 0) for i in participants_ids]
    participants_pairs = list(itertools.combinations(only_ids_ls, 2))
    group.fighters_one = [p[0] for p in participants_pairs]
    group.fighters_two = [p[1] for p in participants_pairs]
    if request.user.is_authenticated:
        form = AddGroupForm(request.POST)
        if request.method == "POST" and form.is_valid():
            rounds = form.cleaned_data['rounds']
            rounds.save()
            print(rounds)
            for participant_pair in participants_pairs:
                fights_dict_list = []
                fight = {
                    "group": group,
                    "rounds": rounds,
                    "tournament": tournament,
                    "fighter_one": group.participants.get(id=participant_pair[0]),
                    "fighter_two": group.participants.get(id=participant_pair[1]),
                    }
                fights_dict_list.append(fight)
                Fight.objects.bulk_create(fights_dict_list)
            return HttpResponseRedirect(reverse("tournaments:tournament_details", args=[group_id]))

        else:
            form = AddFightsForm
            return (
                render(request, "add_fights.html", context={
                    'form': form,
                    'group_id': group_id,
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
#     # fights.create(group=group,
#     tournament=tournament,
#     fighter_one=first_fighter,
#     fighter_two=second_fighter)
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
#     # fights.create(group=group,
#     tournament=tournament,
#     fighter_one=first_fighter,
#     fighter_two=second_fighter)
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

# od nowa z group


# teraz z values
def draw_fights(request, group_id):
    group = Group.objects.get(pk=group_id)
    number = group.number
    tournament = group.tournament
    participants = group.participants.all()
    participants_ids = participants.values('id')
    only_ids_ls = [i.get('id', 0) for i in participants_ids]
    fights = group.fights.all()
    rounds = 5
    first_participant = Participant.objects.first()
    last_participant = Participant.objects.last()
    participants_pairs = list(itertools.combinations(only_ids_ls, 2))
    group.fighters_one = [p[0] for p in participants_pairs]
    group.fighters_two = [p[1] for p in participants_pairs]
    for fight in fights:
        for first in group.fighters_one:
            for second in group.fighters_two:
                fighter_one = group.participants.get(id=first)
                fighter_two = group.participants.get(id=second)
                fights.create(
                    group=group,
                    rounds=rounds,
                    tournament=tournament,
                    fighter_one=fighter_one,
                    fighter_two=fighter_two
                )
    # for id_element in only_ids_ls:
    #     fight = {
    #         "group": group,
    #         "rounds": rounds,
    #         "tournament": tournament,
    #         "fighter_one": fighter_one(id=id_element[0]),
    #         "fighter_two": fighter_two(id=id_element[1]),
    #     }
    # fights_list.append(fight)
    # Fight.objects.bulk_create(fights_list)
    return render(request, "group_sorted.html", context={
        "number": number,
        "tournament": tournament,
        "group_id": group_id,
        "participants": participants,
        "first_participant": first_participant,
        "last_participant": last_participant,
        "fights": fights,
        "participants_pairs": participants_pairs
    })


# jak wyświetlić
# def draw_fights(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     number = group.number
#     tournament = group.tournament
#     participants = group.participants.all()
#     fights = group.fights.all()
#     rounds = 5
#     first_participant = Participant.objects.first()
#     last_participant = Participant.objects.last()
#     participants_pairs= list(itertools.combinations(participants, 2))
#     first_fighters = []
#     for ff in participants_pairs:
#         first_fighters.append(ff[0])
#     second_fighters = []
#     for sf in participants_pairs:
#         second_fighters.append(sf[1])
#     f_one = first_fighters[0]
#     f_two = second_fighters[0]
#     fights_list = []
#     for e in fights:
#         fight = {
#             "group": e.group,
#             "rounds": e.rounds,
#             "tournament": e.tournament,
#             "fighter_one": e.f_one,
#             "fighter_two": e.f_two,
#         }
#         fights_list.append(fight)
#     Fight.objects.bulk_create(fights_list)
#     return render(request, "group_sorted.html", context={
#         "number": number,
#         "tournament": tournament,
#         "group_id": group_id,
#         "participants": participants,
#         "first_participant": first_participant,
#         "last_participant": last_participant,
#         "fights": fights,
#         "first_fighters": first_fighters,
#         "second_fighters":second_fighters,
#         "participants_pairs": participants_pairs
#     })


# batch = [CounterFileData(date=row['date'], value=['value'] for row in parsed_data)]
# CounterFileData.objects.bulk_create(batch)
# # nowe z jednym wynikiem ładnym
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
#     print("participants:")
#     print(participants)
#     # print(participants[0])
#     # print(participants[-1])
#     first_random_fighter = participants[randint(0, count - 1)]
#     # print(first_random_fighter)
#     random_opponent = participants[randint(0, count -1)]
#     # print(random_opponent)
#     random_opponents = []
#     random_first_fighters = []
#
#     # for i in range(count):
#
#     # result = []
#     # for p in participants:
#         # result.append(list(itertools.combinations([range(len(participants))], 2)))
#         # result.append(list(itertools.combinations([participants_ids], 2)))
#         # if first_random_fighter not in random_opponents:
#         #     if random_opponent not in random_first_fighters:
#         #         if random_first_fighters not in random_first_fighters:
#         #             if random_opponent not in random_opponents:
#         #                 if first_random_fighter != random_opponent:
#         #                     random_first_fighters.append(first_random_fighter)
#         #                     random_opponents.append(random_opponent)
#     # print(random_first_fighters)
#     # print(random_opponents)
#     # print("result:")
#     # print(result)
#
#     participants_ids = []
#     for p in participants:
#         participants_ids.append(p.id)
#     print("participants_ids:")
#     print(participants_ids)
#     # example = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8], 2))
#     example = list(itertools.combinations(participants, 2))
#     print("example")
#     print(example)
#     ff = []
#     for f in example:
#         ff.append(f[0])
#     print("ffaaaaaaaaaaaaaaaaaaaaa")
#     print("ff")
#     print(ff)
#     print("ff[0]")
#     print(ff[0])
#     sf = []
#     for f in example:
#         sf.append(f[1])
#     print("sf")
#     print(sf)
#     print("sf[0]")
#     print(sf[0])
#
#     # fighters_pairs = []
#     # for f in ff:
#     #     for s in sf:
#     #         fighters_pairs.append(zip(f,s))
#     # print("fighters_pairs:")
#     # print(fighters_pairs)
#
#
#     participants_pairs = list(itertools.combinations([participants_ids], 2))
#
#     print("participants_pairs:")
#     print(participants_pairs)
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
#         "exemple": example,
#         "ff": ff,
#         "sf":sf
#     })

# @dataclass(frozen=True)
# class Fighter:
#     id: int


# najnowsze
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
#     # print(participants)
#     first_random_fighter = participants[randint(0, count - 1)]
#     random_opponent = participants[randint(0, count -1)]
#     random_opponents = []
#     random_first_fighters = []
#     pairs = []
#     i, j = list(random.sample(range(len(participants)), 2))
#     pairs.append(
#         (
#             participants[i],
#             participants[j],
#         )
#     )
#     # # Remove used fighter instances or ids from fighters list
#     # for k in sorted([i, j], reverse=True):
#     #     del participants[k]
#     #
#     # # End loop if list is empty
#     #     if not participants:
#     #         break
#
#     # fighters = [Fighter(id=i) for i in range(1, 9)]
#
# # Show results
#     print(pairs)
#     print(("teraz"))
#     print(pairs[0])
#     # for p in participants:
#     #     if first_random_fighter not in random_opponents:
#     #         if random_opponent not in random_first_fighters:
#     #             if random_first_fighters not in random_first_fighters:
#     #                 if random_opponent not in random_opponents:
#     #                     if first_random_fighter != random_opponent:
#     #                         random_first_fighters.append(first_random_fighter)
#     #
#     #                        random_opponents.append(random_opponent)
#     participant_indexes = []
#     # for e in participants:
#     #     participant_indexes.append((e[i]))
#
#     # print(list(itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8], 2)))
#     print(itertools.combinations(participants, 2))
#     cos = (itertools.combinations(participants, 2))
#     # print(len(count))
#     # print(range(count))
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
#         "cos":cos,
#         "pairs": pairs
#     })
#

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
