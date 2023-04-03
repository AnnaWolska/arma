from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from datetime import datetime

# import cloudinary
# import cloudinary_storage
# from cloudinary import CloudinaryField
from cloudinary.models import CloudinaryField


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = ImageField(upload_to="organizers/logos/%Y/%m/%d/", blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1, related_name="organizers_created")

    def __str__(self):
        return f"{self.name} "

    class Meta:
        verbose_name = "Organizator"
        verbose_name_plural = "Organizatorzy"


class Tournament(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organizers = models.ManyToManyField('Organizer', related_name="tournaments")
    # image = ImageField(upload_to="tournaments/logos/%Y/%m/%d/", blank=True, null=True)
    image = CloudinaryField(upload_to="tournaments/logos/%Y/%m/%d/", blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="tournaments_created")
    created = models.DateTimeField(auto_now=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    tournament_average = models.FloatField(null=True)


    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.image}"

    class Meta:
        verbose_name = "Turniej"
        verbose_name_plural = "Turnieje"





