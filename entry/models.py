from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Event(models.Model):
    name = models.TextField(default="NA")
    TBA_key = models.TextField(default="NA")
    TBA_eventType = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __str__(self):
        return self.name


class Team(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    name = models.CharField(default="team", max_length=40)
    cur_event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    event_one = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    event_two = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    event_three = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    event_four = models.ForeignKey(Event, on_delete=models.CASCADE, default=0, related_name='+')
    TBA_key = models.CharField(default="NA", max_length=40)

    def __str__(self):
        return str(self.number) + "\t\t" + str(self.name)


class Match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])

    # Cargo
    auto_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    first_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    second_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    third_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    ship_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(8), MinValueValidator(0)])

    # Hatches
    auto_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    first_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    second_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    third_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
    cargo_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(8), MinValueValidator(0)])

    # Climb
    climb = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)])

    # Start
    first_start = models.BooleanField(default=True)
    second_start = models.BooleanField(default=False)

    # Defense
    defense_time = models.IntegerField(default=0, validators=[MaxValueValidator(135000), MinValueValidator(1)])

    def __str__(self):
        return self.team.name + "  Match: " + str(self.match_number)




