import pytz, json
from datetime import datetime

from schematics.types import BaseType

from . import entities as en
from .config import *

class MondayType(BaseType):

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

        if not isinstance(value, en.ColumnValue):
            if self.allow_casts and isinstance(value, self.allow_casts):
                return self._cast(value)
            return value

        self.metadata['id'] = value.id
        self.metadata['title'] = value.title
        settings = json.loads(value.settings_str) if value.settings_str else {}
        for k, v in settings.items():
            self.metadata[k] = v

        try:
            additional_info = json.loads(value.additional_info)
        except:
            additional_info = value.additional_info
        self.original_value = self._convert((value.text, value.value, additional_info))
        return self.original_value

    def to_primitive(self, value, context=None):
        if self.null_value == None:
            return None
        if not value:
            return self.null_value
        return self._export(value)

    def _cast(self, value):
        return self.native_type(value)

    def _convert(self, value: tuple):
        _, data, _ = value
        return data

    def _export(self, value):
        return value