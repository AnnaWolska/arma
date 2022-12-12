from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from posts.models import Post
from tournaments.models import Tournament
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from posts.forms import PostForm, PostDeleteForm
from dal import autocomplete
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def posts_list(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    posts = Post.objects.filter(pk=tournament_id).order_by('id')
    # posts = Post.objects.get_queryset().filter(pk=tournament_id).order_by('id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_list = paginator.get_page(page_number)
    context = {'posts_list': posts_list}
    return render(request, "posts_list.html", context)


def post_details(request, post_id):
    posts = Post.objects.get(pk=post_id)
    id = posts.id
    title = posts.title
    content = posts.content
    user = posts.user
    exemple_file = posts.exemple_file
    image = posts.image
    created = posts.created
    modified = posts.modified
    return render(request, "post_details.html", context={
        'id' : id,
        'title' : title,
        'content': content,
        'user' : user,
        'exemple_file' : exemple_file,
        'image' : image,
        'created':created,
        'modified':modified
    })


def add_post(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)

    if request.user.is_authenticated:
        if request.method == "POST":
            tournament = Tournament.objects.get(pk=tournament_id)
            form = PostForm(request.POST, request.FILES)
            form.user = request.user
            form.tournament = tournament.id

            if form.is_valid():

                instance = form.save(commit=False)
                instance.user = request.user
                instance.tournament_id =tournament_id
                # instance.image = request.FILES
                instance.save()
                form.save_m2m()
            return HttpResponseRedirect(reverse('tournaments:tournament_details', args=[tournament_id]))
        else:
            form = PostForm()
        return(
            render(request, "add_post.html", {"form": form})
        )
    else:
        return redirect(reverse('login'))


def edit_post(request, post_id, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    post = Post.objects.get(pk=post_id)
    post.tournament = tournament
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if user == post.user:
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    form.save()

                    return HttpResponseRedirect(reverse('tournaments:tournament_details', args=[tournament_id]))
                else:
                    return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                form = PostForm(instance=post)
                return render(request, "edit_post.html", {"form": form})


def delete_post(request, tournament_id, post_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    post = Post.objects.get(pk=post_id)
    user = request.user
    posts = user.posts.all()
    for post in posts:
        if request.method == "POST":
            if user.is_authenticated:
                if user == post.user:
                    post.delete()
                    return HttpResponseRedirect(reverse('tournaments:tournament_details', args=[tournament_id] ))
                else:
                    return redirect(reverse('login'))
    else:
        if user.is_authenticated:
            if user == request.user:
                return render( request,"delete_post.html", context={"post":post})
