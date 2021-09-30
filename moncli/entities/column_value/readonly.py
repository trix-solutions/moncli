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