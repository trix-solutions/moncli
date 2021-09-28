from datetime import datetime

from moncli.config import DATE_FORMAT

from .base import ColumnValue, ComplexNullValue
from .objects import Week, Timeline, Country
from .base import ColumnValue
from .constants import COMPLEX_NULL_VALUE
from ...error import ColumnValueError


class CheckboxValue(ComplexNullValue):
    """A checkbox column value."""
    
    native_type = bool
    native_default = False
    allow_casts = (int, str)

    def _convert(self, value):
        try:
            if value['checked'] == 'true':
                return True
        except KeyError:
            return False

    def _format(self):
        if self.value:
            return {'checked': 'true'}
        return COMPLEX_NULL_VALUE

class CountryValue(ComplexNullValue):
    """A country column value."""
    
    native_type = Country
    allow_casts = (dict)

    def _convert(self, value):
        try:
            name = value['countryName']
            code = value['countryCode']
            return Country(name=name, code=code)
        except KeyError:
            raise ColumnValueError('invalid_country_data', self.id, 'Unable to convert "{}" to Country value.'.format(value))


    def _cast(self, value):
        try:
            if isinstance(value, dict):
                name = value['name']
                code = value['code']
                return Country(name=name, code=code)
        except KeyError:
            raise ColumnValueError('invalid_country_data', self.id, 'Unable to convert "{}" to Country value.'.format(value))


    def _format(self):
        if (self.value.name == None) or (self.value.code == None):
            return COMPLEX_NULL_VALUE
        return {'countryName': self.value.name, 'countryCode': self.value.code}




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

class RatingValue(ComplexNullValue):
    """A rating column value."""
    native_type = int
    allow_cast = (str)

    def _convert(self, value):
        return value['rating']
    
    def _format(self):
        return { 'rating': self.value }
        
class TagsValue(ColumnValue):
    """A tags column value."""
    pass


class TimelineValue(ComplexNullValue):
    """A timeline column value."""
    
    native_type = Timeline
    allow_casts = (dict)

    def _convert(self,value):
        from_date = datetime.strptime(value['from'], DATE_FORMAT)
        to_date = datetime.strptime(value['to'], DATE_FORMAT)
        try:
            if value['visualization_type']:
                is_milestone = True
                return Timeline(from_date=from_date,to_date=to_date,is_milestone=is_milestone)
        except KeyError:
            return Timeline(from_date=from_date,to_date=to_date)
    
    def _cast(self, value):
        try:
            from_date = value['from']
            to_date = value['to']
            if isinstance(from_date, str):
                from_date = datetime.strptime(from_date, DATE_FORMAT)
            if isinstance(to_date, str):
                to_date = datetime.strptime(to_date, DATE_FORMAT)
            if isinstance(value,dict):
                return Timeline(
                    from_date,
                    to_date)
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
