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

        try:
            if kwargs['checked'] == 'true':
                self.checked = True
        except KeyError:
            self.checked = False

    
    def format(self):

        if self.checked:
            return { 'checked': 'true' }

        return {}


class CountryValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(CountryValue, self).__init__(id, title)

        try:
            self.country_name = kwargs['country_name']
            self.country_code = kwargs['country_code']
        except:
            self.country_name = None
            self.country_code = None

    
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


class DropdownValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(DropdownValue, self).__init__(id, title)

        try:
            self.ids = kwargs['ids']
        except KeyError:
            self.ids = None

        try: 
            self.label = kwargs['label']
        except KeyError:
            self.label = None


    def format(self):

        if self.label is not None:
            return { 'label': self.label }

        if self.ids is not None:
            return { 'ids': self.ids }

        return {}


class EmailValue(ColumnValue):

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


class HourValue(ColumnValue):

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


class LinkValue(ColumnValue):

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


class LongTextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(LongTextValue, self).__init__(id, title)

        try:
            self.text = kwargs['text']
        except KeyError:
            self.text = None


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

        try:
            value = kwargs['number']

            if self.__isint(value):
                self.number = int(float(value))

            elif self.__isfloat(value):
                self.number = float(value)
        except KeyError:
            pass


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

        try:
            self.persons_and_teams = kwargs['persons_and_teams']
        except KeyError:
            self.persons_and_teams = None

    
    def format(self):

        if self.persons_and_teams is None:
            return {}

        return { 'personsAndTeams': self.persons_and_teams }

    
    def add_people(self, id: int, kind: PeopleKind):

        if self.persons_and_teams is None:
            self.persons_and_teams = []

        self.persons_and_teams.append({ 'id': id, 'kind': kind.name })


    def remove_people(self, id: int):

        people_to_remove = [people for people in self.persons_and_teams if people['id'] == id][0]
        self.persons_and_teams.remove(people_to_remove)

        if len(self.persons_and_teams) == 0:
            self.persons_and_teams = None


class PhoneValue(ColumnValue):

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


class RatingValue(ColumnValue):

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


class StatusValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(StatusValue, self).__init__(id, title)

        if len(kwargs) > 0:
            self.__settings = kwargs['settings']

        try:
            self.change_status_by_index(kwargs['index'])
        except KeyError:
            self.index = None

        try:
            self.change_status_by_label(kwargs['label'])
        except KeyError:
            self.label = None


    def format(self):

        if self.label is not None:
            return { 'label': self.label }

        if self.index is not None:
            return { 'index': self.index }

        return { 'label': ''}


    def change_status_by_index(self, index: int):
        
        self.index = index
        self.label = self.__settings.labels[str(index)]

    def change_status_by_label(self, label: str):
        
        self.label = label
        self.index = self.__settings.get_index(label)


class TagsValue(ColumnValue):
    
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


class TeamValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TeamValue, self).__init__(id, title)

        try:
            self.team_id = kwargs['team_id']
        except KeyError:
            self.team_id = None


    def format(self):

        if self.team_id is not None:
            return { 'team_id': self.team_id }

        return {}


class TextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TextValue, self).__init__(id, title)

        try:
            self.text = kwargs['text']
        except KeyError:
            self.text = None


    def format(self):
        
        if self.text is None:
            return ''

        return self.text


class TimelineValue(ColumnValue):

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


class TimezoneValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TimezoneValue, self).__init__(id, title)

        try:
            self.timezone = kwargs['timezone']
        except:
            self.timezone = None


    def format(self):

        if self.timezone is not None:
            return { 'timezone': self.timezone }

        return {}


class WeekValue(ColumnValue):

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


class ReadonlyValue(ColumnValue):
    
    def __init__(self, id: str, title, **kwargs):
        super(ReadonlyValue, self).__init__(id, title)

        try:
            self.value = kwargs['value']
        except KeyError: 
            self.value = None

    
    def format(self):

        raise ColumnValueIsReadOnly(self.id, self.title)


def create_column_value(id: str, column_type: ColumnType, title: str = None, **kwargs):

    if column_type == ColumnType.checkbox:

        if len(kwargs) == 0:
            return CheckboxValue(id, title)

        return CheckboxValue(id, title, **kwargs)


    elif column_type == ColumnType.country:

        if len(kwargs) == 0:
            return CountryValue(id, title)

        try:
            country_name = kwargs['country_name']
        except KeyError:
            try:
                country_name = kwargs['countryName']
            except KeyError:
                country_name = None

        try:
            country_code = kwargs['country_code']
        except KeyError:
            try:
                country_code = kwargs['countryCode']
            except KeyError:
                country_code = None

        return CountryValue(id, title, country_name=country_name, country_code=country_code)


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
            return DropdownValue(id, title, ids=kwargs['ids'])


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
        return NameValue(id, title, name=kwargs['value'])


    elif column_type == ColumnType.numbers:

        if len(kwargs) == 0:
            return NumberValue(id, title)

        return NumberValue(id, title, number=kwargs['value'])


    elif column_type == ColumnType.people:

        if len(kwargs) == 0:
            return PeopleValue(id, title)

        try:
            persons_and_teams = kwargs['personsAndTeams']
        except KeyError:
            try:
                persons_and_teams = kwargs['persons_and_teams']
            except KeyError:
                persons_and_teams = None

        return PeopleValue(id, title, persons_and_teams=persons_and_teams)


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

        if len(kwargs) == 0:
            return StatusValue(id, title)

        if kwargs.__contains__('label'):
            return StatusValue(id, title, label=kwargs['label'], settings=kwargs['settings'])

        if kwargs.__contains__('index'):
            return StatusValue(id, title, index=kwargs['index'], settings=kwargs['settings'])


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

        return TextValue(id, title, text=kwargs['value'])


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

        if len(kwargs) == 0:
            return TimezoneValue(id, title)

        return TimezoneValue(id, title, **kwargs)


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