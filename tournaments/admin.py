from django.contrib import admin
from .models import Tournament, Organizer


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description"]
    search_fields = ["title"]
    list_filter = ["title"]


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["name"]
