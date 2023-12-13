from faker import Faker
from faker_education import SchoolProvider
from faker_biology.taxonomy import ModelOrganism

# This provides us with a consistent faker generator.
faker = Faker()
faker.add_provider(SchoolProvider)
faker.add_provider(ModelOrganism)