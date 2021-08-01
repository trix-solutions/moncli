import json

from schematics.types import BaseType

from moncli.entities import column_value as cv

class MondayType(BaseType):

    def __init__(self, id: str = None, title: str = None, *args, **kwargs):
        self.original_value = None
        metadata = {}

        if not id and not title:
            raise MondayTypeError('"id" or "title" parameter is required.')
        if id:
            metadata['id'] = id
        if title:
            metadata['title'] = title

        super(MondayType, self).__init__(*args, metadata=metadata, **kwargs)

    def to_native(self, value, context=None):
        self.original_value = value.value
        self.metadata['id'] = value.id
        self.metadata['title'] = value.title
        return json.loads(value.value)


class CheckboxType(MondayType):

    def to_native(self, value, context = None):
        value = super().to_native(value, context=context)
        try:
            return bool(value['checked'])
        except:
            return False

    def to_primitive(self, value, context = None):
        return {'checked': value}


class TextType(MondayType):

    def to_primitive(self, value, context=None):
        if not value:
            return ''
        return value


class MondayTypeError(Exception):
    def __init__(self, message: str, error_code: str):
        self.error_code = error_code
        super(MondayTypeError, self).__init__(message)