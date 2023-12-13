from django.test import TestCase

from apps.entry.models import Team, Schedule
from apps.entry.test.factories import TeamFactory, ScheduleFactory
from apps.organization.test.factories import EventFactory


class TeamFactoryTest(TestCase):

    def test_team_creation(self):
        team_a = TeamFactory()
        self.assertTrue(isinstance(team_a, Team))
        self.assertEqual(str(team_a), str(team_a.number) + " -- " + str(team_a.name))
        team_b = TeamFactory()
        self.assertNotEqual(team_a, team_b)
        self.assertNotEqual(team_a.name, team_b.name)


class ScheduleFactoryTest(TestCase):

    def test_schedule_creation(self):
        event_a = EventFactory()  # id 0
        event_b = EventFactory()  # id 1
        team = TeamFactory()
        schedule_a = ScheduleFactory(event=event_b)  # This overrides the event iterator
        self.assertTrue(isinstance(schedule_a, Schedule))
        schedule_b = ScheduleFactory(event=event_b)
        self.assertNotEqual(schedule_a, schedule_b)
        self.assertNotEqual(schedule_a.match_number, schedule_b.match_number)
        self.assertEqual(schedule_a.event, event_b)
        self.assertEqual(schedule_b.event, event_b)
        self.assertEqual(schedule_a.event, schedule_b.event)
        schedule_c = ScheduleFactory()  # This starts with event id 0
        self.assertNotEqual(schedule_a.event, schedule_c.event)
