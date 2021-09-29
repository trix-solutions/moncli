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
    pass