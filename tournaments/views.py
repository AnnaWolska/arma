from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournaments.models import Tournament, Organizer
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from tournamnets.forms import TournamentForm, OrganizerForm
# from django.utils import timezone
from django.core.paginator import Paginator


def tournaments_list(request):
    tournaments = Tournament.objects.all()
    paginator = Paginator(tournaments, 10)
    page_number = request.GET.get('page')
    tournaments_list = paginator.get_page(page_number)
    context = {'tournaments' : tournaments}
    return render(request, "tournaments_list.html", context)


def tournament_details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    title = tournament.title
    description = tournament.description
    organizer = tournament.organizer
    image = tournament.image
    # form = BookBorrowForm()
    # form.helper.form_action = reverse("books:borrows", args=[book.id])
    return render(request, "tournament_details.html", context = {
        'title' : title,
        'description': description,
        'organizer' : organizer,
        "image":image,
    })


def add_tournament(request):
    formset = OrganizerForm(queryset=Organizer.objects.none())
    if request.method == "POST":
        form = TournamentForm(request.POST, request.FILES)
        formset = OrganizerForm(request.POST)
        if formset.is_valid():
            instance = form.save()
            for f in formset.cleaned_data:
                if f:
                    orgaznier, _ = Organizer.objects.get_or_create(**f)
                    # if author not in instance.authors.all():
                    #     instance.authors.add(author)
            instance.save()
        return HttpResponseRedirect(reverse("tournaments:tournaments_list"))
    else:
        form = TournamentForm()
    return(
        render(request, "add_tournament.html", {"form": form, "formset": formset})
    )

