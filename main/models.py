from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return f"{self.user} {self.bio}"


    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"