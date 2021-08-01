import json

from schematics.types import BaseType

class MondayType(BaseType):

    def __init__(self, column_value_type: type, id: str = None, title: str = None, *args, **kwargs):
        self.original_value = None
        
        metadata = {
            'module' : column_value_type.__module__,
            'name' : column_value_type.__name__
        }
        
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


class MondayTypeError(Exception):
    def __init__(self, message: str, error_code: str):
        self.error_code = error_code
        super(MondayTypeError, self).__init__(message)