from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, entities as en

class _Group(Model):

    id = types.StringType(required=True)
    title = types.StringType()
    archived = types.BooleanType()
    color = types.StringType()
    deleted = types.BooleanType()
    position = types.StringType()


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

    @property
    def items(self):
        if not self.__items:
            self.__items = self.get_items()
        return self.__items

    def duplicate(self, add_to_top: bool = False):
        field_list = config.DEFAULT_GROUP_QUERY_FIELDS
        group_data = client.duplicate_group(
            self.__creds.api_key_v2, 
            self.__board_id, 
            self.id, 
            *field_list)

        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)

    def archive(self):
        field_list = config.DEFAULT_GROUP_QUERY_FIELDS
        group_data = client.archive_group(
            self.__creds.api_key_v2,
            self.__board_id,
            self.id, 
            *field_list)

        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)

    def delete(self):
        field_list = config.DEFAULT_GROUP_QUERY_FIELDS
        group_data = client.delete_group(
            self.__creds.api_key_v2,
            self.__board_id,
            self.id, 
            *field_list)

        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)

    def add_item(self, item_name: str, **kwargs):
        field_list = config.DEFAULT_GROUP_QUERY_FIELDS
        item_data = client.create_item(
            self.__creds.api_key_v2,
            item_name,
            self.__board_id, 
            *field_list,
            group_id=self.id,
            **kwargs)

        return en.Item(creds=self.__creds, **item_data)

    def get_items(self):
        field_list = ['groups.items.' + field for field in config.DEFAULT_ITEM_QUERY_FIELDS]
        items_data = client.get_boards(
            self.__creds.api_key_v2, 
            *field_list,
            ids=[int(self.__board_id)],
            group_ids=[self.id], 
            limit=1)[0]['groups'][0]['items']

        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data]