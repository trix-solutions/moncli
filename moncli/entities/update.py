from schematics import types
from schematics.models import Model

from .. import api_v2 as client, config, entities as en

class Update(Model):
    id = types.StringType(required=True)
    creator_id = types.StringType(required=True)
    item_id = types.StringType(required=True)
    body = types.StringType()
    create_at = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__replies = [Reply(creds=self.__creds, item_id=self.item_id, **reply_data) for reply_data in kwargs.pop('replies', [])]
        self.__creator = None
        super(Update, self).__init__(kwargs)

    def __repr__(self):
        return str(self.to_primitive())

    @property
    def creator(self):
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator

    @property
    def replies(self):
        return self.__replies

    def get_creator(self):
        field_list = config.DEFAULT_USER_QUERY_FIELDS
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)


class Reply(Model):
    id = types.StringType(required=True)
    creator_id = types.StringType(required=True)
    body = types.StringType()
    create_at = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()

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

    def get_creator(self):
        field_list = config.DEFAULT_USER_QUERY_FIELDS
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)