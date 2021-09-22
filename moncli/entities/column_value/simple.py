from moncli.error import ColumnValueError
from moncli.entities.column_value.objects import PersonOrTeam
from moncli import enums

from .base import SimpleNullValue, ComplexNullValue
from .constants import SIMPLE_NULL_VALUE
from ...error import ColumnValueError

class DateValue(ComplexNullValue):
    """A date column value."""
    pass
        

class DropdownValue(ComplexNullValue):
    """A dropdown column value."""
    native_type = list
    native_default = []

    def _convert(self, value):
        labels = self.settings['labels']
        ids = value['ids']
        label_list = []

        for item in labels:
            if item['id'] in ids:
                label_list.append(item['name'])   
        return label_list

    def _format(self):
        labels = self.settings['labels']
        label_ids = [label['id'] for label in labels]
        label_names = [label['name'] for label in labels]
        ids = []
        for value in self.value:
            if isinstance(value,(int,str)):
                try:
                    value = int(value)
                    if value in label_ids:
                        ids.append(value)
                    else:
                        raise ColumnValueError(
                                'invalid_dropdown_index',
                                self.id,
                                'Dropdown does not contain index "{}".'.format(self.value)
                              )
                except ValueError:
                    if value in label_names:
                        list_id = [label['id'] for label in labels if label['name']==value][0]
                        ids.append(list_id)
                    else:
                        raise ColumnValueError(
                                'invalid_dropdown_label',
                                self.id,
                                'Dropdown does not contain label "{}".'.format(self.value)
                                   )
        return dict(ids=ids)    


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

    native_type = (int,float)
    allow_casts = (str)
    
    def _convert(self, value):
        if self.__isint(value):
           return int(value)
        elif self.__isfloat(value):
           return float(value)
        

    def _cast(self, value):
        if isinstance(value,self.allow_casts):
            if self.__isint(value):
                return int(value)
            elif self.__isfloat(value):
                return float(value)
        raise ColumnValueError(
                'invalid_number',
                self.id,
                'Unable to convert "{}" to a number value.'.format(value)
                )

    def _format(self):
        if self.value != None:
            return self.allow_casts(self.value)
        return SIMPLE_NULL_VALUE

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
        return_list = []
        value_list = value['personsAndTeams']
        for value_data in value_list:
            return_data = PersonOrTeam(
                            value_data['id'], 
                            enums.PeopleKind[value_data['kind']]
                            )
            return_list.append(return_data)
        return return_list
    
    def _format(self):
        personsAndTeams = []
        for list_item in self.value:
            if not isinstance(list_item,PersonOrTeam):
                raise ColumnValueError(
                    'invalid_people_value',
                    self.id,
                    'Invalid person or team value "{}".'.format(list_item)
                )
            id = list_item.id
            peopleKind = list_item.kind
            personsAndTeams.append({ 'id': id, 'kind': peopleKind.name })
        return {'personsAndTeams': personsAndTeams}


class PhoneValue(ComplexNullValue):
    """A phone column value."""


class StatusValue(ComplexNullValue):
    """A status column value."""


class TextValue(SimpleNullValue):
    """A text column value."""

    native_type = str
    allow_casts = (int, float)