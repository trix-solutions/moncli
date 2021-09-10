import json

from schematics.transforms import blacklist
from schematics.types import StringType

from ...error import ColumnValueError
from .. import entities as en

class _ColumnValue(en.BaseColumn):
    """Base column value model"""

    text = StringType()
    additional_info = StringType()

    class Options:
        roles = {'default': blacklist('settings_str')}

    def __repr__(self):
        return str(self.to_primitive())

    def format(self):
        return self.to_primitive()


class ColumnValue(_ColumnValue):
    """The value of an items column.

    Properties
 
        additional_info : `json`
            The column value's additional information.
        id : `str`
            The column's unique identifier.
        text : `str`
            The column's textual value in string form.
        title : `str`
            The columns title.
        type : `str`
            The column's type.
        value : `any`
            The column's value in a Python native format.
        settings_str: `str`
            The column's unique settings.

    Methods

        format : `dict`
            Format for column value update.
        set_value : `void`
            Sets the value of the column.
    """

    null_value = None
    read_only = False
    is_simple = False
    allow_casts = ()
    native_type = None
    native_default = None

    def __init__(self, **kwargs):
        value = kwargs.pop('value', None)
        super(ColumnValue, self).__init__(kwargs)
        # Set seriaized configured null value if no value.
        if value == self.null_value:
            self._value = None
        value = json.loads(value)
        self._value = self._convert(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, self.allow_casts):
            self._value = self._cast(value)
        elif isinstance(value, self.native_type):
            self._value = value
        raise ColumnValueError('invalid_column_value', self.id, 'Unable to set value "{}" to column "{}".'.format(value, self.title))

    @property
    def settings(self):
        return json.dumps(self.settings_str)

    @property
    def additional_info_map(self):
        return json.dumps(self.additional_info)

    def format(self):
        if self.read_only:
            raise ColumnValueError('readonly_column', self.id, 'Cannot format value for read-only column "{}".'.format(self.title))

    def _convert(self, value):
        return value

    def _cast(self, value):
        return value
