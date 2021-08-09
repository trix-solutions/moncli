import json, pytz, importlib
from moncli.models import MondayModel
from datetime import datetime, timedelta

from schematics.exceptions import ValidationError
from schematics.types import BaseType

from moncli import client
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
        return value != self.original_value

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
        if not value: return {}
        return {'checked': 'true'}

    def validate_checkbox(self, value):
        if type(value) is not bool:
            raise ValidationError('Value is not a valid checkbox type: ({}).'.format(value))

    def value_changed(self, value):
        try:
            orig = bool(self.original_value['checked'])
        except: 
            orig = False
        try:
            new = bool(value['checked'])
        except:
            new = False
        return orig != new


class DateType(MondayType):

    def to_native(self, value, context):
        if not isinstance(value, cv.ColumnValue):
            return value
        value = super().to_native(value, context=context)
        try:
            self.metadata['changed_at'] = self._get_local_changed_at(value['changed_at'])
        except:
            pass

        date = datetime.strptime(value['date'], DATE_FORMAT) 
        try:
            if value['time'] != None:
                date = pytz.timezone('UTC').localize(date)
                time = datetime.strptime(value['time'], TIME_FORMAT)
                date = date + timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
                return date.astimezone(datetime.now().astimezone().tzinfo)
        except:
            pass

        return date

    def to_primitive(self, value, context=None):
        pre_time = datetime.strftime(value, TIME_FORMAT)
        if pre_time == '00:00:00':
            time = None
        value = value.astimezone(pytz.timezone('UTC'))
        date = datetime.strftime(value, DATE_FORMAT)   
        if time:
            time = datetime.strftime(value, TIME_FORMAT)

        return {
            'date': date,
            'time': time
        }

    def validate_date(self, value):
        if not isinstance(value, datetime):
            raise ValidationError('Invalid datetime type.')

    def value_changed(self, value):
        for k, v in value.items():
            if self.original_value[k] != v:
                return True
        return False

class ItemLinkType(MondayType):

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value

        value = super().to_native(value, context=context)
        try:
            self.metadata['changed_at'] = self._get_local_changed_at(value['changed_at'])
        except:
            pass
        try:
            self.original_value = [id['linkedPulseId'] for id in value['linkedPulseIds']]
        except:
            self.original_value = []
        
        if not self._allow_multiple_values():
            try:
                return str(self.original_value[0])
            except:
                return None
        return [str(value) for value in self.original_value]

    def to_primitive(self, value, context = None):
        if value == None:
            value = []
        if type(value) is not list:
            return {'item_ids': [int(value)]}
        return {'item_ids': value}

    def validate_itemlink(self, value):
        if not self._allow_multiple_values():
            if value != None and type(value) == list:
                raise ValidationError('Multiple items for this item link property are not supported.')
        else:
            if value and type(value) != list:
                raise ValidationError('Item link property requires a list value for multiple items.')

    def value_changed(self, value):
        if not self._allow_multiple_values():
            return value['item_ids'] != self.original_value
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


class LongTextType(MondayType):

    def to_native(self, value, context):
        if not isinstance(value, cv.ColumnValue):
            return value
        value = super().to_native(value, context=context)
        if value == COMPLEX_NULL_VALUE:
            return None
        try:
            self.metadata['changed_at'] = self._get_local_changed_at(value['changed_at'])
        except:
            pass
        return value['text']

    def to_primitive(self, value, context = None):
        if not value: 
            return COMPLEX_NULL_VALUE
        return {'text': value}

    def validate_text(self, value):
        if type(value) is not str:
            raise ValidationError('Value is not a valid long text type: ({}).'.format(value))

    def value_changed(self, value):
        return self.original_value['text'] != value['text']


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

    def to_primitive(self, value, context = None):
        if not value:
            return SIMPLE_NULL_VALUE
        return str(value)

    def validate_number(self, value):
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


class StatusType(MondayType):

    def __init__(self, id: str = None, title: str = None, data_mapping: dict = None, *args, **kwargs):
        self._data_mapping = data_mapping
        super(StatusType, self).__init__(id=id, title=title, *args, **kwargs)

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value
        super(StatusType, self).to_native(value, context)
        if not self._data_mapping:
            return value.text
        try:
            return self._data_mapping[value.text]
        except:
            return None

    def to_primitive(self, value, context = None):
        if self._data_mapping:
            reverse = {v: k for k, v in self._data_mapping.items()}
            value = reverse[value]
        for k, v in self.metadata['labels'].items():
            if value == v:
                return {'index': int(k)}
        return self.original_value

    def validate_status(self, value):
        if self._data_mapping:
            reverse = {v: k for k, v in self._data_mapping.items()}
            value = reverse[value]
        if value not in self.metadata['labels'].values():
            raise ValidationError('Unable to find index for status label: ({}).'.format(value))

    def value_changed(self, value):
        return self.original_value['index'] != value['index']


