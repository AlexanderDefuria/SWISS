from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Sequence, PostGenerationMethodCall
from django.contrib.auth.models import User

from apps.common.tests.faker import faker
from apps.organization.models import Organization, Event, OrgSettings, OrgMember


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event
        django_get_or_create = ('name',)

    name = LazyAttribute(lambda x: "EVENT  " + faker.unique.city())


class OrgSettingsFactory(DjangoModelFactory):
    class Meta:
        model = OrgSettings
        django_get_or_create = ('allow_photos', 'allow_schedule', 'new_user_creation', 'new_user_position',
                                'current_event')

    allow_photos = True
    allow_schedule = True
    new_user_creation = 'MM'
    new_user_position = 'OV'
    current_event = SubFactory(EventFactory)


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ('name', 'settings')

    name = LazyAttribute(lambda x: "ORG " + faker.unique.company())
    settings = SubFactory(OrgSettingsFactory)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    # Defaults (can be overrided)
    username = Sequence(lambda n: f'user{n}')
    email = LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = PostGenerationMethodCall('set_password', 'password!')


class OrgMemberFactory(DjangoModelFactory):
    class Meta:
        model = OrgMember
        django_get_or_create = ('user', 'organization', 'position')

    user = SubFactory(UserFactory)
    organization = SubFactory(OrganizationFactory)
    position = 'LS'
