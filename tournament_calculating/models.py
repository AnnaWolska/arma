from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from tournaments.models import Tournament


class Participant(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="participants")
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=500)
    image = ImageField(upload_to="tournament_calculating/images/%Y/%m/%d/", blank=True, null=True)
    tournaments = models.ManyToManyField('tournaments.Tournament', related_name='participants')
    group_points = models.PositiveSmallIntegerField(null=True, default=0)
    points_average = models.FloatField(null=True, default=0)
    round_average = models.FloatField(null=True, default=0)
    amount_rounds = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_points = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_average = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_wins = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_losses = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_doubles = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_hands = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_disqualifications = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_injuries = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_surrenders = models.PositiveSmallIntegerField(null=True, default=0)
    tournaments_opponent_injuries = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.name}"
         # {self.school} " \
        #        f"{self.image} {self.tournaments} " \
        #        f" {self.group_points}  {self.points_average} {self.round_average} " \
        #        f"{self.amount_rounds} " \
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
    color_fighter_one = models.CharField(max_length=30, choices=COLOR, null=True)
    color_fighter_two = models.CharField(max_length=30, choices=COLOR, null=True)
    number_outgoing = models.CharField(max_length=2, choices=NUMBER, null=True, default=0)
    participants = models.ManyToManyField('Participant', through='ParticipantGroup')

    def __str__(self):
        return f"{self.number} {self.tournament}  {self.color_fighter_one} {self.color_fighter_two}"

    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "Grupy"


class ParticipantGroup(models.Model):
    participant = models.ForeignKey("Participant",on_delete=models.CASCADE, null=True)
    group = models.ForeignKey("Group",on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, null=True)
    tournament_points = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_average = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_wins = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_losses = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_doubles = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_hands = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_disqualifications = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_injuries = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_surrenders = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_opponent_injuries = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_amount_rounds = models.PositiveSmallIntegerField(null=True, default=0)
    tournament_points_modified = models.PositiveSmallIntegerField(null=True, default=0)
    round_average = models.PositiveSmallIntegerField(null=True, default=0)



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


disqualification = 'dyskwalifikacja'
injury = 'kontuzja'
average = 'średnia'
surrender = 'poddanie'
withdrawal = 'wycofanie'


# ROUND_SPECIAL_STATUSES = [
#     (disqualification, 'dyskwalifikacja'),
#     (surrender, 'poddanie'),
#     (withdrawal, 'wycofanie'),
#     (average, 'średnia'),
# ]
# ROUND_CONTUSIONS_STATUSES = [
#     (injury, 'kontuzja'),
# ]

ROUND_SPECIAL_STATUSES = [
    ('dyskwalifikacja', 'dyskwalifikacja'),
    ('poddanie', 'poddanie'),
    ('wycofanie', 'wycofanie'),
    ('średnia', 'średnia'),
]
ROUND_CONTUSIONS_STATUSES = [
    (injury, 'kontuzja'),
]

ROUND_STATUS = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    # ('6', '6'),
    # ('7', '7'),
    # ('8', '8'),
    # ('9', '9'),
    # ('10', '10'),
    # ('kontuzja', 'kontuzja'),
    # ('dyskwalifikacja', 'dyskwalifikacja'),
    # ('poddanie', 'poddanie'),
    # ('wycofanie', 'wycofanie'),
    # ('średnia', 'średnia'),
] + ROUND_SPECIAL_STATUSES + ROUND_CONTUSIONS_STATUSES

class Round(models.Model):

    order = models.PositiveSmallIntegerField(null=True)
    fight = models.ForeignKey("Fight", on_delete=models.CASCADE, related_name="rounds_of_fight", null=True)
    points_fighter_one = models.CharField(max_length=20, choices=ROUND_STATUS, null=True)
    points_fighter_two = models.CharField(max_length=20, choices=ROUND_STATUS, null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="rounds_of_group", null=True)
    fighter_one = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="rounds_of_participant_one", null=True )
    fighter_two = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="rounds_of_participant_two", null=True )

    def __str__(self):
        return f"{self.order} {self.fight} \
        {self.group} {self.fighter_one} {self.fighter_one} {self.points_fighter_one} {self.points_fighter_two}"

    class Meta:
        verbose_name = "Runda"
        verbose_name_plural = "Rundy"





