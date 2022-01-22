import datetime

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


class Log(models.Model):
    gremlin = models.ForeignKey(Gremlin, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.PROTECT)
    # 0-Pending 1-Accepted 2-Rejected
    status = models.IntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)])
    datetime = models.DateField(auto_now=False, auto_now_add=True)
    minutes = models.IntegerField(default=0, validators=[MaxValueValidator(24*60), MinValueValidator(0)])

    def __str__(self):
        return self.gremlin.user.username + " " + str(self.datetime) + " " + str(self.minutes)



