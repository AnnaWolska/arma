from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.description})"

    class Meta:
        verbose_name = "Organizator"
        verbose_name_plural = "organizatorzy"


class Tournament(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organizers = models.ManyToManyField('Organizer', related_name="tournaments")
    image = ImageField(upload_to="tournaments/logos/%Y/%m/%d/", blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1, related_name="tournaments_created")

    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.image}"

    class Meta:
        verbose_name = "Turniej"
        verbose_name_plural = "Turnieje"





