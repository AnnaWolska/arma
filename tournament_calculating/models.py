from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from tournaments.models import Tournament


class Participant(models.Model):
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=500)
    image = ImageField(upload_to="tournament_calculating/images/%Y/%m/%d/", blank=True, null=True)
    tournaments = models.ManyToManyField('tournaments.Tournament', related_name='participants')
    group_points = models.PositiveSmallIntegerField(null=True, default=0)
    points_average = models.PositiveSmallIntegerField(null=True, default=0)
    # fights = models.ForeignKey("Fight", related_name=)

    def __str__(self):
        return f"{self.name} {self.school} {self.image} {self.tournaments} {self.group_points}  {self.points_average}"

    class Meta:
        verbose_name = "Zawodnik"
        verbose_name_plural = "Zawodnicy"


class Group(models.Model):
    COLOR = (
        ('lemonchiffon','żółty' ),
        ('lightgreen', 'zielony'),
        ('powderblue', 'niebieski'),
        ('coral','czerwony' ),
        ('darkorange', 'pomarańczowy'),
        ('thistle', 'fioletowy'),
        ('darkblue', 'granatowy'),
        ('darkslategray', 'czarny'),
        ('floralwhite', 'biały'),
        ('peru', 'brązowy'),
        ('pink','różowy' ),
        ('darkgrey','szary' )
    )
    number = models.PositiveSmallIntegerField(null=False)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="groups")
    participants = models.ManyToManyField('Participant', related_name='groups')
    color_fighter_one = models.CharField(max_length=30, choices=COLOR, null=True)
    color_fighter_two = models.CharField(max_length=30, choices=COLOR, null=True)


    def __str__(self):
        return f"{self.number} {self.tournament} {self.participants} {self.color_fighter_one} {self.color_fighter_two}"

    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "Grupy"


class Fight(models.Model):
    order = models.PositiveSmallIntegerField(null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="fights", null=True)
    rounds = models.PositiveSmallIntegerField(null=True)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="fights", null=True)
    fighter_one = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_one", null=True )
    fighter_two = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_two", null=True )
    fighter_one_points = models.PositiveSmallIntegerField(null=True, default=0)
    fighter_two_points = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.group} {self.rounds} {self.tournament} {self.fighter_one} {self.fighter_two}"

    class Meta:
        verbose_name = "Walka"
        verbose_name_plural = "Walki"


class Round(models.Model):
    STATUS = (
        ('0', 'win'),
        ('1', 'lose'),
        ('2', 'draw'),
        ('3', 'no result'),
        ('4', 'no fight'),
        ('5', 'no status')
    )
    order = models.PositiveSmallIntegerField(null=True)
    fight = models.ForeignKey("Fight", on_delete=models.CASCADE, related_name="rounds_of_fight", null=True)
    result_figter_one = models.CharField(max_length=1, choices=STATUS, null=True)
    result_figter_two = models.CharField(max_length=1, choices=STATUS, null=True)
    points_fighter_one = models.PositiveSmallIntegerField(null=True)
    points_fighter_two = models.PositiveSmallIntegerField(null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="rounds_of_group", null=True)
    fighter = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="rounds_of_participant", null=True )

    def __str__(self):
        return f"{self.order} {self.fight} {self.result_figter_one} {self.result_figter_two} \
        {self.group} {self.fighter} {self.points_fighter_one} {self.points_fighter_two}"

    class Meta:
        verbose_name = "Runda"
        verbose_name_plural = "Rundy"

