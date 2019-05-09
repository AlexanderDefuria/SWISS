from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Team(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    name = models.CharField(default="team", max_length=40)
    matches = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Cargo
    first_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    ship_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Hatches
    first_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    cargo_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Climb
    first_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Start
    first_start = models.BooleanField(default=True)
    second_start_r = models.BooleanField(default=False)
    second_start_l = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Match(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    name = models.CharField(default="team", max_length=40)
    match = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Cargo
    first_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    ship_cargo = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Hatches
    first_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    cargo_hatch = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Climb
    first_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    second_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    third_climb = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(1)])

    # Start
    first_start = models.BooleanField(default=True)
    second_start_r = models.BooleanField(default=False)
    second_start_l = models.BooleanField(default=False)

    def __str__(self):
        return self.name + "  Match: " + self.match
