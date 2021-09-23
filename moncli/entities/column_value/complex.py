from moncli.error import ColumnValueError
from .base import ColumnValue, ComplexNullValue

class CheckboxValue(ColumnValue):
    """A checkbox column value."""
    pass


class CountryValue(ColumnValue):
    """A country column value."""
    pass


class HourValue(ColumnValue):
    """An hour column value."""
    pass


class ItemLinkValue(ComplexNullValue):
    """An item link column value."""
    native_type = list
    native_default = []

    def _convert(self, value):
        try:
            list_id = value['linkedPulseIds']
            item_id = [id_value['linkedPulseId'] for id_value in list_id ]
            return item_id
        except KeyError:
            return []

    def _format(self):
        item_ids = []
        list_value = self.value
        for value in list_value:
            try:
                value = int(value)
                item_ids.append(value)
            except ValueError:
                raise ColumnValueError(
                                    'invalid_item_id',
                                    self.id,
                                    'Invalid item ID "{}".'.format(list_value)
                                    )
        return dict(item_ids=item_ids)

class RatingValue(ColumnValue):
    """A rating column value."""
    pass


class TagsValue(ColumnValue):
    """A tags column value."""
    pass


class TimelineValue(ColumnValue):
    """A timeline column value."""
    pass
        

class TimezoneValue(ColumnValue):
    """A timezone column value."""
    pass


class WeekValue(ColumnValue):
    """A week column value."""
    pass