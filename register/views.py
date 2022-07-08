from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            permission = Permission.objects.get(name="can add tag")
            user.user_premissions.add(permission)
        return redirect(reverse('main:home'))
    else:
        form = RegisterForm()
    return render(response, "accounts/register.html", {"form":form})


def home_view(request):
    return render(request, 'home.html')