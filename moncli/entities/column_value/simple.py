from moncli.error import ColumnValueError
from moncli.entities.column_value.objects import PersonOrTeam
from .base import SimpleNullValue, ComplexNullValue
from moncli import enums

class DateValue(ComplexNullValue):
    """A date column value."""
    pass
        

class DropdownValue(ComplexNullValue):
    """A dropdown column value."""
    pass


class EmailValue(ComplexNullValue):
    """An email column value."""
    pass

class LinkValue(ComplexNullValue):
    """A link column value."""
    pass


class LongTextValue(ComplexNullValue):
    """A long text column value."""
    pass


class NumberValue(SimpleNullValue):
    """A number column value."""

    def __isfloat(self, value):
        """Is the value a float."""
        try:
            float(value)
        except ValueError:
            return False
        return True
  
    def __isint(self, value):
        """Is the value an int."""
        try:
            a = float(value)
            b = int(a)
        except ValueError:
            return False
        return a == b


class PeopleValue(ComplexNullValue):
    """A people column value."""

    native_type = list
    native_default = []
    allow_casts = ()

    def _convert(self, value):
        value_list = value['personsAndTeams']
        return [{PersonOrTeam(value_data['id'], enums.PeopleKind[value_data['kind']])} for value_data in value_list]
    
    def _format(self):
        personsAndTeams = []
        for list_item in self.value:
            if not isinstance(list_item,PersonOrTeam):
                raise ColumnValueError(
                    'invalid_people_value',
                    self.id,
                    'Invalid person or team value "{}".'.format(list_item)
                )
            personsAndTeams = list_item.id
            peopleKind = list_item.kind
            personsAndTeams.append({ 'personsAndTeams': personsAndTeams, 'peopleKind':peopleKind })
        return personsAndTeams


class PhoneValue(ComplexNullValue):
    """A phone column value."""


class StatusValue(ComplexNullValue):
    """A status column value."""


class TextValue(SimpleNullValue):
    """A text column value."""

    native_type = str
    allow_casts = (int, float)