import uuid as uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date
from django.contrib.auth.models import User

__all__ = [
    'Team',
    'Images',
    'Event',
    'Schedule',
    'Attendance',
    'Match',
    'Pits',
    'Result',
    'Organization',
    'OrgMember',
    'OrgSettings',
    'PointsConfig',
    'User'
]


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
        return str(self.name)


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
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
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

    # Pre Match
    on_field = models.BooleanField(default=False)
    preloaded_balls = models.fields.IntegerField(default=0, validators=[MaxValueValidator(3), MinValueValidator(0)])
    auto_start_x = models.fields.FloatField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])
    auto_start_y = models.fields.FloatField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])

    # Auto
    auto_placement = models.fields.TextField(default='000000000000000000000000000000000000', max_length=36)
    auto_placement_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    auto_route = models.fields.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    auto_fouls = models.SmallIntegerField(default=0, validators=[MaxValueValidator(25), MinValueValidator(0)])
    auto_comment = models.TextField(default="")
    auto_baseline = models.BooleanField(default=False)
    auto_cones = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    auto_cubes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    # auto_endgame_action = models.SmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    # Teleop
    placement = models.TextField(default='000000000000000000000000000000000000', max_length=36)
    placement_score = models.IntegerField(default=0, validators=[MaxValueValidator(9999), MinValueValidator(0)])
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

            self.placement_score = self.calculate_grid_points(False)
            self.auto_placement_score = self.calculate_grid_points(True)

        except Exception as e:
            print("error updating result for " + str(self))
            print(e)
        super(Match, self).save(*args, **kwargs)

    @staticmethod
    def load_grid(placement) -> list[list[str]]:
        """
        Loads the placement grid into a 2D array of characters

        :param placement:
        :return:
        """
        grid = [[]]
        for i in range(4):
            grid.append([])
            for j in range(9):
                grid[i].append(placement[i*9 + j])
        return grid

    def calculate_grid_points(self, auto: bool) -> int:
        """
        Calculates the points earned by the auto placement grid

        :param auto: Whether or not the auto placement grid should be used
        :return: The number of points the team earned from the grid
        """
        total = 0
        placement = self.auto_placement if auto else self.placement
        index = 0
        if not auto:
            for char in self.auto_placement:
                if char == '1':
                    placement = placement[:index] + '0' + placement[index + 1:]
                index += 1

        # print(placement)
        for row in range(4):
            for index in range(9):
                bit_index = row*9 + index
                if placement[bit_index] == '1':
                    # print(bit_index)
                    if row == 0:  # The top row of the grid
                        total += 6 if auto else 5
                    elif row == 1:  # The second
                        total += 4 if auto else 3
                    else:  # The bottom rows 3 and 4 (indices 2 and 3)
                        total += 3 if auto else 2

        return total

    def calculate_line_bonus(self):
        total = 0
        # For the endgame we need to check for the 3 in a row
        # This includes the cubes and cones from the auto
        index = 0
        placement = self.placement
        for char in self.auto_placement:
            if char == '1':
                placement = placement[:index] + '1' + placement[index + 1:]
            index += 1

        print(placement)

        grid = self.load_grid(placement)
        for row in range(2):  # Count the top two rows of either cones or cubes
            con_count = 0
            for index in range(9):
                if grid[row][index] == '1':
                    con_count += 1
                if con_count >= 3:
                    total += 5
                    con_count = 0

        con_count = 0
        for index in range(9):  # Count the bottom row of either cones or cubes
            if grid[2][index] == '1' or grid[3][index] == '1':
                con_count += 1
            if con_count >= 3:
                total += 5
                con_count = 0

        return total

    def calculate_points(self) -> int:
        total = self.calculate_grid_points(auto=True)  # Correct
        total += self.calculate_grid_points(auto=False)  # Correct
        total += self.calculate_line_bonus()
        # total += self.auto_baseline * 3
        return total

    @staticmethod
    def decode_grid(grid_val):
        def _get_bit(value: int, location: int) -> bool:
            return bool((value >> location) & 1)

        positions: list[list[bool]] = [[]]
        for i in range(0, 9):
            for j in range(0, 4):
                positions[j][i] = _get_bit(grid_val, i*j + j)


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
        ("neo", "NEO Motors"),
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


class PointsConfig(models.Model):
    # This class is created by Orgs to rank teams based on what they want to prioritize
    # The defaults here are what we recommend.

    pass
