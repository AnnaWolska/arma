from django.contrib import admin
from .models import UserProfile


admin.site.site_header = "Arma Admin"
admin.site.site_title = "Tournaments Admin Portal"
admin.site.index_title = "Witaj w Portalu Tournaments"


# @admin.register(UserProfile)
# class ArmaAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "bio"]
#     search_fields = ["id", "user", "bio"]

