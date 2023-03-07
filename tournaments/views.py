from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournaments.models import Tournament, Organizer
from main.models import UserProfile
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournaments.forms import TournamentForm, OrganizerFormSet, TournamentDeleteForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def tournaments_list(request):
    tournaments = Tournament.objects.all().order_by('-created')
    paginator = Paginator(tournaments, 20)
    page_number = request.GET.get('page')
    tournaments_list = paginator.get_page(page_number)
    context = {'tournaments_list': tournaments_list}
    return render(request, "tournaments_list.html", context)


def tournament_details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    title = tournament.title
    description = tournament.description
    organizers = tournament.organizers.all()
    image = tournament.image
    posts = tournament.comments.all()
    user = tournament.user
    created = tournament.created
    participants = tournament.participants.all()
    groups = tournament.groups.all().order_by('number')
    galleries = tournament.galleries.all()
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "tournament_details.html", context={
        'title': title,
        'description': description,
        'organizers': organizers,
        "image": image,
        "posts": posts,
        "tournament_id": tournament_id,
        "user": user,
        "created": created,
        "participants": participants,
        "groups":groups,
        "galleries": galleries
    })


def add_tournament(request):
    if request.user.is_authenticated:
        formset = OrganizerFormSet(queryset=Organizer.objects.none())
        if request.method == "POST":
            form = TournamentForm(request.POST, request.FILES)
            formset = OrganizerFormSet(request.POST)
            form.instance.user = request.user
            if formset.is_valid():
                instance = form.save()
                for f in formset.cleaned_data:
                    if f:
                        orgaznier, _ = Organizer.objects.get_or_create(**f)
                        orgaznier.user = request.user
                        if orgaznier not in instance.organizers.all():
                            instance.organizers.add(orgaznier)
                instance.save()
            messages.success(request, 'turniej dodany')
            return HttpResponseRedirect(reverse("tournaments:tournaments_list"))
        else:
            form = TournamentForm()
        return(
            render(request, "add_tournament.html", {"form": form, "formset": formset })
        )
    else:
        return redirect(reverse('login'))


def edit_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if user == tournament.user:
                form = TournamentForm(request.POST, request.FILES, instance=tournament)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'turniej zmieniony')
                    return HttpResponseRedirect(reverse('tournaments:tournament_details', args=[tournament_id] ))
                else:
                    return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                form = TournamentForm(instance=tournament)
                return render(request,"edit_tournament.html", {"form": form})


def delete_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if user == tournament.user:
                tournament.delete()
                messages.warning(request, 'turniej usunięty')
                return HttpResponseRedirect(reverse('tournaments:tournaments_list' ))
            else:
                return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                return render( request,"delete_tournament.html", context={"tournament": tournament})

