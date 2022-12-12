from django.contrib import admin
# from import_export import resources
# from import_export.admin import ExportMixin
from .models import Post

#
# class PostResource(resources.ModelResource):
#     class Meta:
#         model = Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title","created","modified","user", "get_title"]

    def get_title(self, obj):
        return obj.tournament.title

    get_title.short_description = 'Ttile'
    get_title.admin_order_field = 'tournament__title'

    search_fields = ["title","created","modified","user", "tournament"]
    list_filter = ["title", "tournament"]




