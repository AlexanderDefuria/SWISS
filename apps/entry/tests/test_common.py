import pytest
from django.test import TestCase
from apps.entry.models import *
from apps.entry.tests.common import *

@pytest.mark.django_db
def test_should_create_org_settings(create_org_settings: OrgSettings) -> None:
    assert create_org_settings.pk != None


@pytest.mark.django_db
def test_should_create_organization(create_organization: Organization) -> None:
    assert create_organization.name == 'MaxTech'


@pytest.mark.django_db
def test_team_creation(create_team: Team) -> None:
    assert create_team.number == 4343
