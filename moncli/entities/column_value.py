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


class LongTextValue(ColumnValue):

    def __init__(self, **kwargs):
        super(LongTextValue, self).__init__(kwargs)

    @property
    def long_text(self):
        if self.value:
            return json.loads(self.value)
        return self.value
    
    @long_text.setter
    def long_text(self, value):
        if value:
            self.text = value
            self.value = json.dumps(value)
        else:
            self.text = ''
            self.value = None


class StatusValue(ColumnValue):

    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise StatusValueSettingsError

        super(StatusValue, self).__init__(kwargs)

    @property
    def index(self):
        return json.loads(self.value)['index']

    @index.setter
    def index(self, index: int):
        value = json.loads(self.value)
        value['index'] = index
        value['label'] = self.__settings.labels[str(index)]
        self.value = json.dumps(value)

    @property
    def label(self):
        try:
            return json.loads(self.value)['label']
        except KeyError:
            return json.loads(self.additional_info)['label']

    @label.setter
    def label(self, label: str):    
        value = json.loads(self.value)
        value['index'] = self.__settings.get_index(label)
        value['label'] = label
        self.value = json.dumps(value)


class TextValue(ColumnValue):

    def __init__(self, **kwargs):
        super(TextValue, self).__init__(kwargs)

    @property
    def text_value(self):
        if self.value:
            return json.loads(self.value)
        return self.value

    @text_value.setter
    def text_value(self, value: str):
        if value:
            self.text = value
            self.value = json.dumps(value)
        else:
            self.text = ''
            self.value = None


def create_column_value(column_type: ColumnType, **kwargs):

    if column_type is ColumnType.long_text:
        return LongTextValue(**kwargs)
    elif column_type is ColumnType.status:
        return StatusValue(**kwargs)
    elif column_type is ColumnType.text:
        return TextValue(**kwargs)


class StatusValueSettingsError(Exception):

    def __init__(self):
        self.message = 'Settings attribute is missing from input status column data.'