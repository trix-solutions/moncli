from datetime import datetime
from importlib import import_module
from json import dumps, loads

from pycountry import countries
from pytz import timezone, exceptions as tzex
from schematics.models import Model
from schematics.types import StringType, IntType

from .. import config, enums, entities as en


SIMPLE_NULL_VALUE = ''
COMPLEX_NULL_VALUE = '{}'

class _ColumnValue(Model):
    id = StringType(required=True)
    title = StringType()
    text = StringType()
    value = StringType()
    additional_info = StringType()

    def __repr__(self):
        return str(self.to_primitive())

    def format(self):
        return self.to_primitive()


class ColumnValue(_ColumnValue):
    null_value = COMPLEX_NULL_VALUE

    def __init__(self, **kwargs):
        super(ColumnValue, self).__init__(kwargs)
        if not self.value:
            self.value = self.null_value

    def set_value(self, *argv, **kwargs): 
        if len(argv) > 0:
            self.value = dumps(argv[0])
        elif len(kwargs) > 0:
            value_obj = loads(self.value)
            for key, value in kwargs.items():
                value_obj[key] = value
            self.value = dumps(value_obj)
        else:
            self.value = self.null_value


class CheckboxValue(ColumnValue):
    def __init__(self, **kwargs):
        super(CheckboxValue, self).__init__(**kwargs)
        
    @property
    def checked(self):
        try:
            return loads(self.value)['checked']
        except KeyError:
            return False

    @checked.setter
    def checked(self, value: bool):
        if value:
            self.set_value(checked=value)
        else:
            self.value = self.null_value
    
    def format(self):
        if self.checked:
            return { 'checked': 'true' }
        return loads(self.null_value)


class CountryValue(ColumnValue):
    def __init__(self, **kwargs):
        super(CountryValue, self).__init__(**kwargs)

    @property
    def country_code(self):
        try:
            return loads(self.value)['countryCode']
        except KeyError:
            return None

    @country_code.setter
    def country_code(self, code):
        country = countries.get(alpha_2=code)
        if not country:
            raise UnknownCountryCodeError(code)
        self.set_value(countryCode=country.alpha_2, countryName=country.name)

    @property
    def country_name(self):
        try:
            return loads(self.value)['countryName']
        except KeyError:
            return None

    @country_name.setter
    def country_name(self, name):
        country = countries.get(name=name)
        if not country:
            raise UnknownCountryNameError(name)
        self.set_value(countryCode=country.alpha_2, countryName=country.name)
 
    def format(self):
        if self.country_code and self.country_name:
            return {
                'countryCode': self.country_code,
                'countryName': self.country_name
            }
        return loads(self.null_value)


class DateValue(ColumnValue):
    def __init__(self, **kwargs):
        super(DateValue, self).__init__(**kwargs)

    @property
    def date(self):
        try:
            return loads(self.value)['date']
        except KeyError:
            return None

    @date.setter
    def date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise DateFormatError(value)

        self.set_value(date=value)

    @property
    def time(self):
        try:
            return loads(self.value)['time']
        except KeyError:
            return None

    @time.setter
    def time(self, value):
        try:
            datetime.strptime(value, '%H:%M:%S')
        except ValueError:
            raise TimeFormatError(value)

        self.set_value(time=value)

    def format(self):
        if self.date:
            result = {'date': self.date}
            if self.time:
                result['time'] = self.time
            return result
        return loads(self.null_value)
        

class DropdownValue(ColumnValue):
    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('dropdown')

        super(DropdownValue, self).__init__(**kwargs)

    @property
    def labels(self):
        ids = loads(self.value)['ids']
        return [label for label in self.__settings.labels if label.id in ids]

    def format(self):
        if len(self.labels) == 0:
            return {}
        return { 'ids': [label.id for label in self.labels] }

    def add_label(self, id: int):
        try:
            label = self.__settings[id]
        except KeyError:
            raise DropdownLabelError('Unable to find dropdown label with ID {}.'.format(str(id)))

        value = loads(self.value)
        if label.id in value['ids']:
            raise DropdownLabelError('Label with ID {} has already been set.'.format(str(id)))
        value['ids'].append(label.id)
        self.value = dumps(value)

        text = self.text.split(', ')
        text.append(label.name)
        self.text = ', '.join(text)

    def remove_label(self, id: int):
        try:
            label = self.__settings[id]
        except KeyError:
            raise DropdownLabelError('Unable to find dropdown label with ID {}.'.format(str(id)))

        value = loads(self.value)
        if label.id not in value['ids']:
            raise DropdownLabelError('Cannot remove unset label with ID {}.'.format(str(id)))
        value['ids'].remove(label.id)
        self.value = dumps(value)

        text = self.text.split(', ')
        text.remove(label.name)
        self.text = ', '.join(text)


