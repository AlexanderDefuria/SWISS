import os
import pytest

from apps.entry.models import *

base_test_dir = os.path.dirname(os.path.realpath(__file__))

def load_fixtures(relative_fixtures) -> list:
    fixtures = []
    for path in relative_fixtures:
        fixtures.append(os.path.join(base_test_dir, path))
    return fixtures


def create_user() -> User:
    user = User.objects.create_user(
        username='test_account_swiss',
        password='passwordtest'
    )
    user.save()
    assert user.username == 'test_account_swiss'
    return user


@pytest.fixture
@pytest.mark.django_db
def team_factory():
    def create_team(
        number=4343,
        name='MaxTech'
    ) -> Team:
        return Team.objects.create(
            number=number,
            name=name
        )
    return create_team


@pytest.fixture
@pytest.mark.django_db
def create_team(team_factory) -> Team:
    return team_factory()


@pytest.fixture
@pytest.mark.django_db
def create_event() -> Event:
    return Event.objects.create(
            name="default_event",
            FIRST_key="NA",
            FIRST_district_key="NA",
            FIRST_eventType=1,
            start="2023-01-10",
            end="2023-01-11",
            imported=False
    )


@pytest.fixture
@pytest.mark.django_db
def create_org_settings(create_event: Event) -> OrgSettings:
    return OrgSettings.objects.create(
        allow_photos=True,
        allow_schedule=True,
        new_user_creation="MM",
        new_user_position="OV",
        current_event=create_event
    )


@pytest.fixture
@pytest.mark.django_db
def create_organization(create_org_settings: OrgSettings, create_team: Team) -> Organization:
    return Organization.objects.create(
            name=create_team.name,
            team=create_team,
            reg_id="831954f5-4201-4d66-9521-a9ced8e9f16a",
            settings=create_org_settings
    )

