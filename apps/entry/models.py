from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date


class Event(models.Model):
    name = models.TextField(default="NA")
    FIRST_key = models.TextField(default="NA")
    FIRST_eventType = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    start = models.DateField(default=date(2020, 1, 1),
                             validators=[MaxValueValidator(date(2020, 12, 31)), MinValueValidator(date(2020, 1, 1))])
    end = models.DateField(default=date(2020, 1, 1),
                           validators=[MaxValueValidator(date(2020, 12, 31)), MinValueValidator(date(2020, 1, 1))])
    imported = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Images(models.Model):
    image = models.ImageField(upload_to='robots', default='/robots/default.jpg', null=False)
    name = models.CharField(default="Wally", max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    name = models.CharField(default="team", max_length=100)
    images = models.ManyToManyField(Images)
    colour = models.CharField(default="#000000", max_length=7)

    def first_image(self):
        # code to determine which image to show. The First in this case.
        try:
            return self.images.all()[0].image
        except IndexError:
            return '/robots/default.jpg'

    def __str__(self):
        return str(self.number) + "\t\t" + str(self.name)


class Schedule(models.Model):
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_type = models.TextField(default="NA", max_length=40)

    red1 = models.IntegerField(Team, default=0)
    red2 = models.IntegerField(Team, default=0)
    red3 = models.IntegerField(Team, default=0)
    blue1 = models.IntegerField(Team,  default=0)
    blue2 = models.IntegerField(Team,  default=0)
    blue3 = models.IntegerField(Team,  default=0)
    red_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    blue_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    def __str__(self):
        return self.match_number


class Match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])

    # Pre Match
    auto_start = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    preloaded_balls = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    on_field = models.BooleanField(default=False)

    # Auto
    auto_route = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    baseline = models.BooleanField(default=False)
    outer_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    lower_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    inner_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    fouls_auto = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    rating_auto = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    auto_comment = models.TextField(default="")

    # Teleop
    outer = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    lower = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    inner = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    wheel_score = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    wheel_rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    balls_collected = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    full_cycles = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    missed_balls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    ball_intake_type = models.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    under_defense = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # Defense
    defense_rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    defense_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(250), MinValueValidator(0)])
    team_defended = models.SmallIntegerField(default=0, validators=[MaxValueValidator(10000), MinValueValidator(0)])
    able_to_push = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # Climb
    climb = models.BooleanField(default=False)
    climb_location = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    field_timeout_pos = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # Human Player
    hp_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    dt_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    yellow_card = models.BooleanField(default=False)

    # Comments
    scouter_name = models.TextField(default="")

    def __str__(self):
        return self.team.name + "  Match: " + str(self.match_number)


class Pits(models.Model):
    number = models.TextField(default="NA")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)

    # Given Stats
    MOTOR_CHOICES = [
        # (Program Name, Human Readable name)
        ("none", "Doesn't Drive?"),
        ("cim", "CIM Motors"),
        ("falcon", "Falcon 500 Motors"),
        ("neo", "NEO Motors"),
        ("other", "Unusual DriveTrain... See Comments")
    ]
    motor_type = models.CharField(
        max_length=6,
        choices=MOTOR_CHOICES,
        default="none"
    )
    motor_number = models.SmallIntegerField(default=0, validators=[MaxValueValidator(8), MinValueValidator(0)])
    weight = models.SmallIntegerField(default=0, validators=[MaxValueValidator(150), MinValueValidator(0)])

    # Comments
    comments = models.TextField(default="No Comments")

    def __str__(self):
        return self.team.name
