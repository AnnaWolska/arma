from django.contrib import admin
from .models import Participant, Group, Fight, Round


@admin.register(Participant)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "school"]

    # def get_group(self, obj):
    #     return obj.group.number
    #
    # get_number.short_description = 'Number'
    # get_number.admin_order_field = 'group__number'

    search_fields = ["name", "school"]
    list_filter = ["name", "school"]


@admin.register(Group)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "get_title"]

    def get_title(self, obj):
        return obj.tournament.title

    get_title.short_description = 'Ttile'
    get_title.admin_order_field = 'tournament__title'

    search_fields = ["id", "number"]
    list_filter = ["id", "number"]


@admin.register(Fight)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "get_number", "rounds"]
    # @display(ordering='group__number', description='Number')
    # def get_number(self, obj):
    #     return obj.group.number

    def get_number(self, obj):
        return obj.group.number

    get_number.short_description = 'Number'
    get_number.admin_order_field = 'group__number'

    # def get_name(self, obj):
    #     return obj.fighter_one.name
    #
    # get_name.short_description = 'Name'
    # get_name.admin_order_field = 'fighter_one__name'
    #
    # def get_name2(self, obj):
    #     return obj.fighter_two.name
    #
    # get_name2.short_description = 'Name'
    # get_name2.admin_order_field = 'fighter_two__name'

    search_fields = ["group", "rounds"]
    list_filter = ["group", "rounds"]


@admin.register(Round)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["id", "result"]

    # def get_number(self, obj):
    #     return obj.tournament.title
    #
    # get_title.short_description = 'Ttile'
    # get_title.admin_order_field = 'tournament__title'
    search_fields = ["id", "result"]
    list_filter = ["id", "result"]