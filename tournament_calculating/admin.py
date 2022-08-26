from django.contrib import admin
from .models import Participant, Group, Fight, Round


@admin.register(Participant)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["name", "school"]
    search_fields = ["name", "school"]
    list_filter = ["name", "school"]


@admin.register(Group)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["number", "tournament"]
    search_fields = ["number", "tournament"]
    list_filter = ["number", "tournament"]


@admin.register(Fight)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["group", "rounds", "tournament"]
    search_fields = ["group", "rounds", "tournament"]
    list_filter = ["group", "rounds", "tournament"]


@admin.register(Round)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["fight", "result"]
    search_fields = ["fight", "result"]
    list_filter = ["fight", "result"]