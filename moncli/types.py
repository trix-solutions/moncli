import pytz, json,re
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime, timedelta, timezone

from schematics.exceptions import ConversionError, ValidationError
from schematics.types import BaseType
from enum import Enum,EnumMeta

from . import entities as en
from .config import *


class MondayType(BaseType):

    native_type = None
    null_value = None
    allow_casts = ()
    native_default = None

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

    def _set_metadata(self, value: en.cv.ColumnValue):
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
    allow_casts = (int, str)
    null_value = {}

    def __init__(self, id: str = None, title: str = None,data_mapping:dict =None ,  *args, **kwargs):
        if data_mapping:
            values= [value for value in data_mapping.values()]        
            self.native_type = values[0].__class__
            self.choices = values
        self._data_mapping =  data_mapping 
        super().__init__(id=id, title=title, *args, **kwargs)
    
    def _process(self, value):
        labels = self.metadata['labels']
        label = str(value)
        if self.native_type != str:
            return value
        try:
            value = int(value)
            try:
                return labels[label]
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
            if not (label in labels.keys()):
                raise ConversionError('Cannot find status label with index "{}".'.format(value))
            return labels[label]
            
        if isinstance(self.native_type,EnumMeta) and isinstance(value,str):
            try:
                value = int(value)
                if not (label in labels.keys()):
                    raise ConversionError('Cannot find status label with index "{}".'.format(value))
                return labels[label]
            except ValueError:
                if not (label in labels.values()):
                    raise ConversionError('Cannot find status label with index "{}".'.format(value))
                return self._data_mapping[label]
        if isinstance(self.native_type,EnumMeta) and isinstance(value,int):
            if not (label in labels.keys()):
                    raise ConversionError('Cannot find status label with index "{}".'.format(value))
            return self._data_mapping[labels[label]]

    def _export(self, value):
        labels = self.metadata['labels']
        label = str(value)
        index  = None
        if isinstance(value,str):
            index = self._data_mapping[value].value
        elif isinstance(value,Enum):
            key = None
            for k,v in self._data_mapping.items():
                if v == value:
                    key = k
                    break
            for k,v in labels.items():
                if v==key:
                    index = k
                    break
        return {'index': int(index)} 

 
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









