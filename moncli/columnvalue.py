from typing import List

from schematics.models import Model
from schematics.types import StringType

from .enums import ColumnType, PeopleKind
from .entities import column_value as cv
from .entities.column_value import StatusValue


class CheckboxValue(cv.ColumnValue):

    def __init__(self, **kwargs):
        super(CheckboxValue, self).__init__(kwargs)
        
        self.checked: bool = False

        try:
            if kwargs['checked'] == 'true':
                self.checked = True
        except KeyError:
            self.checked = False

    
    def format(self):

        if self.checked:
            return { 'checked': 'true' }

        return {}
        

class DateValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(DateValue, self).__init__(id, title)

        try:
            self.date = kwargs['date']
        except KeyError:
            self.date = None

        try: 
            self.time = kwargs['time']
        except KeyError:
            self.time = None


    def format(self):

        if self.date is None:
            return {}

        result = { 'date': self.date }

        if self.time is not None:
            result['time'] = self.time

        return result


class EmailValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(EmailValue, self).__init__(id, title)

        try:
            self.email = kwargs['email']
        except KeyError:
            self.email = None
            self.text = None
            return

        try: 
            self.text = kwargs['text']
        except KeyError:
            self.text = kwargs['email']

    
    def format(self):

        if self.email is None:
            return {}

        return { 'email': self.email, 'text': self.text }


class HourValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(HourValue, self).__init__(id, title)

        try:
            self.hour = kwargs['hour']

            try:
                self.minute = kwargs['minute']
            except KeyError:
                self.minute = 0

        except KeyError:
            self.hour = None
            self.minute = None

    
    def format(self):

        if self.hour is None:
            return {}

        return { 'hour': self.hour, 'minute': self.minute }


class LinkValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(LinkValue, self).__init__(id, title)

        try:
            self.url = kwargs['url']
        except KeyError:
            self.url = None
            self.text = None
            return

        try: 
            self.text = kwargs['text']
        except KeyError:
            self.text = kwargs['url']


    def format(self):

        if self.url is None:
            return {}

        return { 'url': self.url, 'text': self.text }


class NameValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(NameValue, self).__init__(id, title)

        self.name: str = kwargs['name']

    
    def format(self):

        return self.name


class PhoneValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(PhoneValue, self).__init__(id, title)

        try:
            self.phone = kwargs['phone']
            self.country_short_name = kwargs['country_short_name']
        except:
            self.phone = None
            self.country_short_name = None

    
    def format(self):

        if self.phone is None or self.country_short_name is None:
            return {'phone': '', 'countryShortName': ''}

        return { 'phone': self.phone, 'countryShortName': self.country_short_name }


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


class TagsValue(cv.ColumnValue):
    
    def __init__(self, id: str, title: str, **kwargs):
        super(TagsValue, self).__init__(id, title)

        try:
            self.tag_ids = kwargs['tag_ids']
        except KeyError:
            self.tag_ids = None


    def format(self):

        if self.tag_ids is None:
            return { 'tag_ids': [] }

        return { 'tag_ids': self.tag_ids }


class TimelineValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TimelineValue, self).__init__(id, title)

        try:
            self.from_date = kwargs['from_date']
            self.to_date = kwargs['to_date']
        except KeyError:
            self.from_date = None
            self.to_date = None


    def format(self):

        if self.from_date is None or self.to_date is None:
            return {}

        return { 'from': self.from_date, 'to': self.to_date }


class WeekValue(cv.ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(WeekValue, self).__init__(id, title)

        try:
            self.start_date = kwargs['start_date']
            self.end_date = kwargs['end_date']
        except KeyError:
            self.start_date = None
            self.end_date = None


    def format(self):

        if self.start_date is None or self.end_date is None:
            return {}

        return { 'week': { 'startDate': self.start_date, 'endDate': self.end_date }}


class ReadonlyValue(cv.ColumnValue):
    
    def __init__(self, id: str, title, **kwargs):
        super(ReadonlyValue, self).__init__(id, title)

        try:
            self.value = kwargs['value']
        except KeyError: 
            self.value = None

    
    def format(self):

        raise ColumnValueIsReadOnly(self.id, self.title)


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

        if len(kwargs) == 0:
            return DateValue(id, title)

        return DateValue(id, title, **kwargs)


    elif column_type == ColumnType.dropdown:
            return cv.DropdownValue(**kwargs)


    elif column_type == ColumnType.email:

        if len(kwargs) == 0:
            return EmailValue(id, title)

        return EmailValue(id, title, **kwargs)


    elif column_type == ColumnType.hour:

        if len(kwargs) == 0:
            return HourValue(id, title)

        return HourValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.link:

        if len(kwargs) == 0:
            return LinkValue(id, title)

        return LinkValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.long_text:
        return cv.LongTextValue(**kwargs)

    elif column_type == ColumnType.name:
        return NameValue(id, title, name=kwargs['value'])

    elif column_type == ColumnType.numbers:
        return cv.NumberValue(**kwargs)
    elif column_type == ColumnType.people:
        return cv.PeopleValue(**kwargs)


    elif column_type == ColumnType.phone:

        if len(kwargs) == 0:
            return PhoneValue(id, title)

        try:
            phone = kwargs['phone']
        except KeyError:
            phone = None

        try:
            country_short_name = kwargs['countryShortName']
        except KeyError:
            try:
                country_short_name = kwargs['country_short_name']
            except KeyError:
                country_short_name = None

        return PhoneValue(id, title, phone=phone, country_short_name=country_short_name)


    elif column_type == ColumnType.rating:

        if len(kwargs) == 0:
            return RatingValue(id, title)

        return RatingValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.status:
        return cv.StatusValue(**kwargs)

    elif column_type == ColumnType.tags:

        if len(kwargs) == 0:
            return TagsValue(id, title)

        return TagsValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.team:
        return cv.TeamValue(**kwargs)
    elif column_type == ColumnType.text:
        return cv.TextValue(**kwargs)


    elif column_type == ColumnType.timeline:

        if len(kwargs) == 0:
            return TimelineValue(id, title)

        try:
            from_date = kwargs['from']
        except KeyError:
            try:
                from_date = kwargs['from_date']
            except KeyError:
                from_date = None

        try:
            to_date = kwargs['to']
        except KeyError:
            try:
                to_date = kwargs['to_date']
            except KeyError:
                to_date = None

        return TimelineValue(id, title, from_date=from_date, to_date=to_date)
    
    elif column_type == ColumnType.world_clock:
        return cv.TimezoneValue(**kwargs)


    elif column_type == ColumnType.week:

        if len(kwargs) == 0: 
            return WeekValue(id, title)

        try:
            start_date = kwargs['week']['startDate']
        except KeyError:
            try:
                start_date = kwargs['start_date']
            except KeyError:
                start_date = None

        try:
            end_date = kwargs['week']['endDate']
        except KeyError:
            try:
                end_date = kwargs['end_date']
            except:
                end_date = None

        return WeekValue(id, title, start_date=start_date, end_date=end_date)

    
    else:

        return ReadonlyValue(id, title, value=kwargs)


class ColumnValueIsReadOnly(Exception):

    def __init__(self, id: str, title: str):
        self.message = "Cannot format read-only column value '{}' ('{}') for updating.".format(title, id)