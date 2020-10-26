from datetime import datetime
from importlib import import_module
from json import dumps, loads

from pycountry import countries
from pytz import timezone, exceptions as tzex
from schematics.models import Model
from schematics.types import StringType, IntType

from .. import config, enums, entities as en


SIMPLE_NULL_VALUE = ''
COMPLEX_NULL_VALUE = {}

class _ColumnValue(Model):
    """Base column value model"""

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
    """The value of an items column.

    __________
    Properties
 
        additional_info : `json`
            The column value's additional information.
        id : `str`
            The column's unique identifier.
        text : `str`
            The column's textual value in string form.
        title : `str`
            The columns title.
        type : `str`
            The column's type.
        value : `json`
            The column's value in json format.

    
    _______
    Methods

        format : `dict`
            Format for column value update.
        set_value : `void`
            Sets the value of the column.
    """

    null_value = COMPLEX_NULL_VALUE

    def __init__(self, **kwargs):
        super(ColumnValue, self).__init__(kwargs)
        # Set seriaized configured null value if no value.
        if not self.value:
            self.value = dumps(self.null_value)

    def set_value(self, *args, **kwargs): 
        """Sets the value of the column.

        __________
        Parameters

            args : `tuple`
                The column value for a string/int/boolean column value.
            kwargs : `dict`
                The column value for a complex dictionary object.    
        """

        if len(args) > 0:
            self.value = dumps(args[0])
        elif len(kwargs) > 0:
            value_obj = loads(self.value)
            for key, value in kwargs.items():
                value_obj[key] = value
            self.value = dumps(value_obj)
        else:
            self.value = dumps(self.null_value)


class CheckboxValue(ColumnValue):
    """A checkbox column value.
    
    __________
    Properties

        checked : `bool`
            Is the column checked.
    """

    def __init__(self, **kwargs):
        super(CheckboxValue, self).__init__(**kwargs)
        
    @property
    def checked(self):
        """Is the column checked"""
        try:
            return loads(self.value)['checked']
        except KeyError:
            return False

    @checked.setter
    def checked(self, value: bool):
        if value:
            self.set_value(checked=value)
            return
        self.set_value()

    
    def format(self):
        """Format for columjn value update."""
        if self.checked:
            return { 'checked': 'true' }
        return self.null_value


class CountryValue(ColumnValue):
    """A checkbox column value.
    
    __________
    Properties

        country_code : `str`
            The country code.
        country_name : `str`
            The country name.
    """

    def __init__(self, **kwargs):
        super(CountryValue, self).__init__(**kwargs)

    @property
    def country_code(self):
        """The country code."""
        try:
            return loads(self.value)['countryCode']
        except KeyError:
            return None

    @country_code.setter
    def country_code(self, code):
        if not code:
            self.set_value()
            return
        country = countries.get(alpha_2=code)
        if not country:
            raise UnknownCountryCodeError(code)
        self.set_value(countryCode=country.alpha_2, countryName=country.name)

    @property
    def country_name(self):
        """The country name."""
        try:
            return loads(self.value)['countryName']
        except KeyError:
            return None

    @country_name.setter
    def country_name(self, name):
        if not name:
            self.set_value()
            return
        country = countries.get(name=name)
        if not country:
            raise UnknownCountryNameError(name)
        self.set_value(countryCode=country.alpha_2, countryName=country.name)
 
    def format(self):
        """Format for column value update."""
        if self.country_code and self.country_name:
            return {
                'countryCode': self.country_code,
                'countryName': self.country_name
            }
        return self.null_value


class DateValue(ColumnValue):
    """A date column value.

    __________
    Properties

        date : `str`
            The date value.
        time : `str`
            The time value.
    """

    def __init__(self, **kwargs):
        super(DateValue, self).__init__(**kwargs)

    @property
    def date(self):
        """The date value."""
        try:
            return loads(self.value)['date']
        except KeyError:
            return None

    @date.setter
    def date(self, value):
        if value:
            validate_date(value)
        self.set_value(date=value)

    @property
    def time(self):
        """The time value."""
        try:
            return loads(self.value)['time']
        except KeyError:
            return None

    @time.setter
    def time(self, value):
        if value:
            validate_time(value)
        self.set_value(time=value)

    def format(self):
        """Format for column value update."""
        if self.date:
            result = {'date': self.date}
            if self.time:
                result['time'] = self.time
            return result
        return self.null_value
        

