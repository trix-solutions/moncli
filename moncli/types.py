import pytz, json, re
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime, timedelta, timezone
from pycountry import countries

from schematics.exceptions import ConversionError, ValidationError
from schematics.types import BaseType
from enum import EnumMeta,Enum

from . import entities as en
from .config import *
from .entities.column_value import Country



class MondayType(BaseType):

    native_type = None
    null_value = None
    allow_casts = ()
    native_default = None
    is_readonly = False

    def __init__(self, id: str = None, title: str = None, *args, **kwargs):
        self.original_value = None
        metadata = {}

        if not id and not title:
            raise TypeError('"id" or "title" parameter is required.')
        if id:
            metadata['id'] = id
        if title:
            metadata['title'] = title

        # Handle defaults
        default = kwargs.pop('default', None)
        if not default:
            default = self.native_default
        super(MondayType, self).__init__(*args, default=default, metadata=metadata, **kwargs)

    @property
    def changed_at(self):
        value = self.metadata.get('changed_at', None)
        if not value:
            return None
        changed_at = datetime.strptime(value, ZULU_FORMAT)
        utc = pytz.timezone('UTC')
        changed_at = utc.localize(changed_at, is_dst=False)
        return changed_at.astimezone(datetime.now().astimezone().tzinfo)

    def to_native(self, value, context=None):
        if not value:
            return self.native_default

        if not isinstance(value, en.cv.ColumnValue):
            if self.is_readonly:
                return value
            if isinstance(value, self.native_type):
                return self._process(value)
            if self.allow_casts and isinstance(value, self.allow_casts):
                return self._cast(value)
            raise ConversionError("Couldn't interpret '{}' as type {}.".format(str(value), self.native_type.__name__))

        self.metadata['id'] = value.id
        self.metadata['title'] = value.title
        settings = json.loads(value.settings_str) if value.settings_str else {}
        for k, v in settings.items():
            self.metadata[k] = v
        self._process_column_value(value)
        self.original_value = value.value
        return self.original_value

    def to_primitive(self, value, context=None):
        if self.null_value == None:
            return None
        if not value:
            return self.null_value
        # Assume that conversions are necessary before exporting
        value = self.to_native(value)
        return self._export(value)

    def _process(self, value):
        return value

    def _cast(self, value):
        return self.native_type(value)

    def _process_column_value(self, value: en.cv.ColumnValue):
        pass

    def _export(self, value):
        return value


class CheckboxType(MondayType):
    native_type = bool
    native_default = False
    allow_casts = (int, str)
    null_value = {}

    def _export(self, value):
        if value == True:
            return {'checked': 'true'}

class CountryType(MondayType):

    native_type = Country
    allow_casts = (dict,)
    null_value = {}

    def _cast(self, value):
        try:
            return Country(name = value['country'], code = value['code'])
        except KeyError:
            raise ConversionError('Unable to convert value "{}" to Country.'.format(value))
        
    def _export(self, value):
        if value.name and value.code:
            return {'countryName': value.name, 'countryCode': value.code}
        return self.null_value
    
    def validate_country(self, value): 
        country = countries.get(name=value.name)
        if not country:
            raise ValidationError('Value "{}" is not a valid country.'.format(value.name))
        code = countries.get(alpha_2=value.code)
        if not code:
            raise ValidationError('Value "{}" is not a valid alpha 2 country code.'.format(value.code))

    
class DateType(MondayType):

    native_type = datetime
    allow_casts = (str, int)
    null_value = {}
    has_time = False

    def __init__(self, id: str = None, title: str = None, has_time: bool = False, *args, **kwargs):
        self.id = id
        self.title = title
        self.has_time = has_time
        super().__init__(self.id, self.title, *args, **kwargs)

    def _cast(self, value):
        if isinstance(value, int):
            try:
                return datetime.fromtimestamp(value)
            except ValueError:
                raise ConversionError('Invalid UNIX timestamp "{}".'.format(value))
        if isinstance(value, str):
            try:
                date = datetime.strptime(value.split(' ', 1)[0], DATE_FORMAT)
            except ValueError:
                raise ConversionError('Cannot convert value "{}" into Date.'.format(value))
            if self.has_time == True:
                try:
                    time = datetime.strptime(value.split(' ', 1)[1], TIME_FORMAT)
                    date = date + timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
                    return date
                except ValueError:
                    raise ConversionError('Cannot convert value "{}" into Time.'.format(value))
            return date

    def _export(self, value):
        if self.has_time == True:
            value = value.astimezone(timezone.utc)
            date = value.date().strftime(DATE_FORMAT)
            time = value.time().strftime(TIME_FORMAT)
            return {'date': date, 'time': time}
        return {'date': value.date().strftime(DATE_FORMAT), 'time': None}


class DependencyType(MondayType):

    native_type = list
    native_default = []
    null_value = {}

    def _process(self, value):
        value_list = []
        for data in value:
            try:
                value_list.append(int(data))
            except ValueError:
                raise ConversionError('Invalid item ID: "{}".'.format(data))
        return value_list
    
    def _export(self, value):
        return { 'item_ids': [data for data in value]}


