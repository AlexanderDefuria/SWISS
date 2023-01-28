import os
import pytest

from django.test import TestCase
from apps.entry.models import *
from apps.entry.tests.common import *

# https://realpython.com/testing-in-django-part-1-best-practices-and-examples/#structure
# https://realpython.com/django-pytest-fixtures/#creating-django-fixtures
# Create fixtures data files `python3 manage.py dumpdata --format json entry.orgsettings -o organizations.json`


@pytest.mark.django_db
def test_team_creation(create_team):
    team = create_team
    assert isinstance(team, Team)
    assert str(team) == str(team.number) + "\t\t" + str(team.name)


@pytest.mark.django_db
def test_default_image(create_team):
    team = create_team
    assert team.first_image() == 'robots/default.jpg'

