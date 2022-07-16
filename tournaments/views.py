from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournaments.models import Tournament, Organizer
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournaments.forms import TournamentForm, OrganizerFormSet
# from django.utils import timezone
from django.core.paginator import Paginator


def tournaments_list(request):
    tournaments = Tournament.objects.all()
    paginator = Paginator(tournaments, 10)
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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_list = paginator.get_page(page_number)
    return render(request, "tournament_details.html", context={
        'title': title,
        'description': description,
        'organizers': organizers,
        "image": image,
        "posts": posts,
        "posts_list": posts_list
    })


def add_tournament(request):
    if request.user.is_authenticated:
        formset = OrganizerFormSet(queryset=Organizer.objects.none())
        if request.method == "POST":
            form = TournamentForm(request.POST, request.FILES)
            formset = OrganizerFormSet(request.POST)
            if formset.is_valid():
                instance = form.save()
                for f in formset.cleaned_data:
                    if f:
                        orgaznier, _ = Organizer.objects.get_or_create(**f)
                        if orgaznier not in instance.organizers.all():
                            instance.organizers.add(orgaznier)
                instance.save()
            return HttpResponseRedirect(reverse("tournaments:tournaments_list"))
        else:
            form = TournamentForm()
        return(
            render(request, "add_tournament.html", {"form": form, "formset": formset })
        )
    else:
        return redirect(reverse('login'))


def delete_tournament(request, tournament_id):
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            tournament = Tournament.objects.get(pk=tournament_id)
            tournament.delete()
            return HttpResponseRedirect(reverse("tournaments:tournaments_list"))




# def add_tournament(request):
#
#     if request.method == "POST":
#         form = TournamentForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             instance = form.save()
#
#             instance.save()
#         return HttpResponseRedirect(reverse("tournaments:tournaments_list"))
#     else:
#         form = TournamentForm()
#     return(
#         render(request, "add_tournament.html", {"form": form})
#     )