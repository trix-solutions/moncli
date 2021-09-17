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

    def __init__(self, **kwargs):
        super(NumberValue, self).__init__(**kwargs)
    
    @property
    def number(self):
        return self._value

    @number.setter
    def number(self,value):
        if isinstance(value,self.native_type):
            value = self._convert(value)
        elif isinstance(value, self.allow_casts):
            value = self._cast(value) 
        else:
            value = self._format(value)
    
    def format(self):
        return self._format(self.value)

    def _convert(self, value):
        if self.__isint(self.value):
           return int(value)
        elif self.__isfloat(self.value):
           return float(value)
        

    def _cast(self, value):
        if isinstance(value,self.allow_casts):
            if not (isinstance(value,self.native_type)):
                raise ColumnValueError(
                    'invalid_number',
                    self.id,
                    'Unable to convert "{}" to a number value.'.fomrat(value)
                    )
            return self._convert(value)

    def _format(self, value):
        if value == None:
            return SIMPLE_NULL_VALUE
        return self.allow_casts(self.value)

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


class PhoneValue(ComplexNullValue):
    """A phone column value."""


class StatusValue(ComplexNullValue):
    """A status column value."""


class TextValue(SimpleNullValue):
    """A text column value."""

    native_type = str
    allow_casts = (int, float)