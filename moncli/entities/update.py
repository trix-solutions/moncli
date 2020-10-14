from schematics import types
from schematics.models import Model

from .. import api_v2 as client, config, entities as en
from ..api_v2 import constants


class _Update(Model):
    """Update base model"""
    id = types.StringType(required=True)
    creator_id = types.StringType(required=True)
    item_id = types.StringType(required=True)
    body = types.StringType()
    created_at = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()


class Update(_Update):
    """An update
    
    __________
    Properties

        assets : `list[moncli.entities.Asset]`
            The update's assets/files.
        body: `str`
            The update's html formatted body.
        created_at: `str`
            The update's creation date.
        creator : `moncli.entities.User`
            The update's creator.
        creator_id : `str`
            The unique identifier of the update creator.
        id : `str`
            The update's unique identifier.
        item_id : `str`
            The update's item ID.
        replies : `list[moncli.entities.Reply]
            The update's replies.
        text_body : `str`
            The update's text body.
        updated_at : `str`
            The update's last edit date.
    
    _______
    Methods

        get_creator : `moncli.entities.User`
            Get the update's creator.
        add_reply : `moncli.entities.Reply`
            Add reply to update.
        get_replies : `list[moncli.entities.Reply]`
            Get update replies.
        add_file : `moncli.entities.Asset`
            Add a file to update.
        get_files : `list[moncli.entities.Asset]
            Get update's files.
        delete : `moncli.entity.Update`
            Delete an update.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__creator = None
        creator = kwargs.pop('creator', None)
        if creator:
            self.__creator = en.User(cred=self.__creds, **creator)
        self.__replies = None
        replies = kwargs.pop('replies', None)
        if replies:
            self.__replies = [Reply(creds=self.__creds, item_id=kwargs['item_id'], **reply) for reply in replies]
        self.__assets = None
        assets = kwargs.pop('assets', None)
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
        if not self.__replies:
            self.__replies = self.get_replies()
        return self.__replies

    @property
    def assets(self):
        """The update's assets/files."""
        return self.__assets

    def get_creator(self, *args):
        """Get the update's creator.
        __________
        Parameters

            args : `tuple`
                The list of user fields to return.

        _______
        Returns

            user : `moncli.entities.User`
                The update's creator.

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

        args = client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS)
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)


    def add_reply(self, body: str, *args):
        """Add reply to update.

        __________
        Parameters

            body : `str`
                The text body of the reply.
            args : `tuple`
                The list of reply fields to return.

        _______
        Returns

            update : `moncli.entities.Update`
                The updated update.

        _____________
        Return Fields

            assets : `list[moncli.entities.Asset]`
                The update's assets/files.
            body: `str`
                The update's html formatted body.
            created_at: `str`
                The update's creation date.
            creator : `moncli.entities.User`
                The update's creator
            creator_id : `str`
                The unique identifier of the update creator.
            id : `str`
                The update's unique identifier.
            item_id : `str`
                The update's item ID.
            replies : `list[moncli.entities.Reply]
                The update's replies.
            text_body : `str`
                The update's text body.
            updated_at : `str`
                The update's last edit date.
        """

        update_data = client.create_update(
            self.__creds.api_key_v2,
            body,
            self.item_id,
            *args,
            parent_id=self.id)
        return en.Update(creds=self.__creds, **update_data)


    def get_replies(self, *args):
        """Get update replies.
        __________
        Parameters

            args : `tuple`
                The list of update fields to return.

        _______
        Returns

            replies : `list[moncli.entities.Reply]`
                The update's replies.

        _____________
        Return Fields

            body : `str`
                The reply's html formatted body.
            created_at : `str`
                The reply's creation date.
            creator : `moncli.entities.User`
                The reply's creator.
            creator_id : `str`
                The unique identifier of the reply creator.
            id : `str`
                The reply's unique identifier.
            text_body : `str`
                The reply's text body.
            updated_at : `str`
                The reply's last edit date.
        """

         # Hard configure the pagination rate.
        page = 1
        page_limit = 500
        record_count = 500

        args = ['replies.{}'.format(arg) for arg in constants.DEFAULT_REPLY_QUERY_FIELDS]

        while record_count >= page_limit:
            updates_data = client.get_updates(
                self.__creds.api_key_v2, 
                'id', 'item_id', *args,
                limit=page_limit,
                page=page)
            
            try:
                target_update = [update for update in updates_data if update['id'] == self.id][0]
                return [Reply(creds=self.__creds, item_id=target_update['item_id'], **reply_data) for reply_data in target_update['replies']]
            except KeyError:
                if len(target_update) == 0:
                    page += 1
                    record_count = len(updates_data)
                    continue
        return [] 


    def add_file(self, file_path: str, *args):
        """Add a file to update.
        __________
        Parameters

            file_path : `str`
                The path to the file to upload.
            args : `tuple`
                The list of update fields to return.

        _______
        Returns

            asset : `moncli.entities.Asset`
                The newly created asset.

        _____________
        Return Fields

            created_at : `str`
                The file's creation date.
            file_extension : `str`
                The file's extension.
            file_size : `int`
                The file's size in bytes.
            id : `str`
                The file's unique identifier.
            name : `str`
                The file's name.
            public_url : `str`
                Public url to the asset, valid for 1 hour.
            uploaded_by : `moncli.entities.user.User`
                The user who uploaded the file
            url : `str`
                The user who uploaded the file
            url_thumbnail : `str`
                Url to view the asset in thumbnail mode. Only available for images.  
        """

        asset_data = client.add_file_to_update(
            self.__creds.api_key_v2,
            self.id,
            file_path,
            *args)
        return en.Asset(**asset_data)


    def get_files(self, *args):
        """Get update's files.

        __________
        Parameters

            args : `tuple`
                The list of asset fields to return.

        _______
        Returns

            assets : `list[moncli.entities.Asset]`
                The update's files.

        _____________
        Return Fields

            created_at : `str`
                The file's creation date.
            file_extension : `str`
                The file's extension.
            file_size : `int`
                The file's size in bytes.
            id : `str`
                The file's unique identifier.
            name : `str`
                The file's name.
            public_url : `str`
                Public url to the asset, valid for 1 hour.
            uploaded_by : `moncli.entities.user.User`
                The user who uploaded the file
            url : `str`
                The user who uploaded the file
            url_thumbnail : `str`
                Url to view the asset in thumbnail mode. Only available for images.  
        """

         # Hard configure the pagination rate.
        page = 1
        page_limit = 500
        record_count = 500

        args = ['assets.{}'.format(arg) for arg in constants.DEFAULT_ASSET_QUERY_FIELDS]

        while record_count >= page_limit:
            updates_data = client.get_updates(
                self.__creds.api_key_v2, 
                'id', *args,
                limit=page_limit,
                page=page)
            
            try:
                target_update = [update for update in updates_data if update['id'] == self.id][0]
                return [en.Asset(creds=self.__creds, **asset_data) for asset_data in target_update['assets']]
            except KeyError:
                if len(target_update) == 0:
                    page += 1
                    record_count = len(updates_data)
                    continue
        return []   


    def delete(self, *args):
        """Delete the selected update.

        __________
        Parameters

            args : `tuple`
                The list of update fields to return.

        _______
        Returns

            update : `moncli.entities.Update`
                The deleted update.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The update's assets/files.
            body: `str`
                The update's html formatted body.
            created_at: `str`
                The update's creation date.
            creator : `moncli.entities.user.User`
                The update's creator
            creator_id : `str`
                The unique identifier of the update creator.
            id : `str`
                The update's unique identifier.
            item_id : `str`
                The update's item ID.
            replies : `list[moncli.entities.reply.Reply]
                The update's replies.
            text_body : `str`
                The update's text body.
            updated_at : `str`
                The update's last edit date.
        """

        update_data = client.delete_update(
            self.__creds.api_key_v2,
            self.id,
            *args)
        return Update(creds=self.__creds, **update_data)


class _Reply(Model):
    """Reply base model"""
    id = types.StringType(required=True)
    creator_id = types.StringType(required=True)
    body = types.StringType()
    created_at = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()


class Reply(_Reply):
    """A reply for an update
    
    __________
    Properties

        body : `str`
            The reply's html formatted body.
        created_at : `str`
            The reply's creation date.
        creator : `moncli.entities.User`
            The reply's creator.
        creator_id : `str`
            The unique identifier of the reply creator.
        id : `str`
            The reply's unique identifier.
        text_body : `str`
            The reply's text body.
        updated_at : `str`
            The reply's last edit date.

    _______
    Methods

        get_creator : `moncli.entities.User`
            Get the reply's creator.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__item_id = kwargs.pop('item_id')
        self.__creator = None
        super(Reply, self).__init__(kwargs)

    def __repr__(self):
        return str(self.to_primitive())

    @property
    def creator(self):
        """The reply's creator."""
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator
    
    def get_creator(self, *args):
        """Get the reply's creator.

        __________
        Parameters

            args : `tuple`
                List of user return fields.

        _______
        Returns
        
            creator : `moncli.entities.User`
                The creator of this update.

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

        args = client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS)
        user_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.creator_id)])[0]
        return en.User(creds=self.__creds, **user_data)
