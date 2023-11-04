import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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

