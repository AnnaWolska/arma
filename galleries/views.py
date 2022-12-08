from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from galleries.models import Status, Gallery, Photo
from django.core.paginator import Paginator
from galleries.form import GalleryForm, PhotoForm
from django.template import loader
from django.contrib.auth.models import AnonymousUser
from dal import autocomplete
from django.forms import modelformset_factory
from django.db.models import Count


def show_galleries_list(request):
    # galleries = Gallery.objects.filter(status=Status.PUBLISHED)
    galleries = Gallery.objects.filter(status=Status.PUBLISHED).annotate(
                p_count=Count('photos')
             ).filter(p_count__gt=0)

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
        'modified': modified
    }
    return render(request, "galleries/gallery.html", context)


def add_gallery(request):
    if request.method == "POST":
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save()
            gallery.user = request.user
            gallery.save()
            return HttpResponseRedirect(reverse("galleries:add_photo", args=[gallery.id]))
    else:
        form = GalleryForm()
    return(
        render(request, "galleries/add_gallery.html", {"form":form})
    )


def add_photo(request, gallery_id):

    if request.user.is_authenticated:
        # gallery = get_object_or_404(Gallery, pk=gallery_id)
        gallery = Gallery.objects.get(pk=gallery_id)
        # form = PhotoForm()
        PhotosFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1)
        formset = PhotosFormSet(queryset=gallery.photos.none())
        # context = {
        #     "gallery": gallery,
        # }
        if request.method == "POST":
            # form = PhotoForm(request.POST, request.FILES)
            formset = PhotosFormSet(request.POST, request.FILES)
            if formset.is_valid():
                for f in formset.cleaned_data:
                    if f:
                        Photo.objects.create(gallery=gallery, **f)
                        instance = formset.save(commit=False)
                        # instance.gallery = gallery
                        # instance.save()
            return HttpResponseRedirect(reverse("galleries:add_photo", args=[gallery_id]))
        return render(
            request,
            "galleries/add_photo.html", {"formset": formset, 'gallery': gallery })
