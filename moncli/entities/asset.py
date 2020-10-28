from schematics import types
from schematics.models import Model

from .. import api_v2 as client, config
from ..api_v2 import constants
from .user import User

class _Asset(Model):
    """Asset base model."""
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
    """A file uploaded to monday.com.
  
    __________
    Properties

        id : `str`
            The file's unique identifier.
        created_at : `str`
            The file's creation date.
        file_extension : `str`
            The file's extension.
        file_size : `int`
            The file's size in bytes.
        name : `str`
            The file's name.
        public_url : `str`
            Public url to the asset, valid for 1 hour.
        uploaded_by : `moncli.entities.User`
            The user who uploaded the file.
        url : `str`
            The file url.
        url_thumbnail : `str`
            Url to view the asset in thumbnail mode. Only available for images.

    _______
    Methods

        get_uploaded_by_user : `moncli.entities.User`
            Get the user who uploaded the file.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds', None)
        uploaded_by = kwargs.pop('uploaded_by', None)
        if uploaded_by:
            self.__uploaded_by = User(**uploaded_by)
        super(Asset, self).__init__(kwargs)

    @property
    def uploaded_by(self):
        """The user who uploaded the file."""

        if not self.__uploaded_by:
            self.__uploaded_by = self.get_uploaded_by_user()
        return self.__uploaded_by


    def get_uploaded_by_user(self, *args):
        """Get the user who uploaded the file.

        __________
        Parameters

            args : `tuple`
                The list of user return fields.
  
        _______
        Returns

            user : `moncli.entities.User`
                The user who uploaded the file.
        
        _____________
        Return Fields

            account : `moncli.entities.Account`
                The user's account.
            birthday : `str`
                The user's birthday.
            country_code : `str`
                The user's country code.
            created_at : `str`
                The user's creation date.
            email : `str`
                The user's email.
            enabled : `bool`
                Is the user enabled or not.
            id : `str`
                The user's unique identifier.
            is_guest : `bool`
                Is the user a guest or not.
            is_pending : `bool`
                Is the user a pending user.
            is_view_only : `bool`
                Is the user a view only user or not.
            join_date : `str`
                The date the user joined the account.
            location : `str`
                The user' location.
            mobile_phone : `str`
                The user's mobile phone number.
            name : `str`
                The user's name.
            phone : `str`
                The user's phone number.
            photo_original : `str`
                The user's photo in the original size.
            photo_small : `str`
                The user's photo in small size (150x150).
            photo_thumb : `str`
                The user's photo in thumbnail size (100x100).
            photo_thumb_small : `str`
                The user's photo in small thumbnail size (50x50).
            photo_tiny : `str`
                The user's photo in tiny size (30x30).
            teams : `list[moncli.entities.Team]`
                The teams the user is a member in.
            time_zone_identifier : `str`
                The user's time zone identifier.
            title : `str`
                The user's title.
            url : `str`
                The user's profile url.
            utc_hours_diff : `int`
                The user's UTC hours difference.
        """
        
        args = ['uploaded_by.' + arg for arg in client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS)]
        user_data = client.get_assets(
            self.__creds.api_key_v2
            *args,
            ids=[self.id])[0]['uploaded_by']
        return User(**user_data)