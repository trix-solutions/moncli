import json, copy

from schematics.transforms import blacklist
from schematics.types import StringType

from .. import entities as en, ColumnValueError
from .constants import SIMPLE_NULL_VALUE, COMPLEX_NULL_VALUE


class _ColumnValue(en.BaseColumn):
    """Base column value model"""

    def __init__(self, **kwargs):
        self.text = kwargs.pop('text', None)
        self.additional_info = kwargs.pop('additional_info', None)
        super().__init__(**kwargs)


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
    allow_casts = ()
    native_type = None
    native_default = None

    def __init__(self, **kwargs):
        value = kwargs.pop('value', None)
        super().__init__(**kwargs)
        # Set serialized configured null value if no value.
        if value and value != self.null_value:
            value = json.loads(value)
            self._value = self._convert(value)
        else:
            self._value = copy.deepcopy(self.native_default)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.read_only:
            raise ColumnValueError('readonly_column_set', self.id, 'Cannot update value of read-only column "{}".'.format(self.title))
        if isinstance(value, self.allow_casts):
            self._value = self._cast(value)
        elif value == self.native_default or isinstance(value, self.native_type):
            self._value = value
        elif not value:
            self._value = copy.deepcopy(self.native_default)
        else:
            raise ColumnValueError('invalid_column_value', self.id,
                                   'Unable to set value "{}" to column "{}".'.format(value, self.title))

    @property
    def settings(self):
        return json.loads(self.settings_str)

    @property
    def additional_info_map(self):
        return json.dumps(self.additional_info)

    def format(self):
        if self.read_only:
            raise ColumnValueError(
                'readonly_column_format', 
                self.id, 
                'Cannot format value for read-only column "{}".'.format(self.title))
        if self.value == self.native_default:
            return self.null_value
        return self._format()


    def to_primitive(self):
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            additional_info=self.additional_info,
            value=self.value)


    def __repr__(self):
        return str({
            'id': self.id,
            'title': self.title,
            'value': self.value
        })

    def _convert(self, value):
        return value

    def _cast(self, value):
        return self.native_type(value)

    def _format(self):
        return str(self.value)


class SimpleNullValue(ColumnValue):
    null_value = SIMPLE_NULL_VALUE


class ComplexNullValue(ColumnValue):
    null_value = COMPLEX_NULL_VALUE