class EmailValue(ColumnValue):

    def __init__(self, **kwargs):
        super(EmailValue, self).__init__(**kwargs)

    @property
    def email(self):
        try:
            return loads(self.value)['email']
        except KeyError:
            return None

    @email.setter
    def email(self, value):
        self.set_value(email=value)

    @property
    def email_text(self):
        try:
            return loads(self.value)['text']
        except KeyError:
            return self.email

    @email_text.setter
    def email_text(self, value):
        self.set_value(text=value)
    
    def format(self):
        if self.email:  
            return { 'email': self.email, 'text': self.email_text }
        return {}


class HourValue(ColumnValue):
    def __init__(self, **kwargs):
        super(HourValue, self).__init__(**kwargs)

    @property
    def hour(self):
        try:
            return loads(self.value)['hour']
        except KeyError:
            return None

    @hour.setter
    def hour(self, value: int):
        self.set_value(hour=value)
    
    @property
    def minute(self):
        try:
            return loads(self.value)['minute']
        except KeyError:
            return 0

    @minute.setter
    def minute(self, value: int):
        self.set_value(minute=value)

    def format(self):
        if self.hour:
            return { 'hour': self.hour, 'minute': self.minute }
        return loads(self.null_value)


class LinkValue(ColumnValue):
    def __init__(self, **kwargs):
        super(LinkValue, self).__init__(**kwargs)

    @property
    def url(self):
        try:
            return loads(self.value)['url']
        except KeyError:
            return None

    @url.setter
    def url(self, value):
        self.set_value(url=value)

    @property
    def url_text(self):
        try:
            return loads(self.value)['text']
        except KeyError:
            return self.url

    @url_text.setter
    def url_text(self, value):
        return self.set_value(text=value)

    def format(self):
        if self.url:
            return { 'url': self.url, 'text': self.url_text }
        return loads(self.null_value)


class LongTextValue(ColumnValue):
    def __init__(self, **kwargs):
        super(LongTextValue, self).__init__(**kwargs)

    @property
    def long_text(self):
        try:
            return loads(self.value)['text']
        except KeyError:
            return None
    
    @long_text.setter
    def long_text(self, value):
        if value:
            self.set_value(text=value)
        else:
            self.value = dumps(self.null_value)

    def format(self):
        if self.long_text:
            return {'text': self.long_text}
        return loads(self.null_value)


class NameValue(ColumnValue):
    null_value = ''

    def __init__(self, **kwargs):
        super(NameValue, self).__init__(**kwargs)

    @property
    def name(self):
        return loads(self.value)

    @name.setter
    def name(self, value):
        if value:
            self.set_value(value)
        else:
            self.set_value(self.null_value)
    
    def format(self):
        return self.name


class NumberValue(ColumnValue):
    null_value = ''

    def __init__(self, **kwargs):
        super(NumberValue, self).__init__(**kwargs)

    @property
    def number(self):
        if self.value is self.null_value:
            return None
        value = loads(self.value)
        if self.__isint(value):
            return int(value)
        if self.__isfloat(value):
            return float(value)

    @number.setter
    def number(self, value):
        if not self.__isint(value) and not self.__isfloat(value):
            raise NumberValueError()
        self.value = dumps(value)

    def format(self):
        if self.number:
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
    def __init__(self, **kwargs):
        super(PeopleValue, self).__init__(**kwargs)
    
    @property
    def persons_and_teams(self):
        if self.value:
            return loads(self.value)['personsAndTeams']
        return self.value  

    def format(self):
        if self.persons_and_teams:
            return { 'personsAndTeams': self.persons_and_teams }
        return {}

    def add_people(self, person_or_team):
        if type(person_or_team) is type(en.User):
            kind = enums.PeopleKind.person
        elif type(person_or_team) is type(en.Team):
            kind = enums.PeopleKind.team
        persons_and_teams = self.persons_and_teams
        persons_and_teams.append({'id': person_or_team.id, 'kind': kind.name})
        self.set_value(personsAndTeams=persons_and_teams)

    def remove_people(self, id: int):
        persons_and_teams = []
        for entity in self.persons_and_teams:
            if entity.id != id:
                persons_and_teams.append(entity)
        self.set_value(personsAndTeams=persons_and_teams)