class DropdownValue(ColumnValue):
    """A dropdown column value.
    
    __________
    Properties

        labels : `list[moncli.entities.DropdownLabel]`
            Labels currently assigned to the column value.

    _______
    Methods

        add_label : `void`
            Add a label to the column value by id.
        remove_label : `void`
            Remove a label from the column value by id.
    """

    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('dropdown')
        super(DropdownValue, self).__init__(**kwargs)

    @property
    def labels(self):
        """Labels currently assigned to column value."""

        try:
            ids = loads(self.value)['ids']
            return [label for label in self.__settings.labels if label.id in ids]
        except KeyError:
            return []


    def format(self):
        """Format for column value update."""

        if len(self.labels) == 0:
            return {}
        return { 'ids': [label.id for label in self.labels] }


    def add_label(self, id: int):
        """Add a label to the column value by id.

        __________
        Parameters

            id : `int`
                The label ID of the label to add as defined in the column settings.
        """

        try:
            label = self.__settings[id]
        except KeyError:
            raise DropdownLabelError(id)

        value = loads(self.value)
        if value == self.null_value:
            value['ids'] = []
        if label.id in value['ids']:
            raise DropdownLabelSetError(id)
        value['ids'].append(label.id)
        self.set_value(ids=value['ids'])


    def remove_label(self, id: int):
        """Remove a label from the column value by id.

        __________
        Parameters

            id : `int`
                The label ID of the label to remove as defined in the column settings.
        """

        try:
            label = self.__settings[id]
        except KeyError:
            raise DropdownLabelError(id)

        value = loads(self.value)
        if value == self.null_value or label.id not in value['ids']:
            raise DropdownLabelNotSetError(id)
        value['ids'].remove(label.id)
        self.set_value(ids=value['ids'])


class EmailValue(ColumnValue):
    """An email column value.
    
    __________
    Properties

        email : `str`
            The email address.
        email_text : `str`
            The display text.
    """

    def __init__(self, **kwargs):
        super(EmailValue, self).__init__(**kwargs)

    @property
    def email(self):
        """The email address."""
        try:
            return loads(self.value)['email']
        except KeyError:
            return None

    @email.setter
    def email(self, value):
        self.set_value(email=value)

    @property
    def email_text(self):
        """The display text."""
        try:
            return loads(self.value)['text']
        except KeyError:
            return self.email

    @email_text.setter
    def email_text(self, value):
        self.set_value(text=value)
    
    def format(self):
        """Format for column value update."""
        if self.email:  
            return { 'email': self.email, 'text': self.email_text }
        return self.null_value


class FileValue(ColumnValue):
    """A file column value.
    
    __________
    Properties

        files : `list[dict]`
            List of files attached to file column.
    """

    def __init__(self, **kwargs):
        super(FileValue, self).__init__(**kwargs)

    @property
    def files(self):
        """List of files attached to file column."""
        try:
            return loads(self.value)['files']
        except KeyError:
            return None

    def format(self):
        """Format for column value update."""
        return { 'clear_all': True }


class HourValue(ColumnValue):
    """An hour column value.
    
    __________
    Properties

        hour : `int`
            The hour (2-digit).
        minute : `int`
            The minute (2-digit).
    """

    def __init__(self, **kwargs):
        super(HourValue, self).__init__(**kwargs)

    @property
    def hour(self):
        """The hour (2-digit)."""
        try:
            return loads(self.value)['hour']
        except KeyError:
            return None

    @hour.setter
    def hour(self, value: int):
        self.set_value(hour=value)
    
    @property
    def minute(self):
        """The minute (2-digit)."""
        try:
            return loads(self.value)['minute']
        except KeyError:
            return 0

    @minute.setter
    def minute(self, value: int):
        if value:
            self.set_value(minute=value)
            return
        self.set_value(minute=0)

    def format(self):
        """Format for column value update."""
        if self.hour:
            return { 'hour': self.hour, 'minute': self.minute }
        return self.null_value


