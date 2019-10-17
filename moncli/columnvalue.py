from typing import List

from .enums import ColumnType, PeopleKind


class ColumnValue():

    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title

    def format(self):
        pass


class CheckboxValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(CheckboxValue, self).__init__(id, title)
        
        self.checked: bool = False

        if kwargs.__contains__('checked') and kwargs['checked'] == 'true':
            self.checked = True

    
    def format(self):

        if self.checked:
            return { 'checked': 'true' }

        return {}


class CountryValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(CountryValue, self).__init__(id, title)

        self.country_code = None
        self.country_name = None

        for key, value in kwargs.items():

            if key == 'country_code':
                self.country_code = value

            elif key == 'country_name':
                self.country_name = value

    
    def format(self):

        if self.country_code is None or self.country_name is None:
            return {}

        return {
            'countryCode': self.country_code,
            'countryName': self.country_name
        }
        

class DateValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(DateValue, self).__init__(id, title)

        self.date = None
        self.time = None

        for key, value in kwargs.items():

            if key == 'date':
                self.date = value

            elif key == 'time':
                self.time = value


    def format(self):

        if self.date is None:
            return {}

        result = { 'date': self.date }

        if self.time is not None:
            result['time'] = self.time

        return result


class DropdownValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(DropdownValue, self).__init__(id, title)

        self.ids: List[int] = None
        self.label: str = None

        for key, value in kwargs.items():

            if key == 'ids':
                self.ids = value

            elif key == 'label':
                self.label = value


    def format(self):

        if self.label is not None:
            return { 'label': self.label }

        if self.ids is not None:
            return { 'ids': self.ids }

        return {}


class EmailValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(EmailValue, self).__init__(id, title)

        self.email = None
        self.text = None

        for key, value in kwargs.items():

            if key == 'email':
                self.email = value

            elif key == 'text':
                self.text = value

    
    def format(self):

        if self.email is None:
            return {}

        result = { 'email': self.email }

        if self.text is None:
            result['text'] = self.email
        else:
            result['text'] = self.text

        return result


class HourValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(HourValue, self).__init__(id, title)

        self.hour = None
        self.minute = 0

        if kwargs.__contains__('hour'):
            self.hour = kwargs['hour']
            self.minute = kwargs['minute']

    
    def format(self):

        if self.hour is None:
            return {}

        return { 'hour': self.hour, 'minute': self.minute }


class LinkValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(LinkValue, self).__init__(id, title)

        self.url = None
        self.text = None

        for key, value in kwargs.items():

            if key == 'url':
                self.url = value

            elif key == 'text':
                self.text = value


    def format(self):

        if self.url is None:
            return {}

        result = { 'url': self.url}

        if self.text is None:
            result['text'] = self.url
        else:
            result['text'] = self.text

        return result


class LongTextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(LongTextValue, self).__init__(id, title)

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value


    def format(self):

        if self.text is None:
            return {}

        return { 'text': self.text}


class NameValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(NameValue, self).__init__(id, title)

        self.name: str = kwargs['name']

    
    def format(self):

        return self.name
        

class NumberValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(NumberValue, self).__init__(id, title)

        self.number = None

        for key, value in kwargs.items():

            if key == 'number':
                if self.__isint(value):
                    self.number = int(value)

                elif self.__isfloat(value):
                    self.number = float(value)


    def format(self):

        if self.number is not None:
            return str(self.number)

        return ''


    def __isfloat(self, value):

        try:
            float(value)

        except ValueError:
            return False

        return True

    
    def __isint(self, value):

        try:
            a = float(value)
            b = int(a)

        except ValueError:
            return False

        return a == b


class PeopleValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(PeopleValue, self).__init__(id, title)

        self.persons_and_teams: list = None

        for key, value in kwargs.items():

            if key == 'persons_and_teams':
                self.persons_and_teams = value

    
    def format(self):

        if self.persons_and_teams is None:
            return {}

        return { 'personsAndTeams': self.persons_and_teams }

    
    def add_people(self, id: int, kind: PeopleKind):

        if self.persons_and_teams is None:
            self.persons_and_teams = []

        self.persons_and_teams.append({ 'id': id, 'kind': kind.name })


    def remove_people(self, id: int):

        people_to_remove = [people for people in self.persons_and_teams if people['id'] == id]
        self.persons_and_teams.remove(people_to_remove)

        if len(self.persons_and_teams) == 0:
            self.persons_and_teams = None


class PhoneValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(PhoneValue, self).__init__(id, title)

        self.phone = None
        self.country_short_name = None

        if kwargs.__contains__('phone') or kwargs.__contains__('country_short_name'):
            self.phone = kwargs['phone']
            self.country_short_name = kwargs['country_short_name']

    
    def format(self):

        if self.phone is None or self.country_short_name is None:
            return {'phone': '', 'countryShortName': ''}

        return { 'phone': self.phone, 'countryShortName': self.country_short_name }


class RatingValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(RatingValue, self).__init__(id, title)

        self.rating: int = None

        if kwargs.__contains__('rating'):
            self.rating = kwargs['rating']


    def format(self):

        if self.rating is None:
            return {}

        return { 'rating': self.rating }


class StatusValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(StatusValue, self).__init__(id, title)

        self.index = None
        self.label = None

        for key, value in kwargs.items():

            if key == 'index':
                self.index: int = value

            elif key == 'label':
                self.label: str = value


    def format(self):

        if self.label is not None:
            return { 'label': self.label }

        if self.index is not None:
            return { 'index': self.index }

        return { 'label': ''}


