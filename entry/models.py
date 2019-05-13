from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Team(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    name = models.CharField(default="team", max_length=40)
    matches = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])

    # Cargo
    auto_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    first_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    second_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    third_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    ship_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    # Hatches
    auto_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    first_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    second_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    third_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    ship_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    # Climb
    first_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    second_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    third_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    # Start
    first_start = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    second_start = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    # Defense
    defense_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    defense_matches = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    def __str__(self):
        return self.name


class Match(models.Model):
    team_number = models.IntegerField(default=0, validators=[MaxValueValidator(9000), MinValueValidator(0)])
    team_name = models.CharField(default="unnamed_team", max_length=40)
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
        return self.name + "  Match: " + self.match
