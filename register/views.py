# from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm
from main.models import UserProfile
from django.contrib.auth.models import User


# def register(response):
#     users = UserProfile.objects.all()
#     if response.method == "POST":
#         form = RegisterForm(response.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#             users.create(instance=instance)

def register(response):
    users = User.objects.all()
    if response.method == "POST":
        form = RegisterForm(response.POST)
        # username = form.username
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.username = username
            instance.save()
            # users.create(instance)
            print(instance)
            # users.create(username=username)



        messages.success(response, 'zarejestrowany nowy użytkownik')
        return redirect(reverse('main:home'))

    else:
        form = RegisterForm()
    return render(response, "accounts/register.html", {"form":form})


def home_view(request):
    return render(request, 'home.html')