class EmailType(MondayType):
    native_type = en.cv.Email
    null_value = {}
    allow_casts = (dict, )

    def _cast(self, value):
        try:
            return en.cv.Email(value['email'],value.get('text', value['email']))
        except KeyError:
            raise ConversionError('Cannot convert value "{}" to Email.'.format(value))

    def _export(self, value):
        return {'email': value.email, 'text': value.text}

    def validate_email(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if value.email and not re.fullmatch(regex, value.email):
            raise ValidationError('Value "{}" is not a valid email address.'.format(value))


class HourType(MondayType):
    native_type = en.cv.Hour
    null_value = {}
    allow_casts = (dict, )

    def _cast(self, value):
        try:
            return en.cv.Hour(value['hour'],value.get('minute', 0))
        except KeyError:
            raise ConversionError('Cannot convert value "{}" into Hour.'.format(value))
    def _export(self, value):
        return {'hour': value.hour, 'minute': value.minute}

    def validate_hour(self,value):
        if (value.hour > 23) or (value.hour < 0):
            raise ValidationError('Hour values must be between 0-23, not "{}".'.format(value.hour))
        if (value.minute > 59) or (value.minute < 0):
            raise ValidationError('Minute values must be between 0-59, not "{}".'.format(value.minute))


class LinkType(MondayType):
    
    native_type = en.cv.Link
    null_value = {}
    allow_casts = (dict,)

    def _cast(self, value):
        try:
            return en.cv.Link(value['url'],value['text'])
        except KeyError:
            raise ConversionError('Cannot convert value "{}" to Link.'.format(value))
    
    def _export(self, value):
        if value.url != None:
            return {'url': value.url, 'text': value.text}
        return self.null_value

    def validate_link(self,value):
        str_value = value.url
        if not (str_value.startswith('https://') or str_value.startswith('http://')):
            raise ValidationError('Value "{}" is not a valid URL link.'.format(value))
        return str_value



class LongTextType(MondayType):
    native_type = str
    allow_casts = (int, float)
    null_value = {}

    def _export(self, value):
        return {'text': value}


class NumberType(MondayType):
    native_type = (int, float)
    allow_casts = (str, )
    null_value = ""
    
    def _cast(self, value):
        try:
            number_value = int(value) if int(value) else float(value)
            return number_value
        except TypeError:
            raise ConversionError('Couldn\'t interpret str {} as int or float.'.format(value))
    
    def _export(self, value):
        return str(value)


class RatingType(MondayType):
    native_type = int
    allow_casts = (str,)
    null_value = {}

    def _cast(self, value):
        try:
            return int(value)
        except ValueError:
            raise ConversionError('Value "{}" is not a valid rating.'.format(value))
    
    def _export(self, value):
        return { 'rating': value}


class StatusType(MondayType):
    native_type = str
    allow_casts = (int,)
    null_value = {}

    def __init__(self, id: str = None, title: str = None, as_enum: type = None ,  *args, **kwargs):
        if as_enum:
            if not isinstance(as_enum, EnumMeta):
                raise TypeError('Invalid type "{}" for status Enum.'.format(as_enum.__name__))
            self.choices = list(as_enum)
            for value in self.choices:
                if not isinstance(value.value, str):
                    raise TypeError('Invalid value "{}" for status Enum "{}".'.format(value.value, value.__class__.__name__))
            self.native_type =  as_enum
            self.allow_casts = (str,)
            
        super().__init__(id=id, title=title, *args, **kwargs)
    
    def _process(self, value):
        labels = self.metadata['labels']
        if self.native_type != str:
            return value
        try:
            int(value)
            try:
                return labels[value]
            except KeyError:
                raise ConversionError('Cannot find status label with index "{}".'.format(value))
        except ValueError:
            if value in labels.values():
                return value
            raise ConversionError('Cannot find status label "{}".'.format(value))
                
    def _cast(self, value):
        labels = self.metadata['labels']
        label = str(value)
        if self.native_type == str and isinstance(value,int):
            try:    
                return labels[label]
            except KeyError:
                raise ConversionError('Cannot find status label with index "{}".'.format(value))
            
        if isinstance(self.native_type, EnumMeta) and isinstance(value,str):
            try:
                return self.native_type(label)
            except ValueError:
                    raise ConversionError('Cannot find status label with index "{}".'.format(value))
    
    def _process_column_value(self, column_value: en.cv.ColumnValue):
        if self.native_type == str:
            self.choices = [value for value in self.metadata['labels'].values()]
                      
    def _export(self, value):
            labels = self.metadata['labels']
            if self.native_type == str:
                label = value
            elif isinstance(self.native_type, EnumMeta):
                label = value.value
            for index, value in labels.items():
                if value == label:
                    return {'index': int(index)}


class SubItemType(MondayType):

    native_type = list
    native_default = []
    null_value = {}
    is_readonly = True
 

class TextType(MondayType):
    native_type = str
    allow_casts = (int, float)
    null_value = ""


class TagsType(MondayType):
    native_type = list
    native_default = []
    null_value = {}

    def _process(self, value):
        for tag in value:
            try:
                return_value = [int(tag) for tag in value]
            except ValueError:
                raise ConversionError('Invalid Tag ID "{}".'.format(tag))
        return return_value
    
    def _export(self, value):
        return {'tag_ids': value}


class TimeZoneType(MondayType):
    native_type = str
    null_value = {}

    def _export(self, value):
        return {'timezone': value}

    def validate_timezone(self, value):
        try:
            pytz.timezone(value)
        except (UnknownTimeZoneError):
            raise ValidationError('Unknown time zone "{}".'.format(value))


class WeekType(MondayType):
    
    native_type = en.cv.Week
    null_value = {}
    allow_casts = (dict,)

    def _cast(self, value):
        try:
            return en.cv.Week(value['start'],value['end'])
        except KeyError:
            raise ConversionError('Cannot convert value "{}" to Week.'.format(value))
    
    def _export(self, value):
        if not (value.start and value.end) :
            return self.null_value
        start =  value.start.strftime(DATE_FORMAT) 
        end  = value.end.strftime(DATE_FORMAT)
        return  {'week': {'startDate': start, 'endDate': end}}

