from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from galleries.models import Gallery, Photo
from django.core.paginator import Paginator
from galleries.form import GalleryForm, PhotoForm
from django.template import loader
from django.contrib.auth.models import AnonymousUser
from dal import autocomplete
from django.forms import modelformset_factory
from django.db.models import Count
from django.contrib import messages


def show_galleries_list(request):
    galleries = Gallery.objects.all()
    # galleries = Gallery.objects.filter(status=Status.PUBLISHED).annotate(
    #             p_count=Count('photos')
    #          ).filter(p_count__gt=0)
    # galleries = [g for g in galleries if g.photos.count() >0]

    paginator = Paginator(galleries, 8)
    page_number = request.GET.get('page')
    galleries_list = paginator.get_page(page_number)
    context = {'galleries_list': galleries_list}
    return render(request, "galleries/galleries.html", context)


def show_gallery_details(request, gallery_id):
    galleries = Gallery.objects.get(pk=gallery_id)
    id = galleries.id
    title = galleries.title
    description = galleries.description
    user = galleries.user
    created = galleries.created
    modified = galleries.modified
    photos = galleries.photos.all()
    if galleries.tournament is not None:
        tournament = galleries.tournament.title
    else:
        tournament = []
    tournament_id = galleries.tournament.id
    paginator = Paginator(photos, 8)
    page_number = request.GET.get('page')
    gallery_list = paginator.get_page(page_number)
    context = {
        'gallery_list': gallery_list,
        'galleries': galleries,
        'id': id,
        'title': title,
        'description': description,
        'user': user,
        'photos': photos,
        'created': created,
        'modified': modified,
        'tournament': tournament,
        'tournament_id':tournament_id,
        'gallery_id': gallery_id
    }
    return render(request, "galleries/gallery.html", context)


def add_gallery(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = GalleryForm(request.POST)
            if form.is_valid():
                gallery = form.save()
                gallery.user = request.user
                gallery.save()
                messages.success(request, 'galeria dodana')
                return HttpResponseRedirect(reverse("galleries:add_photo", args=[gallery.id]))
        else:
            form = GalleryForm()
        return(
            render(request, "galleries/add_gallery.html", {"form":form})
        )
    else:
        return redirect(reverse('login'))


def add_photo(request, gallery_id):

    if request.user.is_authenticated:
        gallery = Gallery.objects.get(pk=gallery_id)
        PhotosFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1)
        formset = PhotosFormSet(queryset=gallery.photos.none())

        if request.method == "POST":
            formset = PhotosFormSet(request.POST, request.FILES)
            if formset.is_valid():
                for f in formset.cleaned_data:
                    if f:
                        Photo.objects.create(gallery=gallery, **f)

                        instance = formset.save(commit=False)

            messages.success(request, 'zdjęcie dodane')
            return HttpResponseRedirect(reverse("galleries:add_photo", args=[gallery_id]))
        return render(
            request,
            "galleries/add_photo.html", {"formset": formset, 'gallery': gallery })


def delete_gallery(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if user == gallery.user:
                gallery.delete()
                messages.warning(request, 'galeria usunięta')
                return HttpResponseRedirect(reverse('galleries:galleries_list' ))
            else:
                return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                return render( request,"delete_gallery.html", context={"gallery": gallery})