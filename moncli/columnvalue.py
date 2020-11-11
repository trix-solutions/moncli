import deprecated, warnings

from .enums import ColumnType
from .entities import column_value as cv


# Deprecation message
# warnings.simplefilter('always', DeprecationWarning)
warnings.warn(
    'This module will be deprecated soon.  Please use moncli.entities.column_value instead',
    PendingDeprecationWarning)

class CheckboxValue(cv.CheckboxValue):
    pass

class CountryValue(cv.CountryValue):
    pass

class DateValue(cv.DateValue):
    pass

class DropdownValue(cv.DropdownValue):
    pass

class EmailValue(cv.EmailValue):
    pass

class FileValue(cv.FileValue):
    pass

class HourValue(cv.HourValue):
    pass

class LinkValue(cv.LinkValue):
    pass

class LongTextValue(cv.LongTextValue):
    pass

class NameValue(cv.NameValue):
    pass

class NumberValue(cv.NumberValue):
    pass

class PeopleValue(cv.PeopleValue):
    pass

class PhoneValue(cv.PhoneValue):
    pass

class RatingValue(cv.RatingValue):
    pass

class StatusValue(cv.StatusValue):
    pass

class TagsValue(cv.TagsValue):
    pass

class TeamValue(cv.TeamValue):
    pass

class TextValue(cv.TextValue):
    pass

class TimelineValue(cv.TimelineValue):
    pass

class TimezoneValue(cv.TimezoneValue):
    pass

class WeekValue(cv.WeekValue):
    pass

class ReadonlyValue(cv.ReadonlyValue):
    pass

@deprecated.deprecated(version='1.0.0', reason="Please use moncli.entities.create_column_value instead.")
def create_column_value(id: str, column_type: ColumnType, title: str = None, **kwargs):

    if id:
        kwargs['id'] = id
    if title:
        kwargs['title'] = title

    if column_type == ColumnType.checkbox:
        return CheckboxValue(**kwargs)
    elif column_type == ColumnType.country:
        return cv.CountryValue(**kwargs)
    elif column_type == ColumnType.date:
        return cv.DateValue(**kwargs)    
    elif column_type == ColumnType.dropdown:
        return cv.DropdownValue(**kwargs)
    elif column_type == ColumnType.email:
        return cv.EmailValue(**kwargs)
    elif column_type == ColumnType.file:
        return cv.FileValue(**kwargs)
    elif column_type == ColumnType.hour:
        return cv.HourValue(**kwargs)
    elif column_type == ColumnType.link:
        return cv.LinkValue(**kwargs)    
    elif column_type == ColumnType.long_text:
        return cv.LongTextValue(**kwargs)
    elif column_type == ColumnType.name:
        return cv.NameValue(**kwargs)
    elif column_type == ColumnType.numbers:
        return cv.NumberValue(**kwargs)
    elif column_type == ColumnType.people:
        return cv.PeopleValue(**kwargs)
    elif column_type == ColumnType.phone:
        return cv.PhoneValue(**kwargs)
    elif column_type == ColumnType.rating:
        return cv.RatingValue(**kwargs) 
    elif column_type == ColumnType.status:
        return cv.StatusValue(**kwargs)
    elif column_type == ColumnType.tags:
        return cv.TagsValue(**kwargs)
    elif column_type == ColumnType.team:
        return cv.TeamValue(**kwargs)
    elif column_type == ColumnType.text:
        return cv.TextValue(**kwargs)
    elif column_type == ColumnType.timeline:
        return cv.TimelineValue(**kwargs)
    elif column_type == ColumnType.world_clock:
        return cv.TimezoneValue(**kwargs)
    elif column_type == ColumnType.week:
        return cv.WeekValue(**kwargs)
    else:
        return cv.ReadonlyValue(**kwargs)
