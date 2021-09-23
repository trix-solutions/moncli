from .objects import Week
from .base import ColumnValue
from datetime import datetime
from moncli import enums
from datetime import datetime, timedelta
from .base import SimpleNullValue, ComplexNullValue
from .constants import SIMPLE_NULL_VALUE
from ...error import ColumnValueError
from moncli.config import DATE_FORMAT,TIME_FORMAT
import pytz

class CheckboxValue(ColumnValue):
    """A checkbox column value."""
    pass


class CountryValue(ColumnValue):
    """A country column value."""
    pass


class HourValue(ColumnValue):
    """An hour column value."""
    pass


class ItemLinkValue(ColumnValue):
    """An item link column value."""
    pass


class RatingValue(ColumnValue):
    """A rating column value."""
    pass


class TagsValue(ColumnValue):
    """A tags column value."""
    pass


class TimelineValue(ColumnValue):
    """A timeline column value."""
    pass
        

class TimezoneValue(ColumnValue):
    """A timezone column value."""
    pass


class WeekValue(ComplexNullValue):
    """A week column value."""
    
    native_type = Week
    allow_casts = (dict)
    
    
    def _convert(self, value):
        try:
            start = datetime.strptime(value['startDate'], DATE_FORMAT)
            end = datetime.strptime(value['endDate'], DATE_FORMAT)
            return Week(start=start, end=end)
        except KeyError:
            return {}
        
    def _cast(self, value):
        try:
            start_date = value['startDate']
            end_date = value['endDate']
        except (ValueError,KeyError):
            raise ColumnValueError('invalid_week_data', self.id, 'Unable to convert "{}" to Week value of end date.'.format(value))

        return self._convert(value)

        
    def _format(self):
            return {'startDate': self.value.start, 'endDate': self.value.end}
