from .. import entities as en
from ..enums import *

## Column type mappings
COLUMN_TYPE_MAPPINGS = {
    'boolean': ColumnType.checkbox,
    'country': ColumnType.country,
    'date': ColumnType.date,
    'dropdown': ColumnType.dropdown,
    'dependency': ColumnType.dependency,
    'email': ColumnType.email,
    'hour': ColumnType.hour,
    'link': ColumnType.link,
    'location': ColumnType.location,
    'long-text': ColumnType.long_text,
    'name': ColumnType.name,
    'numeric': ColumnType.numbers,
    'multiple-person': ColumnType.people,
    'phone': ColumnType.phone,
    'pulse-updated': ColumnType.last_updated,
    'rating': ColumnType.rating,
    'color': ColumnType.status,
    'tag': ColumnType.tags,
    'team': ColumnType.team,
    'text': ColumnType.text,
    'timerange': ColumnType.timeline,
    'week': ColumnType.week,
    'timezone': ColumnType.world_clock,
    'file': ColumnType.file,
    'board-relation': ColumnType.board_relation,
    'subtasks': ColumnType.subitems,
    'pulse-log': ColumnType.creation_log
}


class BaseColumn(object):
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.title = kwargs.pop('title', None)
        self.settings_str = kwargs.pop('settings_str', None)


class Column(BaseColumn):
    """A board's column.
    
    Properties

        archived : `bool`
            Is the column archived or not.
        id : `str`
            The column's unique identifier.
        settings_str : `str`
            The column's settings in a string form.
        title : `str`
            The column's title.
        type : `str`
            The column's type.
        column_type : `moncli.entities.ColumnType`
            The column's type as an enum.
        width : `int`
            The column's width.
    """

    def __init__(self, **kwargs):
        self.archived = kwargs.pop('archived', None)
        self.type = kwargs.pop('type', None)
        self.width = kwargs.pop('width', None)
        super().__init__(**kwargs)
    
    def __repr__(self):
        return str(self.to_primitive())
    
    @property
    def column_type(self):
        # TODO - Find something else other than auto-number to default to.
        return COLUMN_TYPE_MAPPINGS.get(self.type, ColumnType.auto_number)

    def to_primitive(self):
        return dict(
            id=self.id,
            title=self.title,
            type=self.type,
            archived=self.archived,
            settings_str=self.settings_str,
            width=self.width)


class BaseColumnCollection(en.BaseCollection):
    
    def __init__(self, column_values: list = []):

        def get_index(index):
            if not isinstance(index, (int, str)):
                raise TypeError('Expected index type of int or str, got "{}" instead.'.format(index.__class__.__name__))
            if isinstance(index, (int,)):   
                return index
            for i in range(len(self._values)):
                column = self._values[i]
                if column.id == index or column.title == index:
                    return i
            raise KeyError('Collection contains no value for key "{}".'.format(index))

        super().__init__(column_values, BaseColumn, get_index)