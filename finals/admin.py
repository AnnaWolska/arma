from django.contrib import admin
from .models import Finalist, Stage, FinalFight, FinalRound, Winner


@admin.register(Finalist)
class FinalistAdmin(admin.ModelAdmin):
    list_display = ["final_points", "final_points_average", "group"]
    search_fields = [ "group"]
    list_filter = [ "group"]


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ["number","color_fighter_one", "color_fighter_two", "number_outgoing"]
    # search_fields = ["", ""]
    # list_filter = ["", ""]

@admin.register(FinalFight)
class FinalFightAdmin(admin.ModelAdmin):
    list_display = ["order", "stage", "rounds","final_fighter_one", "final_fighter_two", "tournament","final_fighter_one_points", "final_fighter_two_points", "resolved"]
    # search_fields = ["", ""]
    # list_filter = ["", ""]


@admin.register(FinalRound)
class FinalRoundAdmin(admin.ModelAdmin):
    list_display = ["order", "final_fight", "final_points_fighter_one","final_points_fighter_two", "stage", "final_fighter_one","final_fighter_two" ]
    # search_fields = ["", ""]
    # list_filter = ["", ""]


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ["tournament", "medal"]
    # search_fields = ["", ""]
    # list_filter = ["", ""]


