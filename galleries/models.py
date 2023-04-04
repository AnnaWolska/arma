from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Tournament
from django.utils.timezone import now, timedelta
from sorl.thumbnail import ImageField
from posts.models import Timestamped
import string
from random import random
from django.db import models
# from django.utils.text import slugify


class Gallery(Timestamped):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default="1", related_name="galleries")
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="galleries", null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerie"


def upload_to(instance, filename):
    return f"galleries/{filename}"


@property
def photos_count(self):
    return self.photos.count()


class Photo(Timestamped):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    # image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image = CloudinaryField(blank=True, null=True)
    gallery = models.ForeignKey("Gallery",on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return f"{self.title} {self.short_description} {self.image} {self.gallery}"


    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"