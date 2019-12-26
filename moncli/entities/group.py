from schematics.models import Model
from schematics.types import StringType, BooleanType

from .. import api_v2 as client
from .item import Item

class _Group(Model):

    id = StringType(required=True)
    title = StringType()
    archived = BooleanType()
    color = StringType()
    deleted = BooleanType()
    position = StringType()


class Group(_Group):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__board_id = kwargs.pop('board_id')
        self.__items = None
        super(Group, self).__init__(kwargs)

    
    def __repr__(self):
        o = self.to_primitive()

        if self.__items:
            o['items'] = [item.to_primitive() for item in self.__items]

        return str(o)
    

    def duplicate(self, add_to_top: bool = False):
        
        group_data = client.duplicate_group(
            self.__creds.api_key_v2, 
            self.__board_id, 
            self.id, 
            'id', 'title', 'items.id')

        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)


    def archive(self):
        
        group_data = client.archive_group(
            self.__creds.api_key_v2,
            self.__board_id,
            self.id,
            'id', 'title', 'archived')

        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)


    def delete(self):
        
        group_data = client.delete_group(
            self.__creds.api_key_v2,
            self.__board_id,
            self.id,
            'id', 'title', 'deleted')

        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)


    def add_item(self, item_name: str, **kwargs):
        
        item_data = client.create_item(
            self.__creds.api_key_v2,
            item_name,
            self.__board_id,
            'id', 'name', 'board.id',
            group_id=self.id,
            **kwargs)

        return Item(creds=self.__creds, **item_data)


    def get_items(self):

        if not hasattr(self, '__item_ids'):

            board = client.get_boards(
                self.__creds.api_key_v2,
                'groups.id', 'groups.items.id', 
                ids=[int(self.__board_id)])[0]

            group = [group for group in board['groups'] if group['id'] == self.id][0]
            self.__item_ids = [int(item['id']) for item in group['items']]


        items_data = client.get_items(
            self.__creds.api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'group.id',
            'state',
            'subscribers.id',
            ids=self.__item_ids, 
            limit=1000)

        return [Item(creds=self.__creds, **item_data) for item_data in items_data]