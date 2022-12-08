from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from sorl.thumbnail import ImageField
from posts.models import Timestamped
import string
from random import random
from django.db import models
from django.utils.text import slugify
# from tinymce import models as tinymce_models


# def get_random_text(n):
#     letters = string.ascii_letters
#     return ''.join(random.choice(letters) for i in range(n))
# class Status(models.TextChoices):
#     NEW = 'new', 'new'
#     HIDE = 'hide', 'hide'
#     PUBLISHED = 'published', 'published'


class Gallery(Timestamped):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default="1", related_name="galleries")
    # slug = models.SlugField(unique=True, max_length=100)
    # description = tinymce_models.HTMLField(null=True, blank=True)
    # status = models.CharField(default=Status.NEW, max_length=10, choices=Status.choices)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerie"

    # def save(self, *args, **kwargs):
    #     if self.status == Status.HIDE:
    #         self.photos.update(status=Status.HIDE)
    #     if self._state.adding and not self.slug:
    #         slug = slugify(self.title)
    #         slugs = self.__class__.objects.values_list('slug', flat=True)
    #         if slugs:
    #             while True:
    #                 if slug in slugs:
    #                     slug+= get_random_text(5)
    #                 else:
    #                     break
    #         self.slug = slug
    #     return super().save(*args, **kwargs)


def upload_to(instance, filename):
    return f"galleries/{instance.gallery.slug}/{filename}"


@property
def photos_count(self):
    return self.photos.count()


class Photo(Timestamped):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return f"{self.title} {self.short_description} {self.image} {self.gallery}"
    # slug = models.SlugField(unique=True, max_length=100)
    # source = models.CharField(max_length=255, null=True, blank=True)
    # status = models.CharField(default=Status.NEW, max_length=10, choices=Status.choices)
    #
    # @property
    # def is_published(self):
    #     return self.status == Status.PUBLISHED
    #
    # def __str__(self):
    #     return self.slug

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"