from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournament_calculating.models import Group, Fight, Round, Participant
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournament_calculating.forms import AddParticipantForm
# from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


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


def add_participant(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            form = AddParticipantForm(request.POST, request.FILES)

            form.user = request.user
            if form.is_valid():
                instance = form.save()
                # instance.user.id = request.user
                # instance.user = request.user
                instance.save()
                # for f in form.cleaned_data:
                #     if f:
                #         orgaznier, _ = Organizer.objects.get_or_create(**f)
                #         orgaznier.user = request.user
                #         if orgaznier not in instance.organizers.all():
                #             instance.organizers.add(orgaznier)
                # instance.save()
            return HttpResponseRedirect(reverse("tournament_calculating:participants_list"))
        else:
            form = AddParticipantForm
        return (
            render(request, "add_participant.html", {"form": form})
        )
    else:
        return redirect(reverse('login'))


def tournament_calculate(request):
    pass
    # if request.user.is_authenticated:
    #     if request.method == "POST":
    #         form = TournamentForm(request.POST, request.FILES)
    #         formset = OrganizerFormSet(request.POST)
    #         form.user = request.user
    #         if formset.is_valid():
    #             instance = form.save()
    #             # instance.user.id = request.user
    #             instance.user = request.user
    #             instance.save()
    #             for f in formset.cleaned_data:
    #                 if f:
    #                     orgaznier, _ = Organizer.objects.get_or_create(**f)
    #                     orgaznier.user = request.user
    #                     if orgaznier not in instance.organizers.all():
    #                         instance.organizers.add(orgaznier)
    #             instance.save()
    #         return HttpResponseRedirect(reverse("tournaments:tournaments_list"))
    #     else:
    #         form = TournamentForm()
    #     return(
    #         render(request, "add_tournament.html", {"form": form, "formset": formset })
    #     )
    # else:
    #     return redirect(reverse('login'))
