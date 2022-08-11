from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Gremlin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Card(models.Model):
    user = models.ForeignKey(Gremlin, on_delete=models.CASCADE)
    uuid = models.UUIDField()

    def __str__(self):
        return self.uuid


class Log(models.Model):
    # Each Log is an in or an out. Only outs track time.

    # Fill in later
    mentor = models.ForeignKey(Mentor, on_delete=models.PROTECT, null=True)
    tasks = models.TextField(default="", null=True)

    # Auto Fill
    # 0-Pending 1-Accepted 2-Rejected 3-Issue
    status = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)])
    datetime = models.DateField(auto_now=False, auto_now_add=True)
    out = models.BooleanField(default=False)
    duration = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(24*60)])  # Minutes
    total = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # Minutes

    # Required
    gremlin = models.ForeignKey(Gremlin, on_delete=models.CASCADE)

    def clean_and_save(self, *args, **kwargs):
        last = Log.objects.last()

        if last.datetime.day is not self.datetime.day:
            if Log.objects.count() % 2 is 1:
                # OUT entry across days (almost definitely forgot to clock out)
                last.status = 3  # Mark as an Issue entry
                last.save()

        if Log.objects.count() % 2 is 0:
            # IN entry
            self.save(*args, **kwargs)  # Call the "real" save() method.
            return
        elif Log.objects.count() % 2 is 1:
            # OUT entry
            duration_dt = self.datetime - last.datetime
            self.duration = duration_dt.total_seconds() % 60  # To minutes
            self.total += self.duration
            self.out = True
            return

    def __str__(self):
        return self.gremlin.user.username + " " + str(self.datetime)