class LinkValue(ColumnValue):
    """A link column value.
    
    __________
    Properties

        url : `str`
            The url address.
        url_text : `str`
            The display text.
    """

    def __init__(self, **kwargs):
        super(LinkValue, self).__init__(**kwargs)

    @property
    def url(self):
        """The url address."""
        try:
            return loads(self.value)['url']
        except KeyError:
            return None

    @url.setter
    def url(self, value):
        self.set_value(url=value)

    @property
    def url_text(self):
        """The display text."""
        try:
            return loads(self.value)['text']
        except KeyError:
            return self.url

    @url_text.setter
    def url_text(self, value):
        return self.set_value(text=value)

    def format(self):
        """Format for column value update."""
        if self.url:
            return { 'url': self.url, 'text': self.url_text }
        return self.null_value


class LongTextValue(ColumnValue):
    """A long text column value.
    
    __________
    Properties

        long_text : `str`
            The long text value.
    """
    def __init__(self, **kwargs):
        super(LongTextValue, self).__init__(**kwargs)

    @property
    def long_text(self):
        """The longtext value."""
        try:
            return loads(self.value)['text']
        except KeyError:
            return None
    
    @long_text.setter
    def long_text(self, value):
        if value:
            self.set_value(text=value)
            return
        self.set_value()

    def format(self):
        """Format for column value update."""
        if self.long_text:
            return {'text': self.long_text}
        return self.null_value


class NameValue(ColumnValue):
    """A name column value.
    
    __________
    Properties

        name : `str`
            The name value.
    """

    null_value = SIMPLE_NULL_VALUE

    def __init__(self, **kwargs):
        super(NameValue, self).__init__(**kwargs)

    @property
    def name(self):
        """The name value."""
        try:
            return loads(self.value)
        except Exception:
            return self.null_value

    @name.setter
    def name(self, value):
        if value:
            self.set_value(value)
        else:
            self.set_value()
    
    def format(self):
        """Format for column value update."""
        return self.name


class NumberValue(ColumnValue):
    """A number column value.
    
    __________
    Properties

        number : `int/float`
            The integer or float number value.
    """

    null_value = SIMPLE_NULL_VALUE

    def __init__(self, **kwargs):
        super(NumberValue, self).__init__(**kwargs)

    @property
    def number(self):
        """The integer or float number value."""
        value = loads(self.value)
        if value == self.null_value:
            return None
        if self.__isint(value):
            return int(value)
        if self.__isfloat(value):
            return float(value)

    @number.setter
    def number(self, value):
        if value:
            if not self.__isint(value) and not self.__isfloat(value):
                raise NumberValueError()
            self.set_value(value)
        else:
            self.set_value()

    def format(self):
        """Format for column value update."""
        if self.number:
            return str(self.number)
        return SIMPLE_NULL_VALUE

    def __isfloat(self, value):
        """Is the value a float."""
        try:
            float(value)
        except ValueError:
            return False
        return True
  
    def __isint(self, value):
        """Is the value an int."""
        try:
            a = float(value)
            b = int(a)
        except ValueError:
            return False
        return a == b


class PeopleValue(ColumnValue):
    """A people column value.
    
    __________
    Properties

        persons_and_teams : `list[dict]`
            The persons and teams assigned to the column value.

    _______
    Methods

        add_people : `void`
            Add user or team to column value.
        remove_people : `void`
            Remove user or team from column value.
    """
    
    def __init__(self, **kwargs):
        super(PeopleValue, self).__init__(**kwargs)
    
    @property
    def persons_and_teams(self):
        """The persons and teams assigned to the column value."""
        try:
            return loads(self.value)['personsAndTeams']
        except KeyError:
            return [] 

    def format(self):
        """Format for column value update."""
        if self.persons_and_teams:
            return { 'personsAndTeams': self.persons_and_teams }
        return self.null_value


    def add_people(self, person_or_team):
        """Add user or team to column value.
    
        __________
        Parameters

            person_or_team : `moncli.entities.User/moncli.entities.Team`
                The person/team added to the column value.
        """

        kind = enums.PeopleKind.person
        if type(person_or_team) == en.Team:
            kind = enums.PeopleKind.team
        value = {'id': int(person_or_team.id), 'kind': kind.name}
        if value not in self.persons_and_teams:
            persons_and_teams = self.persons_and_teams
            persons_and_teams.append(value)
            self.set_value(personsAndTeams=persons_and_teams)


    def remove_people(self, id: int):
        """Remove user or team from column value.
    
        __________
        Parameters

            id : `int`
                The id of the person/team to be removed.
        """

        persons_and_teams = []
        for entity in self.persons_and_teams:
            if int(entity['id']) != id:
                persons_and_teams.append(entity)
        self.set_value(personsAndTeams=persons_and_teams)


