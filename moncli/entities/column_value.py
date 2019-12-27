import json

from schematics.models import Model
from schematics.types import StringType

from ..enums import ColumnType

class ColumnValue(Model):

    id = StringType(required=True)
    title = StringType()
    text = StringType()
    value = StringType()
    additional_info = StringType()


    def __repr__(self):
        return str(self.to_primitive())


    def format(self):
        return self.to_primitive()


class TextValue(ColumnValue):

    def __init__(self, **kwargs):
        super(TextValue, self).__init__(kwargs)

    @property
    def text_value(self):
        if self.value:
            return json.loads(self.value)
        return self.value

    @text_value.setter
    def text_value(self, value):
        if value:
            self.text = value
            self.value = json.dumps(value)
        else:
            self.text = ''
            self.value = None


def create_column_value(column_type: ColumnType, **kwargs):

    if column_type is ColumnType.text:
        return TextValue(**kwargs)