class TagsValue(ColumnValue):
    
    def __init__(self, id: str, title: str, **kwargs):
        super(TagsValue, self).__init__(id, title)

        self.tag_ids = None

        for key, value in kwargs.items():

            if key == 'tag_ids':
                self.tag_ids = value


    def format(self):

        if self.tag_ids is None:
            return { 'tag_ids': [] }

        return { 'tag_ids': self.tag_ids }


class TeamValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TeamValue, self).__init__(id, title)

        self.team_id = None

        for key, value in kwargs.items():

            if key == 'team_id':
                self.team_id: int = value


    def format(self):

        if self.team_id is not None:
            return { 'team_id': self.team_id }

        return {}


class TextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TextValue, self).__init__(id, title)

        for key, value in kwargs.items():

            if key == 'text':
                self.text: str = value


    def format(self):
        
        if self.text is None:
            return ''

        return self.text


class TimelineValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TimelineValue, self).__init__(id, title)

        self.from_date = None
        self.to_date = None

        for key, value in kwargs.items():

            if key == 'from':
                self.from_date = value

            elif key == 'to':
                self.to_date = value


    def format(self):

        if self.from_date is None or self.to_date is None:
            return {}

        return { 'from': self.from_date, 'to': self.to_date }


class TimezoneValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TimezoneValue, self).__init__(id, title)

        self.timezone = None

        for key, value in kwargs.items():

            if key == 'timezone':
                self.timezone = value


    def format(self):

        if self.timezone is not None:
            return { 'timezone': self.timezone }

        return {}


class WeekValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(WeekValue, self).__init__(id, title)

        self.start_date = None
        self.end_date = None

        if kwargs.__contains__('week') and kwargs['week'] != '':
            self.start_date = kwargs['week']['startDate']
            self.end_date = kwargs['week']['endDate']


    def format(self):

        if self.start_date is None or self.end_date is None:
            return {}

        return { 'week': { 'startDate': self.start_date, 'endDate': self.end_date }}


def create_column_value(id: str, column_type: ColumnType, title: str = None, **kwargs):

    if column_type == ColumnType.checkbox:

        if len(kwargs) == 0:
            return CheckboxValue(id, title)

        return CheckboxValue(id, title, checked=kwargs['checked'])


    elif column_type == ColumnType.country:

        if len(kwargs) == 0:
            return CountryValue(id, title)

        return CountryValue(id, title, country_code=kwargs['countryCode'], country_name=kwargs['countryName'])


    elif column_type == ColumnType.date:

        if len(kwargs) == 0:
            return DateValue(id, title)

        return DateValue(id, title, **kwargs)


    elif column_type == ColumnType.dropdown:

        if len(kwargs) == 0:
            return DropdownValue(id, title)

        if kwargs.__contains__('label'):
            return DropdownValue(id, title, label=kwargs['label'])

        if kwargs.__contains__('ids'):
            return DropdownValue(id, title, label_id=kwargs['ids'])


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

        if len(kwargs) == 0:
            return LongTextValue(id, title)

        return LongTextValue(id, title, **kwargs)


    elif column_type == ColumnType.name:
        return NameValue(id, title, name=kwargs)


    elif column_type == ColumnType.numbers:

        if len(kwargs) == 0:
            return NumberValue(id, title)

        return NumberValue(id, title, number=kwargs)


    elif column_type == ColumnType.people:

        if len(kwargs) == 0:
            return PeopleValue(id, title)

        return PeopleValue(id, title, persons_and_teams=kwargs['personsAndTeams'])


    elif column_type == ColumnType.phone:

        if len(kwargs) == 0:
            return PhoneValue(id, title)

        return PhoneValue(id, title, phone=kwargs['phone'], country_short_name=kwargs['countryShortName'])


    elif column_type == ColumnType.rating:

        if len(kwargs) == 0:
            return RatingValue(id, title)

        return RatingValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.status:

        if len(kwargs) == 0:
            return StatusValue(id, title)

        if kwargs.__contains__('label'):
            return StatusValue(id, title, label=kwargs['label'])

        if kwargs.__contains__('index'):
            return StatusValue(id, title, index=kwargs['index'])


    elif column_type == ColumnType.tags:

        if len(kwargs) == 0:
            return TagsValue(id, title)

        return TagsValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.team:

        if len(kwargs) == 0:
            return TeamValue(id, title)

        return TeamValue(id, title, **kwargs)


    elif column_type == ColumnType.text:

        if len(kwargs) == 0:
            return TextValue(id, title)

        return TextValue(id, title, text=kwargs)


    elif column_type == ColumnType.timeline:

        if len(kwargs) == 0:
            return TimelineValue(id, title)

        return TimelineValue(id, title, **kwargs)
    
    
    elif column_type == ColumnType.world_clock:

        if len(kwargs) == 0:
            return TimezoneValue(id, title)

        return TimezoneValue(id, title, **kwargs)


    elif column_type == ColumnType.week:

        if len(kwargs) == 0: 
            return WeekValue(id, title)

        return WeekValue(id, title, **kwargs)

    
    else:
        raise InvalidColumnValueType(column_type)

class InvalidColumnValueType(Exception):

    def __init__(self, column_type: ColumnType):
        self.message = "Cannot create column value with type '{}'.".format(column_type._name_)