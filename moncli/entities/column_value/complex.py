from datetime import datetime

from moncli.config import DATE_FORMAT

from .base import ColumnValue, ComplexNullValue
from .objects import Week
from .base import ColumnValue
from .constants import COMPLEX_NULL_VALUE
from ...error import ColumnValueError


class CheckboxValue(ColumnValue):
    """A checkbox column value."""
    pass


class CountryValue(ColumnValue):
    """A country column value."""
    pass


class HourValue(ColumnValue):
    """An hour column value."""
    pass


class ItemLinkValue(ComplexNullValue):
    """An item link column value."""
    native_type = list
    native_default = []

    def _convert(self, value):
        try:
            list_id = value['linkedPulseIds']
            item_id = [id_value['linkedPulseId'] for id_value in list_id ]
            return item_id
        except KeyError:
            return []

    def _format(self):
        item_ids = []
        list_value = self.value
        for value in list_value:
            try:
                value = int(value)
                item_ids.append(value)
            except ValueError:
                raise ColumnValueError(
                    'invalid_item_id',
                    self.id,
                    'Invalid item ID "{}".'.format(list_value))
        return dict(item_ids=item_ids)

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
            start_date = datetime.strptime(value['week']['startDate'], DATE_FORMAT)
            end_date = datetime.strptime(value['week']['endDate'], DATE_FORMAT)
            return Week(start=start_date, end=end_date)
        except (KeyError,ValueError):
            return COMPLEX_NULL_VALUE
        
    def _cast(self, value):
        try:
            start = value['start']
            end = value['end']
            return Week(start=start,end=end)
        except (AttributeError,KeyError):
            raise ColumnValueError('invalid_week_data', self.id, 'Unable to convert "{}" to Week value.'.format(value))
        
    def _format(self):
        try:
            start_date = self.value.start.date()
            end_date = self.value.end.date()
            start_date = datetime.strftime(start_date, DATE_FORMAT)
            end_date = datetime.strftime(end_date, DATE_FORMAT)
            return {'week': {'startDate': start_date, 'endDate': end_date}}
        except (TypeError,AttributeError):
            return COMPLEX_NULL_VALUE
