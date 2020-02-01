from django.db.models.fields import __init__
from django.db import models


class PositionField(models.TextField):

    description = "Position on the field for use in auto"

    def __init__(self, coordinates, *args, **kwargs):
        self.coordinates = coordinates
        self.separator = ","
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_coordinates():
        return 0

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.separator != ",":
            kwargs['separator'] = self.separator
        return name, path, args, kwargs



