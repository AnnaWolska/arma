from django.contrib import admin
from .models import Tournament, Organizer


@admin.register(Tournament)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "organizer"]
    search_fields = ["title", "organizer"]
    list_filter = ["title", "organizer"]


@admin.register(Organizer)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]
