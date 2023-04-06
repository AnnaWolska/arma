from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now,timedelta
from sorl.thumbnail import ImageField
from tournaments.models import Tournament
from cloudinary.models import CloudinaryField



class CheckAgeMixin:
    def is_older_than_n_days(self, n=1):
        delta = timedelta(days=n)
        return now() - self.created > delta


class Timestamped(models.Model, CheckAgeMixin):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(Timestamped):
    title = models.CharField(verbose_name="Tytuł", max_length=255)
    content = models.TextField(verbose_name="Treść")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="posts")
    exemple_file = models.FileField(upload_to='posts/examples', blank=True, null=True)
    image = ImageField(upload_to="posts/images/%Y/%m/%d/", blank=True, null=True)
    # image = CloudinaryField(blank=True, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="comments",  blank=True, null=True)

    def __str__(self):
        return f"{self.title} {self.content} {self.user} {self.exemple_file} {self.image}"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"

