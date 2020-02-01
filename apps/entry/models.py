from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.entry.fields import PositionField


class Event(models.Model):
    name = models.TextField(default="NA")
    TBA_key = models.TextField(default="NA")
    TBA_eventType = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    start = models.IntegerField(default=0, validators=[MaxValueValidator(100000000), MinValueValidator(0)])
    imported = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    name = models.CharField(default="team", max_length=100)

    event_one = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    event_two = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    event_three = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    event_four = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    event_five = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')

    TBA_key = models.TextField(default="NA", max_length=40)

    def __str__(self):
        return str(self.number) + "\t\t" + str(self.name)


class Schedule(models.Model):
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    TBA_key = models.TextField(default="NA", max_length=40)
    match_type = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    red1 = models.IntegerField(Team, default=0)
    red2 = models.IntegerField(Team, default=0)
    red3 = models.IntegerField(Team,  default=0)
    blue1 = models.IntegerField(Team,  default=0)
    blue2 = models.IntegerField(Team,  default=0)
    blue3 = models.IntegerField(Team,  default=0)
    red_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    blue_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    def __str__(self):
        return self.match_number


# TODO Adjust for 2020
class Match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])

    # Auto
    outer_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    low_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    inner_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    baseline = models.fields.BooleanField(default=False)
    fouls_auto = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    rating_auto = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    # start = models.fields.TextField(default="")
    # finish = models.fields.TextField(default="")

    # Teleop
    outer = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    low = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    inner = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    wheel_rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    balls_collected = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    full_cycles = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(99), MinValueValidator(0)])
    fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])

    # Defense
    defense_time = models.IntegerField(default=0, validators=[MaxValueValidator(135000), MinValueValidator(0)])
    defense_rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    defense_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])

    # Comments
    comments = models.TextField(default="")

    def __str__(self):
        return self.team.name + "  Match: " + str(self.match_number)
