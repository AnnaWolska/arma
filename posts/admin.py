from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title","created","modified","user", "get_title"]

    def get_title(self, obj):
        return obj.tournament.title

    get_title.short_description = 'Ttile'
    get_title.admin_order_field = 'tournament__title'

    search_fields = ["title","created","modified","user", "tournament"]
    list_filter = ["title", "tournament"]




