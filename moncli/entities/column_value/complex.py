from datetime import datetime
from moncli.entities.column_value.constants import COMPLEX_NULL_VALUE
from moncli.config import DATE_FORMAT
from moncli.error import ColumnValueError
from .base import ColumnValue, ComplexNullValue
from ..column_value import Timeline

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
                                    'Invalid item ID "{}".'.format(list_value)
                                    )
        return dict(item_ids=item_ids)

class RatingValue(ColumnValue):
    """A rating column value."""
    pass


class TagsValue(ColumnValue):
    """A tags column value."""
    pass


class TimelineValue(ComplexNullValue):
    """A timeline column value."""
    
    native_type = Timeline
    allow_casts = (dict)


    def _convert(self,value):
        from_date = value['from']
        to_date = value['to']
        try:
            if value['visualization_type']:
                is_milestone = True
                return Timeline(from_date=from_date,to_date=to_date,is_milestone=is_milestone)
        except KeyError:
            return Timeline(from_date=from_date,to_date=to_date)
    
    def _cast(self, value):
        try:
            if isinstance(value,dict):
                return self._convert(value)
        except KeyError:
            raise ColumnValueError(
                'invalid_timeline_data',
                self.id,
                'Unable to convert "{}" to Timeline value.'.format(value)
            ) 

    def _format(self):
        try:
            from_date = datetime.strftime(self.value.from_date,DATE_FORMAT)
            to_date = datetime.strftime(self.value.to_date,DATE_FORMAT)
            if from_date > to_date :
                raise ColumnValueError(
                    'invalid_timeline_dates',
                    self.id,
                    'Timeline from date cannot be after timeline to date.'
                )
            if from_date and to_date:
                return {
                    'from': from_date,
                    'to' : to_date
                }
        except TypeError:
            return COMPLEX_NULL_VALUE

class TimezoneValue(ColumnValue):
    """A timezone column value."""
    pass


class WeekValue(ColumnValue):
    """A week column value."""
    pass