from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournaments.models import Tournament, Organizer
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournaments.forms import TournamentForm, OrganizerFormSet, TournamentDeleteForm
# from django.utils import timezone
from django.core.paginator import Paginator


def tournaments_list(request):
    tournaments = Tournament.objects.all()
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
        "user": user
    })


# def add_tournament(request):
#     if request.user.is_authenticated:
#         formset = OrganizerFormSet(queryset=Organizer.objects.none())
#         if request.method == "POST":
#             form = TournamentForm(request.POST, request.FILES)
#             formset = OrganizerFormSet(request.POST)
#             if formset.is_valid():
#
#                 instance = form.save()
#                 instance.user = request.user
#                 instance.save()
#                 for f in formset.cleaned_data:
#                     if f:
#                         orgaznier, _ = Organizer.objects.get_or_create(**f)
#                         if orgaznier not in instance.organizers.all():
#                             instance.organizers.add(orgaznier)
#                 instance.save()
#             return HttpResponseRedirect(reverse("tournaments:tournaments_list"))
#         else:
#             form = TournamentForm()
#         return(
#             render(request, "add_tournament.html", {"form": form, "formset": formset })
#         )
#     else:
#         return redirect(reverse('login'))


def add_tournament(request):
    # user = request.user
    if request.user.is_authenticated:
        formset = OrganizerFormSet(queryset=Organizer.objects.none())
        if request.method == "POST":
            # if user == post.user:
            form = TournamentForm(request.POST, request.FILES)
            formset = OrganizerFormSet(request.POST)
            if formset.is_valid():

                instance = form.save()
                instance.user = request.user
                # instance.user = request.user
                instance.save()
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

#
# def edit_post(request, post_id):
#     user = request.user
#     posts = user.posts.all()
#     for post in posts:
#         if request.method == "POST":
#             if user.is_authenticated:
#                 if user == post.user:
#                     form = PostForm(request.POST, request.FILES, instance=post)
#                     if form.is_valid():
#                         form.save()
#                         return HttpResponseRedirect(reverse("posts:list"))
#                     else:
#                         return redirect(reverse('login'))
#     else:
#         if user.is_authenticated:
#             if user == request.user:
#                 form = PostForm(instance=post)
#                 return render( request,"posts/edit.html", {"form": form})






# def delete_tournament(request, tournament_id):
#     user = request.user
#     if request.method == "POST":
#         if user.is_authenticated:
#             form = TournamentDeleteForm(request.POST)
#             if form.is_valid():
#                 tournament = Tournament.objects.get(pk=tournament_id)
#                 tournament.delete()
#             # return HttpResponseRedirect(reverse("tournaments:delete_tournament"))
#             return(
#                 render(request, "delete_tournament.html", {"form": form})
#             )
#     else:
#         form = TournamentForm()


# def delete_tournament(request, tournament_id):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             # form = TournamentDeleteForm(request.POST)
#             # if form.is_valid():
#             # tournament = Tournament.objects.get(pk=tournament_id)
#             # tournament.delete()
#             # return HttpResponseRedirect(reverse("tournaments:delete_tournament"))
#         # else:
#         #     form = TournamentDeleteForm()
#             return(
#                 # render(request, "delete_tournament.html", {"form": form})
#                 render(request, "delete_tournament.html", {"tournament_id": tournament_id})
#             )
#     else:
#         return redirect(reverse('login'))
#
#
# def delete_post(request, id):
#     del_post = get_object_or_404(Post, id=id)
#     del_post.delete(Post, id=id)
#     return render(request, 'account/delete-post.html', {'del_post': del_post})


def delete_tournament(request, tournament_id):
    if request.user.is_authenticated:
        del_tournament = get_object_or_404(Tournament, id=tournament_id)
        del_tournament.delete()
        # if not del_tournament is None:
        # if request.method == "POST":
        return render(request, 'delete_tournament.html', {'del_tournament': del_tournament})

        # # else:
        # #     return redirect(reverse('tournaments:tournaments_list'))
        # return redirect(reverse('tournaments:tournaments_list'))