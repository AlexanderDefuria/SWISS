import factory
from django.contrib.auth.models import User
from apps.common.tests.faker import faker

from apps.organizations.models import Organization, Event, OrgSettings, OrgMember



class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
        django_get_or_create = ('name',)

    name = 'event' + faker.unique.name()


class OrgSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrgSettings
        django_get_or_create = ('allow_photos', 'allow_schedule', 'new_user_creation', 'new_user_position',
                                'current_event')

    allow_photos = True
    allow_schedule = True
    new_user_creation = 'MM'
    new_user_position = 'OV'
    current_event = factory.SubFactory(EventFactory)


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ('name', 'settings')

    name = 'Organization ' + faker.unique.name()
    settings = factory.SubFactory(OrgSettingsFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Defaults (can be overrided)
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password!')



class OrgMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrgMember
        django_get_or_create = ('user', 'organization', 'position')

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    position = 'LS'