class SubitemsType(MondayType):

    def __init__(self, _type: MondayModel, id: str = None, title: str = None, *args, **kwargs):
        if not issubclass(_type, MondayModel):
            raise MondayTypeError('The input class type is not a Monday Model: ({})'.format(_type.__name__))
        self.type = _type
        super(SubitemsType, self).__init__(id, title, *args, **kwargs)

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value
        item_ids = [item['linkedPulseId'] for item in json.loads(value.value)['linkedPulseIds']]
        self.original_value = {'item_ids': item_ids}
        items = client.get_items(ids=item_ids, get_column_values=True)
        
        value = []
        module = importlib.import_module(self.type.__module__)
        for item in items:
            value.append(getattr(module, self.type.__name__)(item))

        return value

    def validate_subitems(self, value):
        if type(value) is not list:
            raise ValidationError('Value is not a valid subitems list: ({}).'.format(value))
        for val in value:
            if not isinstance(val, self.type):
                raise ValidationError('Value is not a valid instance of subitem type: ({}).'.format(value.__class__.__name__))

    def to_primitive(self, value, context = None):
        return value

    def value_changed(self, value):
        return False


class TextType(MondayType):

    def to_native(self, value, context = None):
        if not isinstance(value, cv.ColumnValue):
            return value
        return super(TextType, self).to_native(value, context)

    def to_primitive(self, value, context = None):
        if not value:
            return ''
        return value

    def validate_text(self, value):
        if type(value) is not str:
            raise ValidationError('Value is not a valid text type: ({}).'.format(value))


class TimelineType(MondayType):

    def to_native(self, value, context):
        if isinstance(value, Timeline):
            return value
        value = super().to_native(value, context=context)
        try:
            return Timeline(
                datetime.strptime(value['from'], DATE_FORMAT),
                datetime.strptime(value['to'], DATE_FORMAT))
        except:
            raise MondayTypeError(message='Invalid data for timeline type: ({}).'.format(value))

    def to_primitive(self, value, context = None):
        if not value:
            return COMPLEX_NULL_VALUE
        return {
            'from': datetime.strftime(value.from_date, DATE_FORMAT),
            'to': datetime.strftime(value.to_date, DATE_FORMAT)
        }

    def validate_timeline(self, value):
        if type(value) is not Timeline:
            raise ValidationError('Value is not a valid timeline type: ({}).'.format(value))

    def value_changed(self, value):
        for k in value.keys():
            if value[k] != self.original_value[k]:
                return True
        return False

    
class WeekType(MondayType):

    def to_native(self, value, context):
        if isinstance(value, Week):
            return value
        if type(value) is dict:
            return Week(value['start'], value['end'])
        value = super(WeekType, self).to_native(value, context=context)
        try:
            week_value = value['week']
            return Week(datetime.strptime(
                week_value['startDate'], DATE_FORMAT), 
                datetime.strptime(week_value['startDate'], DATE_FORMAT))
        except:
            raise MondayTypeError(message='Invalid data for week type: ({})'.format(value))

    def to_primitive(self, value, context = None):
        if not value:
            return COMPLEX_NULL_VALUE
        
        return { 
            'week': {
                'startDate': datetime.strftime(value.start, DATE_FORMAT),
                'endDate': datetime.strftime(value.end, DATE_FORMAT)
            }
        }

    def validate_week(self, value):
        if type(value) is not Week:
            raise ValidationError('Value is not a valid week type: ({}).'.format(value))
        if not value.start:
            raise ValidationError('Value is mssing a start date: ({}).'.format(value))
        if not value.end:
            raise ValidationError('Value is mssing an end date: ({}).'.format(value))
            
    def value_changed(self, value):
        orig_week = self.original_value['week']
        new_week = value['week']
        for k in new_week.keys():
            if new_week[k] != orig_week[k]:
                return True
        return False


class Timeline():

    def __init__(self, from_date = None, to_date = None):
        self.from_date = from_date
        self.to_date = to_date

    def __repr__(self):
        return str({
            'from': datetime.strftime(self.from_date, DATE_FORMAT),
            'to': datetime.strftime(self.to_date, DATE_FORMAT)
        })


class Week():

    def __init__(self, start = None, end = None):
        self._start = start
        self._end = end
        self._calculate_dates(start)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._calculate_dates(value)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        return self._calculate_dates(value)

    @property
    def week_number(self):
        return self._week_number

    def _calculate_dates(self, value):
        if not value:
            return value   
        self._start = value - timedelta(days=value.weekday())
        self._end = self._start + timedelta(days=6)
        self._week_number = self._start.isocalendar()[1]

    def __repr__(self):
        return str({
            'startDate': self._start,
            'endDate': self._end
        })

class MondayTypeError(Exception):
    def __init__(self, message: str = None, messages: dict = None, error_code: str = None):
        self.error_code = error_code
        if message:
            super(MondayTypeError, self).__init__(message)
        elif messages:
            super(MondayTypeError, self).__init__(messages)