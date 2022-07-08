from django.contrib import admin
from .models import UserProfile


admin.site.site_header = "Tournaments Admin"
admin.site.site_title = "Tournaments Admin Portal"
admin.site.index_title = "Witaj w Portalu Tournaments"


@admin.register(UserProfile)
class BooksAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "bio"]
    search_fields = ["id", "user", "bio"]