class PhoneValue(ColumnValue):
    """A phone column value.
    
    __________
    Properties

        phone : `str`
            The phone number value.
        country_short_name : `str`
            The iso-2 country code.
    """

    def __init__(self, **kwargs):
        super(PhoneValue, self).__init__(**kwargs)

    @property
    def phone(self):
        """The phone number value."""
        try:
            return loads(self.value)['phone']
        except KeyError:
            return None

    @phone.setter
    def phone(self, value):
        self.set_value(phone=value)

    @property
    def country_short_name(self):
        """The iso-2 country code."""
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
        """Format for column value update."""
        if self.phone and self.country_short_name:
            return { 'phone': self.phone, 'countryShortName': self.country_short_name }
        return { 'phone': '', 'countryShortName': '' }


class RatingValue(ColumnValue):
    """A rating column value.
    
    __________
    Properties

        rating : `int`
            The rating value.
    """

    def __init__(self, **kwargs):
        super(RatingValue, self).__init__(**kwargs)

    @property
    def rating(self):
        """The rating value."""
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
        """Format for column value update."""
        if self.rating:
            return { 'rating': self.rating }
        return self.null_value


class StatusValue(ColumnValue):
    """A status column value.
    
    __________
    Properties

        index : `int`
            The id of the status label.
        label : `str`
            Display text of the status label.
    """

    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('status')
        super(StatusValue, self).__init__(**kwargs)

    @property
    def index(self):
        """The id of the status label."""
        try:
            return loads(self.value)['index']
        except KeyError: 
            return None

    @index.setter
    def index(self, index: int):
        if index or index == 0:
            try:
                label = self.__settings[index]
                self.set_value(index=index, label=label)
            except KeyError:
                raise StatusIndexError(index)
        else:
            self.set_value()

    @property
    def label(self):
        """Display text of the status label"""
        try:
            return loads(self.value)['label']
        except KeyError:
            try:
                return loads(self.additional_info)['label']
            except KeyError:
                return None

    @label.setter
    def label(self, label: str): 
        if label:
            index=self.__settings.get_index(label)
            if index or index == 0:
                self.set_value(index=index, label=label)
            else:
                raise StatusLabelError(label)
        else:
            self.set_value()

    def format(self):
        """Format for column value update."""
        if self.index or self.index == 0:
            return {'index': self.index}
        return self.null_value
        

class TagsValue(ColumnValue):
    """A tags column value.
    
    __________
    Properties

        tag_ids : `list[int]`
            The list of tag ids assigned to column value. 

    _______
    Methods

        add : `void`
            Add tag to column value.
        remove : `void`
            Remove tag from column value.
    """
    def __init__(self, **kwargs):
        super(TagsValue, self).__init__(**kwargs)

    @property
    def tag_ids(self):
        """The list of tag ids assigned to column value."""
        try:
            return loads(self.value)['tag_ids']
        except KeyError:
            return []

    def format(self):
        """Format for column value update."""
        return { 'tag_ids': self.tag_ids }


    def add(self, tag_id: int):
        """Add tag to column value.

        __________
        Parameters

            tag_id : `int`
                The id of the tag to add.
        """

        tag_ids = self.tag_ids
        if tag_id not in tag_ids:
            tag_ids.append(tag_id)
            self.set_value(tag_ids=tag_ids)


    def remove(self, tag_id: int):
        """Remove tag from column value.

        __________
        Parameters

            tag_id : `int`
                The id of the tag to remove.
        """
        
        tag_ids = self.tag_ids
        if tag_id in tag_ids:
            tag_ids.remove(tag_id)
            self.set_value(tag_ids=tag_ids)


