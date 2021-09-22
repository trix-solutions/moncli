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
    native_type = str
    allow_casts = (int, str)

    def _convert(self, value):
        settings = self.settings
        labels = settings['labels']
        index = str(value['index'])
        value = labels[index]  
        return value
    
    def _cast(self, value):
        if isinstance(value,int):
            index = str(value)
            labels = self.settings['labels']
            try:
                value = labels[index]
                return value
            except KeyError:
                raise ColumnValueError( 'invalid_status_index',self.id )
        if isinstance(value,str):
            labels = self.settings['labels']
            try:
                int_value = int(value)
                label = labels[value]
                return label
            except ValueError:
                if value in labels.values():
                    return value
                raise ColumnValueError( 'invalid_status_index',self.id,
                                        'Cannot find a status with the following index "{}".format(value)' )
        
    def _format(self):
        if self.value == None:
            return {}
        index = None
        labels = self.settings['labels']
        for key, value in labels.items():
         if self.value == value:
             index= int(key)
        return dict(index=index)

class TextValue(SimpleNullValue):
    """A text column value."""

    native_type = str
    allow_casts = (int, float)