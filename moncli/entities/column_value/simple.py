from .base import SimpleNullValue, ComplexNullValue
from .constants import SIMPLE_NULL_VALUE
from ...error import ColumnValueError
from datetime import datetime, timedelta
from moncli.config import DATE_FORMAT,TIME_FORMAT
import pytz
class DateValue(ComplexNullValue):
    """A date column value."""
    native_type = datetime.datetime 
    allow_casts = (int, str)
    has_time = False

    def _convert(self,value):
        try:
            new_time = datetime.strptime(value['time'], TIME_FORMAT)
            new_date = datetime.strptime(value['date'], DATE_FORMAT)
            self.has_time = True
            new_date = pytz.timezone('UTC').localize(new_date)
            new_date = new_date + timedelta(hours=new_time.hours, minutes=new_time.minutes, seconds=new_time.seconds)
            date_value = new_date.astimezone(datetime.now().astimezone().tzinfo) 
            return date_value

        except KeyError:
            new_date = datetime.strptime(value['date'], DATE_FORMAT)
            return new_date
        
    def _cast(self,value):
        if isinstance(value,int):
            try: 
                new_date_value =  datetime.fromtimestamp(value)
                return new_date_value

            except ValueError:
                raise ColumnValueError(
                    'invalid_unix_date',
                     self.id,
                    'Unable to convert "{}" from UNIX timestamp.'.format(value)
                )
        if isinstance(value, str):
            try:
                date=value.split()[0]
                time=value.split()[1]

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


class PhoneValue(ComplexNullValue):
    """A phone column value."""


class StatusValue(ComplexNullValue):
    """A status column value."""


class TextValue(SimpleNullValue):
    """A text column value."""

    native_type = str
    allow_casts = (int, float)