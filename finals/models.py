from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from tournaments.models import Tournament
from tournament_calculating.models import Participant


class Finalist(models.Model):

    participant = models.OneToOneField(
        "tournament_calculating.Participant",
        on_delete=models.CASCADE,
        primary_key=True
    )
    final_points = models.PositiveSmallIntegerField(null=True, default=0)
    final_points_average = models.PositiveSmallIntegerField(null=True, default=0)
    group = models.ForeignKey("tournament_calculating.Group", on_delete=models.CASCADE, related_name="finalists",
                              null=True)

    def __str__(self):
        return f"{self.final_points} {self.group}  {self.final_points_average} {self.participant} "


class Stage(models.Model):
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
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="stages")
    stage_participants = models.ManyToManyField('tournament_calculating.Participant', related_name='stages')
    color_fighter_one = models.CharField(max_length=30, choices=COLOR, null=True)
    color_fighter_two = models.CharField(max_length=30, choices=COLOR, null=True)
    number_outgoing = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.number} {self.tournament} {self.stage_participants} {self.color_fighter_one} {self.color_fighter_two} {self.number_outgoing}"


class FinalFight(models.Model):
    order = models.PositiveSmallIntegerField(null=True)
    stage = models.ForeignKey("Stage", on_delete=models.CASCADE, related_name="fights", null=True)
    rounds = models.PositiveSmallIntegerField(null=True)
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="final_fights", null=True)
    final_fighter_one = models.ForeignKey('tournament_calculating.Participant', on_delete=models.CASCADE, related_name="final_fighters_one", null=True )
    final_fighter_two = models.ForeignKey('tournament_calculating.Participant', on_delete=models.CASCADE, related_name="final_fighters_two", null=True )
    final_fighter_one_points = models.PositiveSmallIntegerField(null=True, default=0)
    final_fighter_two_points = models.PositiveSmallIntegerField(null=True, default=0)
    resolved = models.BooleanField(default=False , null=True)


    def __str__(self):
        return f"{self.stage} {self.rounds} {self.tournament} {self.final_fighter_one} {self.final_fighter_two}"

    class Meta:
        verbose_name = "Walka"
        verbose_name_plural = "Walki"


class FinalRound(models.Model):
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
        ('11', '11'),
        ('draw','remis' ),
        ('brak rezultatu','brak rezultatu' ),
        ('nie było walki','nie było walki' ),
        ('brak statusu','brak statusu' ),
        ('dyskwalifikacja','dyskwalifikacja' ),
        ('kontuzja','kontuzja' ),
        ('nieobecność','nieobecność'),
        ('inne','inne' ),
        ('poddanie', 'poddanie')
    )
    order = models.PositiveSmallIntegerField(null=True)
    final_fight = models.ForeignKey("FinalFight", on_delete=models.CASCADE, related_name="rounds_final_fight", null=True)
    final_points_fighter_one = models.CharField(max_length=20, choices=STATUS, null=True)
    final_points_fighter_two = models.CharField(max_length=20, choices=STATUS, null=True)
    stage = models.ForeignKey("Stage", on_delete=models.CASCADE, related_name="rounds_of_stage", null=True)
    final_fighter_one = models.ForeignKey('tournament_calculating.Participant', on_delete=models.CASCADE, related_name="final_rounds_participant_one",
                                    null=True)
    final_fighter_two = models.ForeignKey('tournament_calculating.Participant', on_delete=models.CASCADE, related_name="final_rounds_participant_two",
                                    null=True)

    def __str__(self):
        return f"{self.order} {self.final_fight} \
        {self.stage} {self.final_fighter_one} {self.final_fighter_one} {self.final_points_fighter_one} {self.final_points_fighter_two}"

    class Meta:
        verbose_name = "Runda finałowa"
        verbose_name_plural = "Rundy finałowe"



class Winner(models.Model):
    MEDALS = (
    ('złoto','złoto' ),
    ('srebro','srebro' ),
    ('brąz','brąz' ),
    )
    participant = models.OneToOneField(
    Participant,
    on_delete=models.CASCADE,
    primary_key=True,
    )
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="winners")
    medal = models.CharField(max_length=20, choices=MEDALS, null=True)

    def __str__(self):
        return f"{self.participant} {self.tournament} {self.medal}"


    # class Draw(models.Model):
    #     draw_fighter_one =
    #     draw_fighter_two =
