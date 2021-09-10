from importlib import import_module

from .constants import *
from .objects import *
from .base import *
from .simple import *
from .complex import *
from .readonly import *


def create_column_value(column_type: ColumnType, **kwargs):
    """Create column value instance

    Parameters

        column_type : `moncli.ColumnType`
            The column type to create.
        kwargs : `dict`
            The raw column value data.
    """

    return getattr(
        import_module(__name__), 
        COLUMN_TYPE_VALUE_MAPPINGS.get(column_type, 'ReadonlyValue'))(**kwargs)

