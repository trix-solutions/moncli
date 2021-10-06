import pytz, json
from datetime import datetime
from pytz.exceptions import UnknownTimeZoneError

from schematics.exceptions import ConversionError, ValidationError
from schematics.types import BaseType

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



        
class TextType(MondayType):
    native_type = str
    allow_casts = (int, float)
    null_value = ""


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
class StatusType(MondayType):
    def __init__(self, id: str = None, title: str = None,  *args, **kwargs):
        data_mapping = { v: int(k) for k,v in self.settings['labels'] }
        if data_mapping:
            values= [data_mapping]        
            self.to_native = values[0].__class__
            values = self.choices
        data_mapping =  self.field_data_mapping 
        super().__init__(id=id, title=title, *args, **kwargs)
    
    def _process(self, value):
        labels = self.metadata['labels']
        if isinstance(self.native_type,str):
            try:
                if isinstance(int(value),int):
                    if value in labels.values():
                        return value
            except ValueError:
                    raise ConversionError('Cannot find status label with index "{}".'.format(value))
            if isinstance(value,int):
                if value in labels.values():
                    return value
            return value

    def _cast(self, value):
        return super()._cast(value)





