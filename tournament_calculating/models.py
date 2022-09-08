from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from tournaments.models import Tournament


class Participant(models.Model):
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=500)
    image = ImageField(upload_to="tournament_calculating/images/%Y/%m/%d/", blank=True, null=True)
    tournaments = models.ManyToManyField('tournaments.Tournament', related_name='participants')

    def __str__(self):
        return f"{self.name} {self.school} {self.image} {self.tournaments}"

    class Meta:
        verbose_name = "Zawodnik"
        verbose_name_plural = "Zawodnicy"


class Group(models.Model):
    number = models.PositiveSmallIntegerField(null=False)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="groups")
    participants = models.ManyToManyField('Participant', related_name='groups')


    def __str__(self):
        return f"{self.number} {self.tournament} {self.participants}"

    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "Grupy"


class Fight(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="fights", null=True)
    rounds = models.PositiveSmallIntegerField(null=True)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="fights", null=True)
    fighter_one = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_one", null=True )
    fighter_two = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_two", null=True )

    def __str__(self):
        return f"{self.group} {self.rounds} {self.fighter_one} {self.fighter_two}"

    class Meta:
        verbose_name = "Walka"
        verbose_name_plural = "Walki"


class Round(models.Model):
    POINTS = (
        ('a', '3'),
        ('b', '4'),
        ('c', '5'),
        ('d', 'remis'),
        ('e', '0')
    )

    fight = models.ForeignKey("Fight", on_delete=models.CASCADE, related_name="rounds_of_fight")
    result = models.CharField(max_length=1, choices=POINTS, null=True)

    def __str__(self):
        return f"{self.fight} {self.result}"

    class Meta:
        verbose_name = "Runda"
        verbose_name_plural = "Rundy"






    ## class FightersPairs(models.Model):
    # class Fighters_pair(models.Model):
    #     fighter_one = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_one", default=[0])
    #     fighter_two = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_two", default=[0])
    #
    #     def __str__(self):
    #         return f" {self.fighter_one } {self.fighter_two }"
    #
    #     class Meta:
    #         verbose_name = "Walka"
    #         verbose_name_plural = "Walki"
