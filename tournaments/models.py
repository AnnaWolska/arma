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
    organizer = models.ForeignKey("Organizer", on_delete=models.CASCADE, related_name="organized_tournaments", null=True, blank=True)
    image = ImageField(upload_to="tournaments/logos/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.title} {self.description} {self.organizer} {self.image}"

    class Meta:
        verbose_name = "Turniej"
        verbose_name_plural = "Turnieje"





