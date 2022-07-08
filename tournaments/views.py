from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournaments.models import Tournament, Organizer
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser
# from tournamnets.forms import TournamentForm
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


# def add_book(request):
#     formset = AuthorFormSet(queryset=Author.objects.none())
#     if request.method == "POST":
#         form = BookForm(request.POST, request.FILES)
#         formset = AuthorFormSet(request.POST)
#         if formset.is_valid():
#             instance = form.save()
#             for f in formset.cleaned_data:
#                 if f:
#                     author, _ = Author.objects.get_or_create(**f)
#                     # if author not in instance.authors.all():
#                     #     instance.authors.add(author)
#             instance.save()
#         return HttpResponseRedirect(reverse("books:list"))
#     else:
#         form = BookForm()
#     return(
#         render(request, "add_book.html", {"form": form, "formset": formset})
#     )

def add_tournament(request):
    pass