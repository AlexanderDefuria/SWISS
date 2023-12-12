from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.postgres.fields import ArrayField

from apps.organization.models import Organization, Event


class Team(models.Model):
    class Meta:
        ordering = ['number']

    number = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    name = models.CharField(default="team", max_length=100)
    colour = models.CharField(default="#000000", max_length=7)
    # TODO Remove and move somewhere else.
    pick_status = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)])
    glance = models.FileField(upload_to='json/', null=True, blank=True)
    avatar = models.CharField(default="NA", max_length=10000)
    totalMatchesWon = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    totalMatchesLost = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    totalMatchesPlayed = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    winRate = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    eventsAttended = ArrayField(models.CharField(max_length=6, blank=True, default=''), default=list)

    def first_image(self):
        try:
            return Images.objects.filter(team=self).first()
        except Images.DoesNotExist:
            return 'robots/default.jpg'

    def __str__(self):
        return str(self.number) + " -- " + str(self.name)


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
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    qualification_rank = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    playoff_rank = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])

    def __str__(self):
        return str(self.team) + ' at ' + self.event.name


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"
        ordering = ['-match_number']

    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=0)
    match_number = models.IntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(-1)])

    # Pre Match
    on_field = models.BooleanField(default=False)
    preloaded_balls = models.fields.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)])
    auto_start_x = models.fields.FloatField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])
    auto_start_y = models.fields.FloatField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])

    # Auto
    auto_placement = models.fields.IntegerField(default=0)
    auto_route = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    auto_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    auto_comment = models.TextField(default="")
    auto_baseline = models.BooleanField(default=False)
    auto_cones = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    auto_cubes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Teleop
    placement = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cycles = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    intake_type = models.SmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    under_defense = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    defended_by = models.IntegerField(default=0, blank=True, null=True)
    offensive_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    cones = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cubes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Defense
    defense_played = models.BooleanField(default=False)
    defense_time = models.IntegerField(default=0)
    defense_rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    defense_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(250), MinValueValidator(0)])
    team_defended = models.IntegerField(default=0, blank=True, null=True)
    able_to_push = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # Endgame
    endgame_time = models.IntegerField(default=0, validators=[MaxValueValidator(165), MinValueValidator(0)])
    endgame_action = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    endgame_attempts = models.IntegerField(default=0)
    endgame_comments = models.TextField(default="")

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

    def save(self, *args, **kwargs):
        try:
            result = Result()
            result.schedule = Schedule.objects.get(match_number=self.match_number, event=self.event)
            result.match = self
            result.ownership = self.ownership
            result.completed = True
            result.event = self.ownership.settings.current_event

            result.save()
        except Exception as e:
            print("error updating result for " + str(self))
            print(e)
        super(Match, self).save(*args, **kwargs)

    @staticmethod
    def decode_grid(grid_val):
        def _get_bit(value: int, location: int) -> bool:
            return bool((value >> location) & 1)

        positions: list[bool] = []
        for i in range(0, 36):
            for j in range(0, 4):
                positions[i] = _get_bit(grid_val, i)


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
    weight = models.SmallIntegerField(default=0, validators=[MaxValueValidator(200), MinValueValidator(0)])

    # Name
    scouter_name = models.TextField(default="")
    ownership = models.ForeignKey(Organization, on_delete=models.CASCADE, default=0, related_name='+')

    # Given Stats
    MOTOR_CHOICES = [
        # (Program Name, Human Readable name)
        ("none", "Doesn't Drive?"),
        ("cim", "CIM Motors"),
        ("falcon", "Falcon 500 Motors"),
        ("kraken", "Kraken X60"),
        ("neo", "NEO Motors"),
        ("neovtx", "NEO Vortex"),
        ("other", "Unusual DriveTrain... See Comments")
    ]

    DRIVE_TRAIN = [
        # TODO: Fill in the DRIVE TRAIN options
        ('', '')
    ]

    def get_data(self, field):
        return getattr(self, field)

    def __str__(self):
        return self.team.name


class Result(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, blank=True)
    completed = models.BooleanField(default=False)
    gouda = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0, related_name='+')
    ownership = models.ForeignKey(Organization, on_delete=models.CASCADE, default=0, related_name='+')

    def __str__(self):
        return str(self.match.match_number) + ' from ' + self.event.name