class TeamValue(ColumnValue):
    """A team column value.
    
    __________
    Properties

        team_id : `int`
            The id of the assigned team.
    """
    
    def __init__(self, **kwargs):
        super(TeamValue, self).__init__(**kwargs)

    @property 
    def team_id(self):
        """The id of the assigned team."""
        try:
            return loads(self.value)['team_id']
        except KeyError:
            return None

    @team_id.setter
    def team_id(self, value):
        if value:
            self.set_value(team_id=value)
        else:
            self.set_value()

    def format(self):
        """Format for column value update."""
        if self.team_id is not None:
            return { 'team_id': self.team_id }
        return self.null_value


class TextValue(ColumnValue):
    """A text column value.
    
    __________
    Properties

        text_value : `str`
            The column text value.
    """

    null_value = ''
    def __init__(self, **kwargs):
        super(TextValue, self).__init__(**kwargs)

    @property
    def text_value(self):
        """The column text value."""
        value = loads(self.value)
        if value == self.null_value:
            return None
        return value

    @text_value.setter
    def text_value(self, value):
        if value:
            self.set_value(value)
        else:
            self.set_value()

    def format(self):
        """Format for column value update."""
        if self.text_value:
            return self.text_value
        return self.null_value


class TimelineValue(ColumnValue):
    """A timeline column value.
    
    __________
    Properties

        from_date : `str`
            The timeline start date.
        to_date : `str`
            The timeline end date.
    """

    def __init__(self, **kwargs):
        super(TimelineValue, self).__init__(**kwargs)

    @property
    def from_date(self):
        """The timeline start date."""
        try:
            return loads(self.value)['from']
        except KeyError:
            return None

    @from_date.setter
    def from_date(self, value):
        if value:
            validate_date(value)
            self.set_value(**{'from': value})
        else: 
            self.set_value()

    @property
    def to_date(self):
        """The timeline end date."""
        try:
            return loads(self.value)['to']
        except KeyError:
            return None

    @to_date.setter
    def to_date(self, value):
        if value:
            validate_date(value)
            self.set_value(to=value)
        else:
            self.set_value()

    def format(self):
        """Format for column value update."""
        if self.from_date and self.to_date:
            return { 'from': self.from_date, 'to': self.to_date }
        return self.null_value
        

class TimezoneValue(ColumnValue):
    """A timezone column value.
    
    __________
    Properties

        timezone : `str`
            The timezone standard value.
    """
    def __init__(self, **kwargs):
        super(TimezoneValue, self).__init__(**kwargs)

    @property
    def timezone(self):
        """The timezone standard value."""
        try:
            return loads(self.value)['timezone']
        except KeyError:
            return None

    @timezone.setter
    def timezone(self, value):
        if value:
            try:
                timezone(value)
            except tzex.UnknownTimeZoneError:
                raise UnknownTimeZoneError(value)
            self.set_value(timezone=value) 
        else:
            self.set_value()  

    def format(self):
        """Format for column value update."""
        if self.timezone:
            return { 'timezone': self.timezone }
        return self.null_value


class WeekValue(ColumnValue):
    """A week column value.
    
    __________
    Properties

        start_date : `str`
            The start date of the week.
        end_date : `str`
            The end date of the week.

    _______
    Methods

        set_value : `void`
            Set week column value.
    """

    null_value = {'week': ''}
    def __init__(self, **kwargs):
        super(WeekValue, self).__init__(**kwargs)

    @property
    def start_date(self):
        """The start date of the week."""
        try:
            return loads(self.value)['week']['startDate']
        except KeyError:
            return None
        except TypeError:
            return None

    @start_date.setter
    def start_date(self, value):
        if value:   
            validate_date(value)
            self.set_value(startDate=value)
        else:
            self.set_value()

    @property
    def end_date(self):
        """The end date of the week."""
        try:
            return loads(self.value)['week']['endDate']
        except KeyError:
            return None
        except TypeError:
            return None

    @end_date.setter
    def end_date(self, value):
        if value:  
            validate_date(value)
            self.set_value(endDate=value)
        else:
            self.set_value()

    def format(self):
        """Format for column value update."""
        if self.start_date and self.end_date:
            return { 'week': { 'startDate': self.start_date, 'endDate': self.end_date }}
        return self.null_value


    def set_value(self, *args, **kwargs):
        """Set week column value.
        
        __________
        Parameters

            args : `tuple`
                This is not used.
            kwargs : `dict`
                The column value properties to be added/updated.
        """

        value = loads(self.value)
        if len(kwargs) == 0:
            value = self.null_value
        for k, v in kwargs.items():
            if value == self.null_value:
                value['week'] = {}
            value['week'][k] = v
        self.value = dumps(value)


