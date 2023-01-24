from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from tournaments.models import Tournament
# from finals.models import Finalist

#dodać relację do user
class Participant(models.Model):
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=500)
    image = ImageField(upload_to="tournament_calculating/images/%Y/%m/%d/", blank=True, null=True)
    tournaments = models.ManyToManyField('tournaments.Tournament', related_name='participants')
    # participant_finals = models.ManyToManyField('finals.Finalist', related_name='participants')
    group_points = models.PositiveSmallIntegerField(null=True, default=0)
    points_average = models.FloatField(null=True, default=0)
    round_average = models.FloatField(null=True, default=0)
    amount_rounds = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.name} {self.school} {self.image} {self.tournaments} " \
               f" {self.group_points}  {self.points_average} {self.round_average} " \
               f"{self.amount_rounds} " \
               # f"{self.participant_finals}"

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
    NUMBER = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    GR_NUMBER = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    number = models.PositiveSmallIntegerField( choices=GR_NUMBER, null=False, default=0)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="groups")
    participants = models.ManyToManyField('Participant', related_name='groups')
    color_fighter_one = models.CharField(max_length=30, choices=COLOR, null=True)
    color_fighter_two = models.CharField(max_length=30, choices=COLOR, null=True)
    number_outgoing = models.CharField(max_length=2, choices=NUMBER, null=True, default=0)
    # outgoings =

    def __str__(self):
        return f"{self.number} {self.tournament} {self.participants} {self.color_fighter_one} {self.color_fighter_two}"

    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "Grupy"


class Fight(models.Model):
    ROUNDS_NUMBER = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    order = models.PositiveSmallIntegerField(null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="fights", null=True)
    # rounds = models.PositiveSmallIntegerField(null=True)
    rounds = models.PositiveSmallIntegerField(choices=ROUNDS_NUMBER, null=False, default=0)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="fights", null=True)
    fighter_one = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_one", null=True )
    fighter_two = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="fighters_two", null=True )
    fighter_one_points = models.PositiveSmallIntegerField(null=True, default=0)
    fighter_two_points = models.PositiveSmallIntegerField(null=True, default=0)
    resolved = models.BooleanField(default=False , null=True)

    def __str__(self):
        return f"{self.group} {self.rounds} {self.tournament} {self.fighter_one} {self.fighter_two}"

    class Meta:
        verbose_name = "Walka"
        verbose_name_plural = "Walki"


class Round(models.Model):
    STATUS = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        # ('0 dubl', "0 dubl"),
        ('kontuzja', 'kontuzja'),
        ('dyskwalifikacja', 'dyskwalifikacja'),
        ('poddanie', 'poddanie'),
        ('wycofanie', 'wycofanie'),
        ('średnia', 'średnia'),
    )
    order = models.PositiveSmallIntegerField(null=True)
    fight = models.ForeignKey("Fight", on_delete=models.CASCADE, related_name="rounds_of_fight", null=True)
    # result_fighter_one = models.CharField(max_length=1, choices=STATUS, null=True)
    # result_fighter_two = models.CharField(max_length=1, choices=STATUS, null=True)
    # points_fighter_one = models.PositiveSmallIntegerField(null=True)
    # points_fighter_two = models.PositiveSmallIntegerField(null=True)
    points_fighter_one = models.CharField(max_length=20, choices=STATUS, null=True)
    points_fighter_two = models.CharField(max_length=20, choices=STATUS, null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="rounds_of_group", null=True)
    fighter_one = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="rounds_of_participant_one", null=True )
    fighter_two = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="rounds_of_participant_two", null=True )
    # numberfield , postsave
    # resolved_fighter_one = models.BooleanField(default=False, null=True)
    # resolved_fighter_two = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.order} {self.fight} \
        {self.group} {self.fighter_one} {self.fighter_one} {self.points_fighter_one} {self.points_fighter_two}"

    class Meta:
        verbose_name = "Runda"
        verbose_name_plural = "Rundy"





