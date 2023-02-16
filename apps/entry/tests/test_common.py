import pytest
from django.test import TestCase
from apps.entry.models import *
from apps.entry.tests.common import *
from apps.entry.models import Organization


@pytest.mark.django_db
def test_should_create_org_settings(create_org_settings_fixture) -> None:
    assert create_org_settings_fixture.pk is not None


@pytest.mark.django_db
def test_should_create_organization(create_organization_fixture) -> Organization:
    assert create_organization_fixture.name == 'MaxTech'
    return create_organization_fixture



@pytest.mark.django_db
def test_team_creation(create_team_factory) -> None:
    assert create_team_factory.number == 4343
