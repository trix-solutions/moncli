import json, pytz
from datetime import datetime

from schematics.exceptions import ValidationError
from schematics.types import BaseType

from moncli.entities import column_value as cv

SIMPLE_NULL_VALUE = ''
COMPLEX_NULL_VALUE = {}
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
CHANGED_AT_FORMAT = '{}T{}.%fZ'.format(DATE_FORMAT, TIME_FORMAT)


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
        self.metadata['id'] = value.id
        self.metadata['title'] = value.title
        settings = json.loads(value.settings_str) if value.settings_str else {}
        for k, v in settings.items():
            self.metadata[k] = v
        self.original_value = json.loads(value.value)
        return self.original_value

    def value_changed(self, value):
        return value == self.original_value

    def _is_column_value(self, value):
        if not isinstance(value, cv.ColumnValue):
            return value

    def _get_local_changed_at(self, changed_at_str: str):
        try:
            changed_at = datetime.strptime(changed_at_str, CHANGED_AT_FORMAT)
            utc = pytz.timezone('UTC')
            changed_at = utc.localize(changed_at, is_dst=False)
            return changed_at.astimezone(datetime.now().astimezone().tzinfo)
        except:
            return None


class CheckboxType(MondayType):

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value
        value = super().to_native(value, context=context)
        try:
            return bool(value['checked'])
        except:
            return False

    def to_primitive(self, value, context = None):
        return {'checked': value}

    def validate_checkbox(self, value):
        if not self.value_changed(value):
            return
        if type(value) is not bool:
            raise ValidationError('Value is not a valid checkbox type: ({}).'.format(value))


class ItemLinkType(MondayType):

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value

        value = super().to_native(value, context=context)
        try:
            self.metadata['changed_at'] = self._get_local_changed_at(value['changed_at'])
        except:
            pass
        self.original_value = [str(id['linkedPulseId']) for id in value['linkedPulseIds']]
        
        if not self._allow_multiple_values():
            try:
                return self.original_value[0]
            except:
                return None
        return self.original_value

    def to_primitive(self, value, context = None):
        if value == None:
            value = []
        if not self._allow_multiple_values():
            if value:
                value = [{'linkedPulseId': value}]
        else:
            value = [{'linkedPulseId': int(id)} for id in value]
        return {'linkedPulseIds': value}

    def validate_itemlink(self, value):
        if not self.value_changed(value):
            return
        if not self._allow_multiple_values():
            if value != None and type(value) == list:
                raise ValidationError('Multiple items for this item link property are not supported.')
        else:
            if value and type(value) != list:
                raise ValidationError('Item link property requires a list value for multiple items.')

    def value_changed(self, value):
        if not self._allow_multiple_values():
            return value != self.original_value
        if type(value) != type(self.original_value):
            return True
        if len(value) != len(self.original_value):
            return False
        for v in value:
            if v not in self.original_value:
                return False
        return True

    def _allow_multiple_values(self):
        try:
            return self.metadata['allowMultipleItems']
        except KeyError:
            return True


class NumberType(MondayType):

    def to_native(self, value, context):
        if not isinstance(value, cv.ColumnValue):
            return value
        value = super().to_native(value, context=context)
        if value == SIMPLE_NULL_VALUE:
            return None
        if self._isint(value):
            return int(value)
        if self._isfloat(value):
            return float(value)

    def to_primitive(self, value, context=None):
        if not value:
            return SIMPLE_NULL_VALUE
        return str(value)

    def validate_number(self, value):
        if not self.value_changed(value):
            return
        if type(value) not in [int, float]:
            raise ValidationError('Value is not a valid number type: ({}).'.format(value))

    def _isfloat(self, value):
        """Is the value a float."""
        try:
            float(value)
        except ValueError:
            return False
        return True
  
    def _isint(self, value):
        """Is the value an int."""
        try:
            a = float(value)
            b = int(a)
        except ValueError:
            return False
        return a == b


class TextType(MondayType):

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value
        return super(TextType, self).to_native(value, context)

    def to_primitive(self, value, context=None):
        if not value:
            return ''
        return value

    def validate_text(self, value):
        if not self.value_changed(value):
            return
        if type(value) is not str:
            raise ValidationError('Value is not a valid text type: ({}).'.format(value))


class TimelineType(MondayType):

    def to_native(self, value, context):
        if isinstance(value, Timeline):
            return value
        if isinstance(value, cv.ColumnValue):
            value = super().to_native(value, context=context)
        try:
            return Timeline(
                datetime.strptime(value['from'], DATE_FORMAT),
                datetime.strptime(value['to'], DATE_FORMAT))
        except:
            raise MondayTypeError(message='Invalid data for timeline type: ({}).'.format(value))

    def to_primitive(self, value, context=None):
        if not value:
            return COMPLEX_NULL_VALUE
        return {
            'from': datetime.strftime(value.from_date, DATE_FORMAT),
            'to': datetime.strftime(value.to_date, DATE_FORMAT)
        }


class Timeline():

    def __init__(self, from_date = None, to_date = None):
        self.from_date = from_date
        self.to_date = to_date

    def __repr__(self):
        return str({
            'from': datetime.strftime(self.from_date, DATE_FORMAT),
            'to': datetime.strftime(self.to_date, DATE_FORMAT)
        })

class MondayTypeError(Exception):
    def __init__(self, message: str = None, messages: dict = None, error_code: str = None):
        self.error_code = error_code
        if message:
            super(MondayTypeError, self).__init__(message)
        elif messages:
            super(MondayTypeError, self).__init__(messages)