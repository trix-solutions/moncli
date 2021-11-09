from datetime import datetime, timezone

from .. import DATE_FORMAT, TIME_FORMAT
from .base import ColumnValue

class ReadonlyValue(ColumnValue):
    """A readonly column value."""
    read_only = True


class FileValue(ReadonlyValue):
    """A file column value."""  
    native_type= list
    native_default= []

    def _convert(self, value):
        return value['files']


class LastUpdatedValue(ReadonlyValue):
    """An Last Updated column value."""

    native_type = datetime
    native_default = None

    def __init__(self, **kwargs):
        del kwargs['value']
        time_value = kwargs.pop('text', None)
        super().__init__(**kwargs)
        self._value = self._convert(time_value)

    def _convert(self, value):
        datetime_format = "{} {} {}".format(DATE_FORMAT,TIME_FORMAT,"%Z")
        utc_date = datetime.strptime(value,datetime_format)
        utc_date = utc_date.replace(tzinfo=timezone.utc)
        local_time = utc_date.astimezone(datetime.now().astimezone().tzinfo)
        return local_time


class SubitemsValue(ReadonlyValue):
    """An item link column value."""
    
    native_type = list
    native_default = []

    def _convert(self, value):
        try:
            list_ids = value['linkedPulseIds']
            item_ids = [id_value['linkedPulseId'] for id_value in list_ids ]
            return item_ids
        except KeyError:
            return []


class CreationLogValue(ReadonlyValue):
    """A Creation Log column value."""

    native_type = datetime
    native_default = None

    def __init__(self, **kwargs):
        del kwargs['value']
        time_value = kwargs.pop('text', None)
        super().__init__(**kwargs)
        self._value = self._convert(time_value)
    
    def _convert(self, value):
        datetime_format = "{} {} {}".format(DATE_FORMAT,TIME_FORMAT,"%Z")
        utc_date = datetime.strptime(value,datetime_format)
        utc_date = utc_date.replace(tzinfo=timezone.utc)
        local_time = utc_date.astimezone(datetime.now().astimezone().tzinfo)
        return local_time


