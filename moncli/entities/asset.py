from schematics import types
from schematics.models import Model

from .. import api_v2 as client, config
from ..decorators import default_field_list
from .user import User

class _Asset(Model):
    id = types.StringType(required=True)
    created_at = types.DateType()
    file_extension = types.StringType()
    file_size = types.IntType()
    name = types.StringType()
    public_url = types.StringType()
    url = types.StringType()
    url_thumbnail = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Asset(_Asset):
    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds', None)
        uploaded_by = kwargs.pop('uploaded_by', None)
        if uploaded_by:
            self.__uploaded_by = User(**uploaded_by)
        super(Asset, self).__init__(kwargs)

    @property
    def uploaded_by(self):
        if not self.__uploaded_by:
            self.__uploaded_by = self.get_uploaded_by_user()
        return self.__uploaded_by

    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_uploaded_by_user(self, *args):
        args = ['uploaded_by.' + arg for arg in args]
        user_data = client.get_assets(
            self.__creds.api_key_v2
            *args,
            ids=[self.id])[0]['uploaded_by']
        return User(**user_data)