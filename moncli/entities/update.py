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
        self.__creator = None
        creator = kwargs.pop('creator', None)
        if creator:
            self.__creator = en.User(cred=self.__creds, **creator)
        self.__replies = None
        replies = kwargs.pop('replies', None)
        if replies:
            self.__reply = [Reply(creds=self.__creds, item_id=self.item_id, **reply) for reply in replies]
        self.__assets = None
        assets = kwargs.pop('assets')
        if assets:
            self.__assets = [en.Asset(creds=self.__creds, **asset) for asset in assets]
        super(Update, self).__init__(kwargs)

    def __repr__(self):
        o = self.to_primitive()
        if len(self.__replies) > 0:
            o['replies'] = self.__replies
        return str(o)

    @property
    def creator(self):
        """The update's creator."""
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator

    @property
    def replies(self):
        """The update's replies."""
        return self.__replies

    @property
    def assets(self):
        """The update's assets/files."""
        return self.__assets

    def get_creator(self, *args):
        args = client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS)
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)

    def add_reply(self, body: str, *args):
        update_data = client.create_update(
            self.__creds.api_key_v2,
            body,
            self.item_id,
            *args,
            parent_id=self.id)
        return en.Update(creds=self.__creds, **update_data)

    def add_file(self, file_path: str, *args):
        asset_data = client.add_file_to_update(
            self.__creds.api_key_v2,
            self.id,
            file_path,
            *args)
        return en.Asset(**asset_data)

    def get_files(self, *args):
        return None


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
    
    def get_creator(self, *args):
        args = client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS)
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)