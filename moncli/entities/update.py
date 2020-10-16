from schematics import types
from schematics.models import Model

from .. import api_v2 as client, config, entities as en
from ..api_v2 import constants
from ..decorators import default_field_list, optional_arguments


class _Update(Model):
    id = types.StringType(required=True)
    creator_id = types.StringType(required=True)
    item_id = types.StringType(required=True)
    body = types.StringType()
    created_at = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()


class Update(_Update):
    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        replies = kwargs.pop('replies', [])
        super(Update, self).__init__(kwargs)
        self.__replies = [Reply(creds=self.__creds, item_id=self.item_id, **reply) for reply in replies]
        self.__creator = None

    def __repr__(self):
        o = self.to_primitive()
        if len(self.__replies) > 0:
            o['replies'] = self.__replies
        return str(o)

    @property
    def creator(self):
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator

    @property
    def replies(self):
        return self.__replies

    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_creator(self, *args):
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)

    def add_file(self, file_path: str, *args):
        asset_data = client.add_file_to_update(
            self.__creds.api_key_v2,
            self.id,
            file_path,
            *args)
        return en.Asset(**asset_data)


class _Reply(Model):
    id = types.StringType(required=True)
    creator_id = types.StringType(required=True)
    body = types.StringType()
    created_at = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()


class Reply(_Reply):
    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__item_id = kwargs.pop('item_id')
        self.__creator = None
        super(Reply, self).__init__(kwargs)

    def __repr__(self):
        return str(self.to_primitive())

    @property
    def creator(self):
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator
    
    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_creator(self, *args):
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)