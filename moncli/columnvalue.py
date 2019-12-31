from typing import List

from schematics.models import Model
from schematics.types import StringType

from .enums import ColumnType, PeopleKind
from .entities import column_value as cv


class NameValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(NameValue, self).__init__(id, title)

        self.name: str = kwargs['name']

    
    def format(self):

        return self.name


class RatingValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(RatingValue, self).__init__(id, title)

        self.rating: int = None

        try:
            self.rating = kwargs['rating']
        except KeyError:
            pass


    def format(self):

        if self.rating is None:
            return {}

        return { 'rating': self.rating }





def create_column_value(id: str, column_type: ColumnType, title: str = None, **kwargs):

    if id:
        kwargs['id'] = id
    if title:
        kwargs['title'] = title

    if column_type == ColumnType.checkbox:
        return cv.CheckboxValue(**kwargs)
    elif column_type == ColumnType.country:
        return cv.CountryValue(**kwargs)
    elif column_type == ColumnType.date:
        return cv.DateValue(**kwargs)    
    elif column_type == ColumnType.dropdown:
        return cv.DropdownValue(**kwargs)
    elif column_type == ColumnType.email:
        return cv.EmailValue(**kwargs)
    elif column_type == ColumnType.hour:
        return cv.HourValue(**kwargs)
    elif column_type == ColumnType.link:
        return cv.LinkValue(**kwargs)    
    elif column_type == ColumnType.long_text:
        return cv.LongTextValue(**kwargs)
    elif column_type == ColumnType.name:
        return NameValue(id, title, name=kwargs['value'])
    elif column_type == ColumnType.numbers:
        return cv.NumberValue(**kwargs)
    elif column_type == ColumnType.people:
        return cv.PeopleValue(**kwargs)
    elif column_type == ColumnType.phone:
        return cv.PhoneValue(**kwargs)
    elif column_type == ColumnType.rating:
        if len(kwargs) == 0:
            return RatingValue(id, title)
        return RatingValue(id, title, **kwargs) 
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