from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Team(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    name = models.CharField(default="team", max_length=40)
    matches = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])

    # Cargo
    auto_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    first_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    ship_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Hatches
    auto_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    first_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    cargo_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Climb
    first_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Start
    first_start = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_start = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    def __str__(self):
        return self.name


class Match(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9000), MinValueValidator(1)])
    name = models.CharField(default="unnamed_team", max_length=40)
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(1)])

    # Cargo
    auto_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    first_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    second_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    third_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    ship_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(8), MinValueValidator(1)])

    # Hatches
    auto_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    first_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    second_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    third_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(1)])
    cargo_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(8), MinValueValidator(1)])

    # Climb
    climb = models.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(1)])

    # Start
    first_start = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_start = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    def __str__(self):
        return self.name + "  Match: " + self.match