class PhoneValue(ColumnValue):
    def __init__(self, **kwargs):
        super(PhoneValue, self).__init__(**kwargs)

    @property
    def phone(self):
        try:
            return loads(self.value)['phone']
        except KeyError:
            return None

    @phone.setter
    def phone(self, value):
        self.set_value(phone=value)

    @property
    def country_short_name(self):
        try:
            return loads(self.value)['countryShortName']
        except KeyError:
            return None

    @country_short_name.setter
    def country_short_name(self, value):
        country = countries.get(alpha_2=value)
        if not country:
            raise UnknownCountryCodeError(value)
        self.set_value(countryShortName=value)
    
    def format(self):
        if self.phone and self.country_short_name:
            return { 'phone': self.phone, 'countryShortName': self.country_short_name }
        return { 'phone': '', 'countryShortName': '' }


class RatingValue(ColumnValue):
    def __init__(self, **kwargs):
        super(RatingValue, self).__init__(**kwargs)

    @property
    def rating(self):
        try:
            return loads(self.value)['rating']
        except KeyError:
            return None

    @rating.setter
    def rating(self, value: int):
        if value:
            self.set_value(rating=value)
        else:
            self.set_value()

    def format(self):
        if self.rating:
            return { 'rating': self.rating }
        return loads(self.null_value)


class StatusValue(ColumnValue):
    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('status')

        super(StatusValue, self).__init__(**kwargs)

    @property
    def index(self):
        try:
            return loads(self.value)['index']
        except KeyError: 
            return None

    @index.setter
    def index(self, index: int):
        self.set_value(index=index, label=self.__settings.labels[str(index)])

    @property
    def label(self):
        try:
            return loads(self.value)['label']
        except KeyError:
            try:
                return loads(self.additional_info)['label']
            except KeyError:
                return None

    @label.setter
    def label(self, label: str):    
        self.set_value(index=self.__settings.get_index(label), label=label)

    def format(self):
        if self.index:
            return {'index': self.index}
        return loads(self.null_value)
        

class TagsValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TagsValue, self).__init__(**kwargs)

    @property
    def tag_ids(self):
        try:
            return loads(self.value)['tag_ids']
        except KeyError:
            return []

    def add(self, tag_id: int):
        tag_ids = self.tag_ids
        tag_ids.append(tag_id)
        self.set_value(tag_ids=tag_ids)

    def remove(self, tag_id: int):
        tag_ids = self.tag_ids
        tag_ids.remove(tag_id)
        self.set_value(tag_ids=tag_ids)

    def format(self):
        return { 'tag_ids': self.tag_ids }


class TeamValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TeamValue, self).__init__(**kwargs)

    @property 
    def team_id(self):
        try:
            return loads(self.value)['team_id']
        except KeyError:
            return None

    @team_id.setter
    def team_id(self, value):
        if value:
            self.set_value(team_id=value)
        else:
            self.value = self.null_value

    def format(self):
        if self.team_id is not None:
            return { 'team_id': self.team_id }
        return {}


class TextValue(ColumnValue):
    null_value = ''
    def __init__(self, **kwargs):
        super(TextValue, self).__init__(**kwargs)

    @property
    def text_value(self):
        if self.value:
            return loads(self.value)
        return self.value

    @text_value.setter
    def text_value(self, value):
        if value:
            self.value = dumps(value)
        else:
            self.value = dumps(self.null_value)

    @text_value.setter
    def text_value(self, value: str):
        if value:
            self.text = value
            self.value = dumps(value)
        else:
            self.text = ''
            self.value = self.null_value

    def format(self):
        if self.value is self.null_value:
            return self.value
        return loads(self.value)


class TimelineValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TimelineValue, self).__init__(**kwargs)

    @property
    def from_date(self):
        try:
            return loads(self.value)['from']
        except KeyError:
            return None

    @from_date.setter
    def from_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise DateFormatError(value)

        self.set_value(**{'from': value})

    @property
    def to_date(self):
        try:
            return loads(self.value)['to']
        except KeyError:
            return None

    @to_date.setter
    def to_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise DateFormatError(value)

        self.set_value(to=value)

    def format(self):
        if self.from_date and self.to_date:
            return { 'from': self.from_date, 'to': self.to_date }
        return loads(self.null_value)
        

class TimezoneValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TimezoneValue, self).__init__(**kwargs)

    @property
    def timezone(self):
        try:
            return loads(self.value)['timezone']
        except KeyError:
            return None

    @timezone.setter
    def timezone(self, value):
        if not value:
            self.value = self.null_value
            return

        try:
            timezone(value)
        except tzex.UnknownTimeZoneError:
            raise UnknownTimeZoneError(value)

        self.set_value(timezone=value)   

    def format(self):
        if self.timezone:
            return { 'timezone': self.timezone }
        return loads(self.null_value)


class WeekValue(ColumnValue):
    def __init__(self, **kwargs):
        super(WeekValue, self).__init__(**kwargs)

    @property
    def start_date(self):
        try:
            return loads(self.value)['week']['startDate']
        except KeyError:
            return None

    @start_date.setter
    def start_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise DateFormatError(value)

        self.set_value(startDate=value)

    @property
    def end_date(self):
        try:
            return loads(self.value)['week']['endDate']
        except KeyError:
            return None

    @end_date.setter
    def end_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise DateFormatError(value)

        self.set_value(endDate=value)

    def format(self):
        if self.start_date and self.end_date:
            return { 'week': { 'startDate': self.start_date, 'endDate': self.end_date }}
        return loads(self.null_value)

    def set_value(self, *argv, **kwargs):
        value_obj = loads(self.value)
        for key, value in kwargs.items():
            if self.value is self.null_value:
                value_obj['week'] = {}
            value_obj['week'][key] = value
        self.value = dumps(value_obj)


class ReadonlyValue(ColumnValue):
    def __init__(self, **kwargs):
        super(ReadonlyValue, self).__init__(**kwargs)

    def format(self):
        raise ColumnValueIsReadOnly(self.id, self.title)
            

def create_column_value(column_type: enums.ColumnType, **kwargs):
    return getattr(
        import_module(__name__), 
        config.COLUMN_TYPE_VALUE_MAPPINGS.get(column_type, 'ReadonlyValue'))(**kwargs)


class ColumnValueSettingsError(Exception):
    def __init__(self, column_type: str):
        self.message = 'Settings attribute is missing from input {} column data.'.format(column_type)


class DateFormatError(Exception):
    def __init__(self, value):
        self.message = 'Unable to parse date value "{}".'.format(value)


class TimeFormatError(Exception):
    def __init__(self, value):
        self.message = 'Unable to parse time value "{}".'.format(value)


class DropdownLabelError(Exception):
    def __init__(self, message):
        self.message = message


class NumberValueError(Exception):
    def __init__(self):
        self.message = 'Set value must be a valid integer or float.'


class UnknownTimeZoneError(Exception):
    def __init__(self, timezone):
        self.message = 'Unable to set unknown timezone value "{}".'.format(timezone)


class UnknownCountryCodeError(Exception):
    def __init__(self, country_code):
        self.message = 'Unable to set unrecognized country code value "{}".'.format(country_code)


class UnknownCountryNameError(Exception):
    def __init__(self, country_name):
        self.message = 'Unable to set unrecognized country name value "{}".'.format(country_name)


class ColumnValueIsReadOnly(Exception):
    def __init__(self, id: str, title: str):
        self.message = "Cannot format read-only column value '{}' ('{}') for updating.".format(title, id)