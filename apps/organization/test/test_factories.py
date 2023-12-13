from django.test import TestCase

from apps.organization.models import Organization
from apps.organization.test.factories import OrganizationFactory


class OrganizationFactoryTest(TestCase):

    def test_team_creation(self):
        a = OrganizationFactory()
        self.assertTrue(isinstance(a, Organization))
        b = OrganizationFactory()
        self.assertTrue(isinstance(b, Organization))
        assert a != b
        assert a.name != b.name

