from django.db.models.fields import __init__
from django.db import models


class PositionField(models.Field):

    description = "Position on the field for use in auto"

    def __init__(self, x_pos, y_pos, separator=",", *args, **kwargs):
        self.x_pos = x_pos
        self.y_pos = y_pos

        kwargs['max_length'] = 104
        self.separator = separator
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.separator != ",":
            kwargs['separator'] = self.separator
        del kwargs["max_length"]
        return name, path, args, kwargs

    def get_prep_value(self, value):
        return str(''.join([''.join(l) for l in (value.x_pos, value.y_pos)]))

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            return connection.Database.Binary(value)
        return value