class ItemLinkValue(ColumnValue):
    """An item link column value.
    
    __________
    Properties

        item_ids : `list[str]`
            The list of linked items unique identifiers.

    _______
    Methods

        add_item : `void`
            Add item to link list.
        remove_item : `void`
            remove item from remove.
    """

    def __init__(self, **kwargs):
        super(ItemLinkValue, self).__init__(**kwargs)

    @property
    def item_ids(self):
        """List of linked items unique identifiers."""
        try:
            return [str(id) for id in loads(self.value)['item_ids']]
        except:
            return []

    def add_item(self, item_id: str):
        """Add item to link list.

        __________
        Parameters

            item_id : `str`
                Item unique identifier to add.
        """

        ids = self.item_ids
        ids.append(str(item_id))
        self.value = dumps({'item_ids': [int(id) for id in ids]})


    def remove_item(self, item_id: str):
        """Remove item from link list.

        __________
        Parameters

            item_id : `str`
                Item unique identifier to remove.
        """

        if item_id not in self.item_ids:
            raise ItemIdNotFound(item_id)

        ids = [id for id in self.item_ids if id != item_id]
        self.value = dumps({'item_ids': [int(id) for id in ids]})

    
    def format(self):
        """Format for column value update."""
        return {'item_ids': [int(id) for id in self.item_ids]}
        

class ReadonlyValue(ColumnValue):
    """A readonly column value."""
    def __init__(self, **kwargs):
        super(ReadonlyValue, self).__init__(**kwargs)

    def format(self):
        """Format for column value update."""
        raise ColumnValueIsReadOnly(self.id, self.title)
            

def create_column_value(column_type: enums.ColumnType, **kwargs):
    """Create column value instance

    __________
    Parameters

        column_type : `moncli.enums.ColumnType`
            The column type to create.
        kwargs : `dict`
            The raw column value data.
    """

    return getattr(
        import_module(__name__), 
        config.COLUMN_TYPE_VALUE_MAPPINGS.get(column_type, 'ReadonlyValue'))(**kwargs)


def validate_date(date_string: str):
    """Validate date string

    __________
    Parameters

        date_string : `str`
            The date string to be validated.
    """

    try:
        datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise DateFormatError(date_string)


def validate_time(time_string: str):
    """Validate time string

    __________
    Parameters

        time_string : `str`
            The time string to be validated.
    """

    try:
        datetime.strptime(time_string, '%H:%M:%S')
    except ValueError:
        raise TimeFormatError(time_string)


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
    def __init__(self, id: int):
        self.message = 'Unable to find dropdown label with ID {}.'.format(str(id))


class DropdownLabelSetError(Exception):
    def __init__(self, id: int):
        self.message = 'Label with ID {} has already been set.'.format(str(id))


class DropdownLabelNotSetError(Exception):
    def __init__(self, id: int):
        self.message = 'Cannot remove unset label with ID {}.'.format(str(id))


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


class StatusIndexError(Exception):
    def __init__(self, index: int):
        self.message = 'Unable to find status value with index {}.'.format(str(index))


class StatusLabelError(Exception):
    def __init__(self, label: str):
        self.message = 'Unable to find status value with label {}.'.format(label)

class ItemIdNotFound(Exception):
    def __init__(self, item_id: str):
        self.message = 'Unable to find item ID "{}".'.format(item_id)