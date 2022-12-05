from django.contrib import admin
from .models import Participant, Group, Fight, Round


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "school"]

    search_fields = ["name", "school"]
    list_filter = ["name", "school"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "get_title"]

    def get_title(self, obj):
        return obj.tournament.title

    get_title.short_description = 'Ttile'
    get_title.admin_order_field = 'tournament__title'

    search_fields = ["id", "number"]
    list_filter = ["id", "number"]


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ["id", "get_number", "rounds", "get_name", "get_name2", "get_tournament_name"]

    def get_number(self, obj):
        return obj.group.number
    get_number.short_description = 'Group Nr'
    get_number.admin_order_field = 'group__number'

    def get_name(self, obj):
        return obj.fighter_one.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'fighter_one__name'

    def get_name2(self, obj):
        return obj.fighter_two.name
    get_name2.short_description = 'Name2'
    get_name2.admin_order_field = 'fighter_two__name'

    def get_tournament_name(self, obj):
        return obj.tournament.title
    get_tournament_name.short_description = 'Tournament Name'
    get_tournament_name.admin_order_field = 'tournament__title'

    search_fields = ["group", "rounds"]
    list_filter = ["group", "rounds"]




@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ["id", "fight", "result", "points","fighter"]

    search_fields = ["id", "fight", "result", "points","fighter"]
    list_filter = ["id", "fight", "result", "points"]