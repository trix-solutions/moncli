from json import dumps, loads
from importlib import import_module

from pycountry import countries
from pytz import timezone, exceptions as tzex
from schematics.models import Model
from schematics.types import StringType, IntType

from .. import config, enums, entities as e


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
        value_obj = loads(self.value)
        if len(argv) > 0:
            self.value = dumps(argv[0])
        elif len(kwargs) > 0:
            for key, value in kwargs.items():
                value_obj[key] = value
            self.value = dumps(value_obj)
        else:
            self.value = self.null_value


class CountryValue(ColumnValue):
    def __init__(self, **kwargs):
        super(CountryValue, self).__init__(**kwargs)

    @property
    def country_code(self):
        if self.value:
            return loads(self.value)['countryCode']
        return self.value

    @country_code.setter
    def country_code(self, code):
        country = countries.get(alpha_2=code)
        if not country:
            raise UnknownCountryCodeError(code)
        self.set_value(countryCode=country.alpha_2, countryName=country.name)

    @property
    def country_name(self):
        if self.value:
            return loads(self.value)['countryName']
        self.value

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
        return self.null_value


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
            return None

    @email_text.setter
    def email_text(self, value):
        self.set_value(text=value)
    
    def format(self):
        if self.email:  
            return { 'email': self.email, 'text': self.text }
        return {}


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
            return None

    @url_text.setter
    def url_text(self, value):
        return self.set_value(text=value)

    def format(self):
        if self.url:
            return { 'url': self.url, 'text': self.text }
        return self.null_value


class LongTextValue(ColumnValue):
    def __init__(self, **kwargs):
        super(LongTextValue, self).__init__(**kwargs)

    @property
    def long_text(self):
        if self.value:
            return loads(self.value)['text']
        return self.value
    
    @long_text.setter
    def long_text(self, value):
        if value:
            self.text = value
            current_value = loads(self.value)
            current_value['text'] = value
            self.value = dumps(current_value)
        else:
            self.text = ''
            self.value = None

    def format(self):
        if self.long_text:
            return {'text': self.long_text}
        return {}


class NumberValue(ColumnValue):
    def __init__(self, **kwargs):
        super(NumberValue, self).__init__(**kwargs)

    @property
    def number(self):
        if not self.value:
            return self.value
        value = loads(self.value)
        if self.__isint(value):
            return int(value)
        if self.__isfloat(value):
            return float(value)

    @number.setter
    def number(self, value):
        if not self.__isint(value) and not self.__isfloat(value):
            raise NumberValueError()
        self.text = str(value)
        self.value = dumps(self.text)

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
        if type(person_or_team) is type(e.User):
            kind = enums.PeopleKind.person
        elif type(person_or_team) is type(e.Team):
            kind = enums.PeopleKind.team
        persons_and_teams = self.persons_and_teams
        persons_and_teams.append({'id': person_or_team.id, 'kind': kind.name})
        value = loads(self.value)
        value['personsAndTeams'] = persons_and_teams
        self.value = dumps(value)

    def remove_people(self, id: int):
        persons_and_teams = []
        for entity in self.persons_and_teams:
            if entity.id != id:
                persons_and_teams.append(entity)
        value = loads(self.value)
        value['personsAndTeams'] = persons_and_teams
        self.value = dumps(value)


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
        return self.null_value


class StatusValue(ColumnValue):
    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('status')

        super(StatusValue, self).__init__(**kwargs)

    @property
    def index(self):
        return loads(self.value)['index']

    @index.setter
    def index(self, index: int):
        value = loads(self.value)
        value['index'] = index
        value['label'] = self.__settings.labels[str(index)]
        self.value = dumps(value)

    @property
    def label(self):
        try:
            return loads(self.value)['label']
        except KeyError:
            return loads(self.additional_info)['label']

    @label.setter
    def label(self, label: str):    
        value = loads(self.value)
        value['index'] = self.__settings.get_index(label)
        value['label'] = label
        self.value = dumps(value)


class TeamValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TeamValue, self).__init__(**kwargs)

    @property 
    def team_id(self):
        if self.value:
            return loads(self.value)['team_id']
        return self.value

    @team_id.setter
    def team_id(self, value):
        if not value:
            self.value = value
        else:
            self.value = dumps({'team_id': value})

    def format(self):
        if self.team_id is not None:
            return { 'team_id': self.team_id }
        return {}


class TextValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TextValue, self).__init__(**kwargs)

    @property
    def text_value(self):
        if self.value:
            return loads(self.value)
        return self.value

    @text_value.setter
    def text_value(self, value: str):
        if value:
            self.text = value
            self.value = dumps(value)
        else:
            self.text = ''
            self.value = None


class TimezoneValue(ColumnValue):
    def __init__(self, **kwargs):
        super(TimezoneValue, self).__init__(**kwargs)

    @property
    def timezone(self):
        if self.value:
            return loads(self.value)['timezone']
        return self.value

    @timezone.setter
    def timezone(self, tz):
        try:
            timezone(tz)
        except tzex.UnknownTimeZoneError:
            raise UnknownTimeZoneError(tz)

        if self.value:
            value = loads(self.value)
            value['timezone'] = tz
        else:
            value = {'timezone': tz}
        self.value = dumps(value)

    def format(self):
        if self.timezone is not None:
            return { 'timezone': self.timezone }
        return {}


def create_column_value(column_type: enums.ColumnType, **kwargs):
    return getattr(
        import_module(__name__), 
        config.COLUMN_TYPE_VALUE_MAPPINGS[column_type])(**kwargs)


class ColumnValueSettingsError(Exception):
    def __init__(self, column_type: str):
        self.message = 'Settings attribute is missing from input {} column data.'.format(column_type)


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