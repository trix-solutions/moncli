import pytz, json
from datetime import datetime

from schematics.exceptions import ConversionError
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
            return value

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

class TextType(MondayType):
    native_type = str
    allow_casts = (int, float)
    null_value = ""