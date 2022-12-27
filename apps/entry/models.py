import random
import uuid as uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Team(models.Model):
    class Meta:
        ordering = ['number']

    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    name = models.CharField(default="team", max_length=100)
    colour = models.CharField(default="#000000", max_length=7)
    # TODO Remove and move somewhere else.
    pick_status = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)])
    glance = models.FileField(upload_to='json/', null=True, blank=True)

    def first_image(self):
        # code to determine which image to show. The First in this case.
        try:
            # TODO Replace references?
            return self.images.all()[random.randint(0, len(self.images.all()) - 1)].image
        except Exception:
            return 'robots/default.jpg'

    def __str__(self):
        return str(self.number) + "\t\t" + str(self.name)


class Images(models.Model):
    class Meta:
        verbose_name_plural = "Images"
        ordering = ['name']

    image = models.ImageField(upload_to='robots', default='/robots/default.jpg', null=False)
    name = models.CharField(default="Wally", max_length=100)
    ownership = models.ForeignKey(Team, on_delete=models.CASCADE, default=0, related_name='+')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0, related_name='+')

    def __str__(self):
        return self.name


class Event(models.Model):
    class Meta:
        ordering = ['start']

    name = models.TextField(default="NA")
    FIRST_key = models.TextField(default="NA")
    FIRST_district_key = models.TextField(default="NA")
    FIRST_eventType = models.TextField(default="NA")
    start = models.DateField(default=date(2020, 1, 1),
                             validators=[MaxValueValidator(date(2220, 12, 31)),
                                         MinValueValidator(date(2020, 1, 1))])
    end = models.DateField(default=date(2020, 1, 1),
                           validators=[MaxValueValidator(date(2220, 12, 31)), MinValueValidator(date(2020, 1, 1))])

    imported = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    class Meta:
        verbose_name_plural = "Schedule"
        ordering = ['match_number']

    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_type = models.TextField(default="NA", max_length=40)
    description = models.TextField(default="NA", max_length=100)

    red1 = models.IntegerField(Team, default=0)
    red2 = models.IntegerField(Team, default=0)
    red3 = models.IntegerField(Team, default=0)
    blue1 = models.IntegerField(Team, default=0)
    blue2 = models.IntegerField(Team, default=0)
    blue3 = models.IntegerField(Team, default=0)
    red_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    blue_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    def __str__(self):
        return str(self.match_number)


