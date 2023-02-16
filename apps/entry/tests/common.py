import os
import pytest

from apps.entry.models import *

base_test_dir = os.path.dirname(os.path.realpath(__file__))

username = 'test_account_swiss'
password = 'passwordtest'

def load_fixtures(relative_fixtures) -> list:
    fixtures = []
    for path in relative_fixtures:
        fixtures.append(os.path.join(base_test_dir, path))
    return fixtures


def create_user() -> User:
    user = User.objects.create_user(
        username=username,
        password=password
    )
    user.save()
    assert user.username == 'test_account_swiss'
    return user

def create_org_member(user: User, org: Organization) -> OrgMember:
    member = OrgMember.objects.create(
        user=user,
        organization=org
    )
    member.save()
    assert member.user.username == user.username
    assert member.organization.name == org.name
    return member

def create_team():
    return Team.objects.create(
        number=4343,
        name='MaxTech'
    )

def create_event():
    return Event.objects.create(
        name="default_event",
        FIRST_key="NA",
        FIRST_district_key="NA",
        FIRST_eventType=1,
        start="2023-01-10",
        end="2023-01-11",
        imported=False
    )

def create_org_settings(event: Event):
    return OrgSettings.objects.create(
        allow_photos=True,
        allow_schedule=True,
        new_user_creation="MM",
        new_user_position="OV",
        current_event=event
    )

def create_organization(org_settings: OrgSettings, team: Team):
    return Organization.objects.create(
            name=team.name,
            team=team,
            reg_id="831954f5-4201-4d66-9521-a9ced8e9f16a",
            settings=org_settings
    )


@pytest.fixture
@pytest.mark.django_db
def team_factory():
    return create_team_factory


@pytest.fixture
@pytest.mark.django_db
def create_team_factory(team_factory) -> Team:
    return team_factory()


@pytest.fixture
@pytest.mark.django_db
def create_event_fixture() -> Event:
    return create_event()


@pytest.fixture
@pytest.mark.django_db
def create_org_settings_fixture(create_event_fixture: Event) -> OrgSettings:
    return create_org_settings(create_event_fixture)


@pytest.fixture
@pytest.mark.django_db
def create_organization_fixture(create_org_settings_fixture, create_team_fixture: Team) -> Organization:
    return create_organization(create_org_settings_fixture, create_team_fixture)

