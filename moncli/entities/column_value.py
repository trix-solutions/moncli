import json
from importlib import import_module

from schematics.models import Model
from schematics.types import StringType

from .. import config
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


class DropdownValue(ColumnValue):

    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('dropdown')

        super(DropdownValue, self).__init__(kwargs)

    def format(self):
        """
        if self.label is not None:
            return { 'label': self.label }
        if self.ids is not None:
            return { 'ids': self.ids }
        """
        return {} 


class LongTextValue(ColumnValue):

    def __init__(self, **kwargs):
        super(LongTextValue, self).__init__(kwargs)

    @property
    def long_text(self):
        if self.value:
            return json.loads(self.value)['text']
        return self.value
    
    @long_text.setter
    def long_text(self, value):
        if value:
            self.text = value
            current_value = json.loads(self.value)
            current_value['text'] = value
            self.value = json.dumps(current_value)
        else:
            self.text = ''
            self.value = None

    def format(self):
        if self.long_text:
            return {'text': self.long_text}
        return {}


class NumberValue(ColumnValue):

    def __init__(self, **kwargs):
        super(NumberValue, self).__init__(kwargs)

    @property
    def number(self):
        if not self.value:
            return self.value
        value = json.loads(self.value)
        if self.__isint(value):
            return int(value)
        if self.__isfloat(value):
            return float(value)

    @number.setter
    def number(self, value):
        if not self.__isint(value) and not self.__isfloat(value):
            raise NumberValueError()
        self.text = str(value)
        self.value = json.dumps(self.text)

    def format(self):
        if self.number:
            return str(self.number)
        return ''

    def __isfloat(self, value):
        try:
            float(value)
        except ValueError:
            return False

        return True
  
    def __isint(self, value):
        try:
            a = float(value)
            b = int(a)
        except ValueError:
            return False

        return a == b


class StatusValue(ColumnValue):

    def __init__(self, **kwargs):
        try:
            self.__settings = kwargs.pop('settings')
        except KeyError:
            raise ColumnValueSettingsError('status')

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
    return getattr(
        import_module(__name__), 
        config.COLUMN_TYPE_VALUE_MAPPINGS[column_type])(**kwargs)


class ColumnValueSettingsError(Exception):

    def __init__(self, column_type: str):
        self.message = 'Settings attribute is missing from input {} column data.'.format(column_type)


class NumberValueError(Exception):

    def __init__(self):
        self.message = 'Set value must be a valid integer or float.'