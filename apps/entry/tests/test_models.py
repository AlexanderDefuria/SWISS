from django.test import TestCase
from apps.entry.models import *

# https://realpython.com/testing-in-django-part-1-best-practices-and-examples/#structure
# https://realpython.com/django-pytest-fixtures/#creating-django-fixtures

class TeamTest(TestCase):
    fixtures = ["/home/alexander/Desktop/FRC-Scouting/apps/entry/tests/test_data/teams.json"]

    @classmethod
    def create_team(cls):
        return Team.objects.create(name="test team name",
                                   number=4343,
                                   colour="#000000")

    def test_team_creation(self):
        team = self.create_team()
        self.assertTrue(isinstance(team, Team))
        self.assertEqual(str(team), str(team.number) + "\t\t" + str(team.name))

    def test_default_image(self):
        team = self.create_team()
        self.assertEqual(team.first_image(), 'robots/default.jpg')

    def test_check_fixture(self):
        team = Team.objects.get(pk=188)
        self.assertEqual(team.name, "Blizzard")

