from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from tournaments.models import Organizer
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from tournaments.forms import TournamentForm, OrganizerFormSet, TournamentDeleteForm
from organizers.forms import OrganizerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def organizers_list(request):
    organizers = Organizer.objects.all().order_by('name')
    paginator = Paginator(organizers, 20)
    page_number = request.GET.get('page')
    organizers_register = paginator.get_page(page_number)
    context = {'organizers_list': organizers_register}
    return render(request, "organizers_list.html", context)


def add_organizer(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            form = OrganizerForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save()
                instance.user = request.user
                instance.save()
                messages.success(request, 'organizator dodany')
            return HttpResponseRedirect(reverse("organizers:organizers_list"))
        else:
            form = OrganizerForm()
        return(
            render(request, "add_organizer.html", {"form": form})
        )
    else:
        return redirect(reverse('login'))


def delete_organizer(request, organizer_id):
    organizer = Organizer.objects.get(pk=organizer_id)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if user == organizer.user:
                organizer.delete()
                messages.warning(request, 'organizator usunięty')
                return HttpResponseRedirect(reverse('organizers:organizers_list'))
            else:
                return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                return render(request, "delete_organizer.html", context={"organizer": organizer})


def organizer_details(request, organizer_id):
    organizer = Organizer.objects.get(pk=organizer_id)
    name = organizer.name
    description = organizer.description
    image = organizer.image
    user = organizer.user
    return render(request, "organizer_details.html", context={
        'name': name,
        'description': description,
        "image": image,
        "organizer_id": organizer_id,
        "user": user
    })


def edit_organizer(request, organizer_id):
    organizer = Organizer.objects.get(pk=organizer_id)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if user == organizer.user:
                form = OrganizerForm(request.POST, request.FILES, instance=organizer)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'organizator zmieniony')
                    return HttpResponseRedirect(reverse(
                        'organizers:organizer_details',
                        args=[organizer_id])
                    )
                else:
                    return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                form = OrganizerForm(instance=organizer)
                return render(request,"edit_organizer.html", {"form": form})