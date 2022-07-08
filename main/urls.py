from django.urls import path
from main.views import home_view, contact, user_profile

app_name = "main"
urlpatterns = [
    path('', home_view, name = "home"),
    path('contact', contact, name="contact"),
    path('user/<int:user_id>/profile', user_profile, name="userprofile")
]