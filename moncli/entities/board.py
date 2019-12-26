from schematics.models import Model
from schematics.types import StringType, IntType, ListType, ModelType

import moncli.entities.exceptions as ex, moncli.entities.objects as o
import moncli.columnvalue as cv
from .. import api_v2 as client
from .. import config
from ..enums import ColumnType
from ..config import COLUMN_TYPE_MAPPINGS
from .group import Group
from .item import Item

class _Board(Model):

    id = StringType(required=True)
    name = StringType()
    board_folder_id = IntType()
    board_kind = StringType()
    description = StringType()
    permissions = StringType()
    pos = StringType()
    state = StringType()


class Board(_Board):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds', None)
        self.__columns = None
        self.__groups = None
        self.__items = None

        super(Board, self).__init__(kwargs)


    def __repr__(self):
        o = self.to_primitive()

        if self.__columns:
            o['columns'] = [column.to_primitive() for column in self.__columns]
        if self.__items:
            o['items'] = [item.to_primitive() for item in self.__items]
        
        return str(o)


    @property
    def items(self):
        if not self.__items:
            self.__items = self.get_items()
        return self.__items

    
    @property
    def columns(self):
        if not self.__columns:
            self.__columns = self.get_columns()
        return self.__columns


    def add_column(self, title:str, column_type: ColumnType):
        
        column_data = client.create_column(
            self.__creds.api_key_v2, 
            self.id, 
            title, 
            column_type, 
            'id', 'title', 'type')

        return o.Column(creds=self.__creds, **column_data)

    
    def get_columns(self):

        field_list = ['columns.' + field for field in config.DEFAULT_COLUMN_QUERY_FIELDS]
        column_data = client.get_boards(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.id)],
            limit=1)[0]['columns']

        return [o.Column(data) for data in column_data]


    def add_group(self, group_name: str):

        group_data = client.create_group(
            self.__creds.api_key_v2,
            self.id,
            group_name,
            'id', 'title')

        return Group(
            creds=self.__creds,
            board_id=self.id,
            **group_data)


    def get_groups(self):

        field_list = ['groups.id', 'groups.title', 'groups.archived', 'groups.color', 'groups.deleted', 'groups.items.id', 'groups.position']

        if self.__groups == None:
            
            board = client.get_boards(
                self.__creds.api_key_v2,
                *field_list,
                ids=[int(self.id)])[0]

            self.__groups = {
                group_data['id']: Group(creds=self.__creds, board_id=self.id, **group_data)
                for group_data
                in board['groups']
            }

        return list(self.__groups.values()) 

    
    def get_group(self, id: str = None, title: str = None):
        
        if id is None and title is None:
            raise ex.NotEnoughGetGroupParameters()

        if id is not None and title is not None:
            raise ex.TooManyGetGroupParameters()

        groups = self.get_groups()
        if id is not None:
            return self.__groups[id]
        else:
            return [group for group in groups if group.title == title][0]


    def add_item(self, item_name: str, group_id: str = None, column_values = None):

        kwargs = {}

        if group_id is not None:
            kwargs['group_id'] = group_id

        if column_values is not None:
            if type(column_values) == dict:
                kwargs['column_values'] = column_values
            elif type(column_values) == list:
                kwargs['column_values'] = { value.id: value.format() for value in column_values }
            else:
                raise ex.InvalidColumnValue(type(column_values).__name__)

        item_data = client.create_item(
            self.__creds.api_key_v2, 
            item_name, 
            self.id, 
            'id', 'name', 'board.id', 
            **kwargs)

        return Item(creds=self.__creds, **item_data)


    def get_items(self, *args):
        
        if len(args) == 0:
            field_list = config.DEFAULT_ITEM_QUERY_FIELDS

        field_list = ['items.' + field for field in field_list]

        items_data = client.get_boards(
            self.__creds.api_key_v2,
            *field_list, 
            ids=[int(self.id)])[0]['items']

        return [Item(creds=self.__creds, **item_data) for item_data in items_data] 


    def get_items_by_column_values(self, column_value: cv.ColumnValue, **kwargs):
        
        field_list = [
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'group.id',
            'state',
            'subscribers.id'
        ]

        if type(column_value) == cv.DateValue:
            value = column_value.date
        elif type(column_value) == cv.StatusValue:
            value = column_value.label
        else:
            value = column_value.format()

        items_data = client.get_items_by_column_values(
            self.__creds.api_key_v2, 
            self.id, 
            column_value.id, 
            value, 
            *field_list,
            **kwargs)

        return [Item(creds=self.__creds, **item_data) for item_data in items_data]


    def get_column_values(self):
        pass


    def get_column_value(self, id: str = None, title: str = None, **kwargs):

        if id is None and title is None:
            raise ex.NotEnoughGetColumnValueParameters()

        if id is not None and title is not None:
            raise ex.TooManyGetColumnValueParameters()

        columns = { column.id: column for column in self.get_columns() }

        if id is not None:

            column = columns[id]
            column_type = COLUMN_TYPE_MAPPINGS[column.type]
            

        elif title is not None:

            column = [column for column in columns.values() if column.title == title][0]
            column_type = COLUMN_TYPE_MAPPINGS[column.type]

        if column_type == ColumnType.status:
            kwargs['settings'] = column.settings
        
        return cv.create_column_value(column.id, ColumnType[column_type], column.title, **kwargs)

        