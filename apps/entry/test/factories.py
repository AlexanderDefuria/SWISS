from factory import Sequence, LazyAttribute, Iterator
from factory.django import DjangoModelFactory

from apps.common.tests.faker import faker
from apps.entry.models import Team, Schedule, Attendance
from apps.organization.models import Event


def random_team_number():
    return LazyAttribute(lambda x: faker.pyint(min_value=0, max_value=999))


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = LazyAttribute(lambda x: faker.unique.organism())
    number = Sequence(lambda n: n)
    colour = faker.color()


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = Schedule

    match_number = Sequence(lambda n: n)
    event = Iterator(Event.objects.all())
    red1 = random_team_number()
    red2 = random_team_number()
    red3 = random_team_number()
    blue1 = random_team_number()
    blue2 = random_team_number()
    blue3 = random_team_number()
    match_type = "Qualification"
    description = LazyAttribute(lambda x: faker.sentence())
    if faker.boolean():
        red_score = random_team_number()
        blue_score = random_team_number()


class AttendanceFactory(DjangoModelFactory):
    class Meta:
        model = Attendance

    team = Iterator(Team.objects.all())
    event = Iterator(Event.objects.all())
    qualification_rank = Sequence(lambda n: n)
    playoff_rank = Sequence(lambda n: n)