class Attendance(models.Model):
    team = models.IntegerField(Team, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    qualification_rank = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    playoff_rank = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    def __str__(self):
        return str(self.team) + ' at ' + self.event.name


class OrgSettings(models.Model):
    # Organization wide settings for users.
    class Meta:
        verbose_name_plural = "Organization Settings"

    AVAILABLE_POSITIONS = (
        # (Program Name, Human Readable name)
        ("PA", "Public Access"),
        ("OV", "Only View"),
        ("MS", "Match Scout"),
        ("PS", "Pit Scout"),
        ("GS", "General Scout"),
        ("DT", "Drive Team"),
        ("LS", "Lead Scout"),
        ("NA", "No Access"),
    )

    NEW_USER_POSITIONS = AVAILABLE_POSITIONS[:-1]
    NEW_USER_CREATION_OPTIONS = (
        # **, first is approval for use, second is account creation
        ("MA", "Manual Approval, Open Registration"),
        ("MM", "Manual Creation of All Users"),
        ("AA", "Open Registration and Use")
    )

    allow_photos = models.BooleanField(default=True)
    allow_schedule = models.BooleanField(default=True)
    new_user_creation = models.CharField(max_length=2, choices=NEW_USER_CREATION_OPTIONS, default="MM")
    new_user_position = models.CharField(max_length=2, choices=NEW_USER_POSITIONS, default="OV")
    current_event = models.ForeignKey(Event, on_delete=models.SET_DEFAULT, default=0)

    def __str__(self):
        return self.organization.name + 'settings'


class Organization(models.Model):
    # Organization Information
    class Meta:
        verbose_name_plural = "Organizations"

    name = models.CharField(max_length=100, blank=False, unique=True)
<<<<<<< HEAD
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
=======
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)
>>>>>>> 77cc7f077a516e0416a85cbddd6fda83757921d9
    reg_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    settings = models.OneToOneField(OrgSettings, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name


class OrgMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    tutorial_completed = models.BooleanField(default=False)
    position = models.CharField(max_length=2, choices=OrgSettings.AVAILABLE_POSITIONS, default="GS")

    def __str__(self):
        return self.position + " - " + self.user.username + " from " + self.organization.name


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"
        ordering = ['-match_number']

    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(-1)])
    gouda = models.FloatField(default=0, blank=True, null=True)

    # Pre Match
    auto_start_x = models.fields.FloatField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])
    auto_start_y = models.fields.FloatField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])
    on_field = models.BooleanField(default=False)
    preloaded_balls = models.fields.BooleanField(default=True)

    # Auto
    auto_route = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    baseline = models.BooleanField(default=False)
    upper_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    lower_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    missed_balls_auto = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    auto_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    auto_comment = models.TextField(default="")

    # Teleop
    upper = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    lower = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    missed_balls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    intake_type = models.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    under_defense = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    defended_by = models.IntegerField(default=0, blank=True, null=True)
    offensive_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])

    # Defense
    defense_played = models.BooleanField(default=False)
    defense_time = models.IntegerField(default=0)
    defense_rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    defense_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(250), MinValueValidator(0)])
    team_defended = models.IntegerField(default=0, blank=True, null=True)
    able_to_push = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # Climb
    lock_status = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    endgame_action = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    climb_time = models.IntegerField(default=0)
    climb_attempts = models.IntegerField(default=0)
    climb_comments = models.TextField(default="")

    # Human Player
    fouls_hp = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    fouls_driver = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    yellow_card = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    yellow_card_description = models.TextField(default="")

    # Scouter
    scouter_name = models.TextField(default="")
    comment = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    ownership = models.ForeignKey(Organization, on_delete=models.CASCADE, default=0, related_name='+')

    def __str__(self):
        return self.team.name + " Match: " + str(self.match_number) + " at " + str(self.event)


class Pits(models.Model):
    class Meta:
        verbose_name_plural = "Pits"
        ordering = ['team']

    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)

    # Drivetrain
    drivetrain_style = models.TextField(default="")
    drivetrain_wheels = models.TextField(default="")
    drivetrain_motortype = models.TextField(default="")
    drivetrain_motorquantity = models.SmallIntegerField(default=0,
                                                        validators=[MaxValueValidator(10), MinValueValidator(0)])
    drivetrain_speed = models.SmallIntegerField(default=0, validators=[MaxValueValidator(20), MinValueValidator(0)])
    drivetrain_transmission = models.TextField(default="")

    # Auto
    auto_route = models.BooleanField(default=False)
    auto_description = models.TextField(default="")
    auto_scoring = models.SmallIntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)])

    # Teleop
    tele_scoring = models.SmallIntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)])
    tele_positions = models.SmallIntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])

    # Robot styles and stats
    ball_intake = models.TextField(default="")
    ball_capacity = models.SmallIntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    shooter_style = models.TextField(default="")
    low_bot = models.BooleanField(default=False)
    weight = models.SmallIntegerField(default=0, validators=[MaxValueValidator(200), MinValueValidator(0)])
    targeting_system = models.TextField(default="")

    # Climb
    climb_locations = models.SmallIntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])

    # Name
    scouter_name = models.TextField(default="")
    ownership = models.ForeignKey(Organization, on_delete=models.CASCADE, default=0, related_name='+')

    # Given Stats
    MOTOR_CHOICES = [
        # (Program Name, Human Readable name)
        ("none", "Doesn't Drive?"),
        ("cim", "CIM Motors"),
        ("falcon", "Falcon 500 Motors"),
        ("neo", "NEO Motors"),
        ("other", "Unusual DriveTrain... See Comments")
    ]

    def getData(self, field):
        return getattr(self, field)

    def __str__(self):
        return self.team.name


class Result(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, default=0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, blank=True)
    completed = models.BooleanField(default=False)
    red_gouda = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    blue_gouda = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    ownership = models.ForeignKey(Team, on_delete=models.CASCADE, default=0, related_name='+')

    def __str__(self):
        return str(self.schedule.match_number) + ' from ' + self.schedule.event.name

