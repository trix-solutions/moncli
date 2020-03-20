from .. import api_v2 as client, columnvalue as cv
from ..entities import objects as o
from ..enums import ColumnType
from ..constants import COLUMN_TYPE_MAPPINGS
from . import exceptions as ex
from .group import Group
from .item import Item

class Board():

    def __init__(self, **kwargs):
        self.__groups = None
        self.__creds = kwargs['creds']

        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            if key == 'board_folder_id':
                self.board_folder_id = value
            
            elif key == 'board_kind':
                self.board_kind = value

            elif key == 'description':
                self.description = value

            elif key == 'items':
                self.__item_ids = [int(item['id']) for item in value]

            elif key == 'owner':
                self.__owner_id: str = value['id']

            elif key == 'permissions':
                self.permissions = value

            elif key == 'pos':
                self.position = value

            elif key == 'state':
                self.state = value


    def add_column(self, title:str, column_type: ColumnType):
        
        column_data = client.create_column(
            self.__creds.api_key_v2, 
            self.id, 
            title, 
            column_type, 
            'id', 'title', 'type')

        return o.Column(creds=self.__creds, **column_data)

    
    def get_columns(self):

        board = client.get_boards(
            self.__creds.api_key_v2,
            'columns.id',
            'columns.archived',
            'columns.settings_str',
            'columns.title',
            'columns.type',
            'columns.width',
            ids=[int(self.id)])

        return [o.Column(creds=self.__creds, **column_data) for column_data in board[0]['columns']]


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


    def get_items(self):
        
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

        if not hasattr(self, '__item_ids'):

            items = client.get_boards(
                self.__creds.api_key_v2,
                'items.id', 
                ids=[int(self.id)])[0]['items']

            self.__item_ids = [int(item['id']) for item in items]

        items_data = client.get_items(
            self.__creds.api_key_v2, 
            *field_list,
            ids=self.__item_ids, 
            limit=1000)

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

        