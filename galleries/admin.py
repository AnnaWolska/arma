from django.contrib import admin
from django.db.models import Count
from import_export import resources
from import_export.admin import ExportMixin
from . import models
from .models import Gallery, Photo
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            t = get_thumbnail(value, "150")
            output.append(f'<a href="{value.url}" target="_blank"><img src="{t.url}"></a>')
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return ''.join(output)


class PhotoInLine(admin.StackedInline):
    model = Photo
    fields = ['title', 'short_description', 'image']
    extra = 1
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }


class GalleryResource(resources.ModelResource):
    class Meta:
        model = Gallery


class HasPhotosFilter(admin.SimpleListFilter):
    title = "Ilość zdjęć"
    parameter_name = 'photos_count'

    def lookups(self, request, model_admin):
        return (
            ('Yes', "Yes"),
            ('No', 'No')
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(_photos_count__gt=0)
        elif value == 'No':
            return queryset.filter(_photos_count=0)
        return queryset


@admin.register(Gallery)
class GalleryAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ["id","title","photos_count","description","created","modified","user","tournament"]
    fieldsets = (
        ('', {
            'fields': ('title',),
        }),
        ('Opis', {
            'fields': ('description',),
            'description': "Napisz parę słów o tej galerii"
        }),

    )
    search_fields = ["title","description","created","modified","user"]
    list_filter = [HasPhotosFilter]
    resource_class = GalleryResource
    inlines = (PhotoInLine,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _photos_count=Count('photos')
        )
        return queryset

    def photos_count(self, obj):
        return obj.photos.count()

    photos_count.admin_order_field = "_photos_count"
    photos_count.short_description = "Ilość zdjęć"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ["title", "short_description", "created", "modified", "gallery"]
    search_fields = ["title", "short_description", "created", "modified", "gallery"]
    list_filter = ["title", "short_description", "created", "modified", "gallery"]



