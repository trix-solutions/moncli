from .base import ColumnValue

class ReadonlyValue(ColumnValue):
    """A readonly column value."""
    read_only = True


class FileValue(ReadonlyValue):
    """A file column value.""" 
    pass


class SubitemsValue(ReadonlyValue):
    """An item link column value."""
    pass