import json
from typing import List

from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, entities as en, enums
from ..api_v2 import constants
from .column_value import FileValue


class _Item(Model):
    """Item Base Model"""

    id = types.StringType(required=True)
    name = types.StringType()
    created_at = types.StringType()
    creator_id = types.StringType()
    state = types.StringType()
    updated_at = types.StringType()


class Item(_Item):
    """An item (table row)
    
    __________
    Properties
    __________
    assets : `list[moncli.entities.Asset]`
        The item's assets/files.
    board : `moncli.entities.Board`
        The board that contains this item.
    column_values : `list[moncli.entities.ColumnValue]`
        The item's column values.
    created_at : `str`
        The item's create date.
    creator : `moncli.entities.User`
        The item's creator.
    creator_id : `str`
        The item's unique identifier.
    group : `moncli.entities.Group`
        The group that contains this item.
    id : `str`
        The item's unique identifier.
    name : `str`
        The item's name.
    state : `str`
        The board's state (all / active / archived / deleted)
    subscriber : `moncli.entities.User`
        The pulse's subscribers.
    updated_at : `str`
        The item's last update date.
    updates : `moncli.entities.Update`
        The item's updates.

    _______
    Methods
    _______
    add_file : `moncli.entities.Asset`
        Add a file to a column value.
    get_files : `list[moncli.entities.Asset]`
        Retrieves the file assets for the login user's account.
    remove_files : `moncli.entities.Item`
        Removes files from a column value.
    get_board : `moncli.entities.Board`
        Get the board that contains this item.
    get_creator : `moncli.entities.User`
        Get the item's creator.
    get_column_values : `list[moncli.entities.ColumnValue]`
        Get the item's column values.
    get_column_value : `moncli.entities.ColumnValue`
        Get an item's column value by ID or title.
    change_column_value : `moncli.entities.Item`
        Change an item's column value.
    change_multiple_column_values : `moncli.entities.Item`
        Change the item's column values.
    create_subitem : `moncli.entities.Item`
        Create subitem.
    move_to_group : `moncli.entities.Item`
        Move item to a different group.
    archive : `moncli.entities.Item`
        Archive this item.
    delete : `moncli.entities.Item`
        Delete this item.
    duplicate : `moncli.entities.Item`
        Duplicate this item.
    add_update : `moncli.entities.Update`
        Create a new update for this item.
    get_updates : `list[moncli.entities.Update]`
        Get updates for this item.
    delete_update : `moncli.entities.Update`
        Delete item update.
    clear_updates : `moncli.entities.Item`
        Clear all updates for item.
    
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__assets = None
        self.__board = None
        self.__creator = None
        self.__column_values = None
        self.__updates = None
        assets = kwargs.pop('assets', None)
        if assets != None:
            self.__assets = [en.Asset(creds=self.__creds, **asset) for asset in assets]
        board = kwargs.pop('board', None)
        if board:
            self.__board = en.Board(creds=self.__creds, **board)
        creator = kwargs.pop('creator', None)
        if creator:
            self.__creator = en.User(creds=self.__creds, **creator)
        column_values = kwargs.pop('column_values', None)
        if column_values != None:
            columns_map = { column.id: column for column in self.board.columns }
            self.__column_values = [en.create_column_value(columns_map[data['id']].column_type, **data) for data in column_values]
        updates = kwargs.pop('updates', None)
        if updates != None:
            self.__updates = [en.Update(creds=self.__creds, **update_data) for update_data in updates]
        super(Item, self).__init__(kwargs)

    def __repr__(self):
        o = self.to_primitive()
        if self.__assets:
            o['assets'] = self.__assets.to_primitive()
        if self.__board:
            o['board'] = self.__board.to_primitive()
        if self.__creator:
            o['creator'] = self.__creator.to_primitive()
        if self.__column_values:
            o['column_values'] = [value.to_primitive() for value in self.__column_values]
        if self.__updates:
            o['updates'] = [value.to_primitive() for value in self.__updates]
        return str(o)

    @property
    def assets(self):
        """The item's assets/files."""
        if self.__assets == None:
            self.__assets = self.get_files()
        return self.__assets

    @property
    def board(self):
        """The board that contains this item."""
        if not self.__board:
            self.__board = self.get_board()
        return self.__board

    @property
    def creator(self):
        """The item's creator."""
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator

    @property
    def column_values(self):
        """The item's column_values."""
        if self.__column_values == None:
            self.__column_values = self.get_column_values()
        return self.__column_values

    @property
    def updates(self):
        """The item's updates."""
        if self.__updates == None: 
            self.__updates = self.get_updates()
        return self.__updates


    def add_file(self, file_column: FileValue, file_path: str, *args):
        """Add a file to a column value.

        __________
        Parameters

            file_column : moncli.entities.FileValue
                The file column value to be updated.
            file_path : `str`
                The file path.
            args : `tuple`
                Optional file return fields.

        _______
        Returns

            assets : `moncli.entities.Asset`
                The newly created file asset.

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

        asset_data = client.add_file_to_column(
            self.__creds.api_key_v2,
            self.id,
            file_column.id,
            file_path,
            *args)
        return en.Asset(**asset_data)


    def get_files(self, column_ids: list = None, *args):
        """Retrieves the file assets for the login user's account.

        __________
        Parameters

            args : `str`
                The list asset return fields.
            kwargs : `dict`
                Optional keyword arguments for retrieving file assets from an item.
            
        _______
        Returns

            assets : `list[moncli.entities.asset.Asset]`
                A list of file assets uploaded to the account.

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

        __________________
        Optional Arguments

            column_ids : `list[str]`
                A list of column IDs from which to retrieve file assets.     
        """
        
        args = client.get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS, *args)
        args = ['assets.' + arg for arg in args]
        kwargs = {'ids': [int(self.id)]}
        if column_ids:
            kwargs['assets'] = {'column_ids': column_ids}
        assets_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            **kwargs)[0]['assets']
        return [en.Asset(**asset_data) for asset_data in assets_data]


    def remove_files(self, file_column: FileValue, *args):
        """Add a file to a column value.

        __________
        Parameters

            file_column : moncli.entities.FileValue
                The file column value to be updated.
            args : `tuple`
                Optional file return fields.

        _______
        Returns

            assets : `moncli.entities.Asset`
                The deleted file asset.

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

        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            file_column.id,
            self.__board.id,
            file_column.format(),
            *args)
        return Item(creds=self.__creds, **item_data)


    def get_board(self, *args):
        """Get the board that contains this item.

        __________
        Parameters

            args : `tuple`
                Optional board return fields.

        _______
        Returns

            boards : `moncli.entities.Board`
                The board containing this item.

        _____________
        Return Fields

            activity_logs : `list[moncli.entities.object.ActivityLog]`
                The board log events.
            board_folder_id : `int`
                The board's folder unique identifier.
            board_kind : `str`
                The board's kind (public / private / share).
            columns : `list[moncli.entities.object.Column]`
                The board's visible columns.
            communication : `str`
                Get the board communication value - typically meeting ID.
            description : `str`
                The board's description.
            groups : `list[moncli.entities.group.Group]`
                The board's visible groups.
            id : `str`
                The unique identifier of the board.
            items : `list[moncli.entities.item.Item]`
                The board's items (rows).
            name : `str`
                The board's name.
            owner : `moncli.entities.user.User`
                The owner of the board.
            permissions : `str`
                The board's permissions.
            pos : `str`
                The board's position.
            state : `str`
                The board's state (all / active / archived / deleted).
            subscribers : `list[moncli.entities.user.User]`
                The board's subscribers.
            tags : `list[moncli.entities.objects.Tag]`
                The board's specific tags.
            top_group : `moncli.entities.group.Group`
                The top group at this board.
            updated_at : `str`
                The last time the board was updated at (ISO8601 DateTime).
            updates : `list[moncli.entities.update.Update]`
                The board's updates.
            views : `list[moncli.entities.board.BoardView]`
                The board's views.
            workspace : `moncli.entities.objects.Workspace`
                The workspace that contains this board (null for main workspace).
            workspace_id : `str`
                The board's workspace unique identifier (null for main workspace).
        """

        args = client.get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS, *args)
        args = ['board.' + arg for arg in args]
        board_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['board']
        return en.Board(creds=self.__creds, **board_data)


    def get_creator(self, *args):
        """Get the item's creator.

        __________
        Parameters

            args : `tuple`
                The list of user return fields.

        _______
        Returns

            user : `moncli.entities.User`
                The item's creator.

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

        args = ['creator.' + arg for arg in client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS)]
        user_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['creator']
        return en.User(creds=self.__creds, **user_data)
   

    def get_column_values(self, *args):
        """Get the item's column values.

        __________
        Parameters

            args : `tuple`
                Optional column value return fields.

        _______
        Returns

            column_value : `list[moncli.entities.ColumnValue]`
                The item's column values.

        _____________
        Return Fields

            additional_info : `json`
                The column value's additional information.
            id : `str`
                The column's unique identifier.
            text : `str`
                The column's textual value in string form.
            title : `str`
                The column's title.
            type : `str`
                The column's type.
            value : `json`
                The column's value in json format.
        """

        # Pulls the columns from the board containing the item and maps 
        # column ID to type.
        columns_map = { column.id: column for column in self.board.columns }
        args = ['column_values.' + arg for arg in client.get_field_list(constants.DEFAULT_COLUMN_VALUE_QUERY_FIELDS, *args)]
        column_values_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['column_values']

        values = []
        for data in column_values_data:
            id = data['id']
            column_type = columns_map[id].column_type
            if columns_map[id].settings:
                data['settings'] = columns_map[id].settings
            values.append(en.create_column_value(column_type, **data))
        return values


    def get_column_value(self, id = None, title = None, *args):
        """Get an item's column value by ID or title.

        __________
        Parameters

            id : `str`
                The column's unique identifier.
                NOTE: This parameter is mutually exclusive and cannot be used with 'title'.
            title : `str`
                The column's title.
                NOTE: This parameter is mutually exclusive and cannot be used with 'id'.
            args : `tuple`
                Optional column value return fields.

        _______
        Returns

            column_value : `moncli.entities.ColumnValue`
                The item's column value.

        _____________
        Return Fields

            additional_info : `json`
                The column value's additional information.
            id : `str`
                The column's unique identifier.
            text : `str`
                The column's textual value in string form.
            title : `str`
                The column's title.
            type : `str`
                The column's type.
            value : `json`
                The column's value in json format.
        """

        if id and title:
            raise en.board.TooManyGetColumnValueParameters()
        if id is None and title is None:
            raise en.board.NotEnoughGetColumnValueParameters()
        
        if title:
            for column_value in self.get_column_values(*args):
                if title and column_value.title == title:
                    return column_value

        elif id:
            args = ['column_values.' + arg for arg in client.get_field_list(constants.DEFAULT_COLUMN_VALUE_QUERY_FIELDS, *args)]
            column_value_data = client.get_items(
                self.__creds.api_key_v2,
                *args,
                ids=[int(self.id)],
                column_values={'ids': [id]})[0]['column_values'][0]

            columns_map = { column.id: column for column in self.board.columns }
            column_type = columns_map[id].column_type
            if columns_map[id].settings:
                column_value_data['settings'] = columns_map[id].settings
            return en.create_column_value(column_type, **column_value_data)
    

    def change_column_value(self, column_value = None, *args):
        """Get an item's column value by ID or title.

        __________
        Parameters

            column_value : `moncli.entities.ColumnValue`
                The column value to update.
            args : `tuple`
                Optional item return fields.

        _______
        Returns

            item : `moncli.entities.Item`
                The updated item.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The item's assets/files.
            board : `moncli.entities.board.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.column_value.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.user.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.group.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.user.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.update.Update`
                The item's updates.
        """

        if column_value is None:
            raise ColumnValueRequired()
        if not isinstance(column_value, en.ColumnValue):
            raise en.board.InvalidColumnValue(type(column_value).__name__)
        else:
            column_id = column_value.id
            value = column_value.format()

        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            column_id,
            self.board.id,
            value,
            *args)
        return Item(creds=self.__creds, **item_data)
    

    def change_multiple_column_values(self, column_values, *args):
        """Change the item's column values.

        __________
        Parameters

            column_values : `list[moncli.entities.ColumnValue] / dict`
                The column value to update. 
                NOTE: This value can either be a list of moncli.entities.ColumnValue objects or a formatted dictionary.
            args : `tuple`
                Optional item return fields.

        _______
        Returns

            item : `moncli.entities.Item`
                The updated item.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The item's assets/files.
            board : `moncli.entities.board.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.column_value.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.user.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.group.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.user.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.update.Update`
                The item's updates.
        """

        if type(column_values) == dict:
            values = column_values
        elif type(column_values) == list:
            values = { value.id: value.format() for value in column_values }
        else:
            raise en.InvalidColumnValue(type(column_values).__name__)
        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            self.id,
            self.board.id,
            values,
            *args)
        return Item(creds=self.__creds, **item_data)


    def create_subitem(self, item_name: str, *args, **kwargs):
        """Create subitem.

        __________
        Parameters
        
            item_name : `str`
                The new item's name.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for creating subitems.

        _______
        Returns
                    
            subitem : `moncli.entities.Item`
                The created subitem.

        _____________
        Return Fields
        
            assets : `list[moncli.entities.Asset]`
                The item's assets/files.
            board : `moncli.entities.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.Update`
                The item's updates.

        __________________
        Optional Arguments
        
            column_values : `json`
                The column values of the new item.
        """
        
        subitem_data = client.create_subitem(
            self.__creds.api_key_v2,
            self.id,
            item_name,
            *args,
            **kwargs)
        return en.Item(creds=self.__creds, **subitem_data)


    def move_to_group(self, group_id: str, *args):
        """Move item to a different group.

        __________
        Parameters

            group_id : `str`
                The group's unique identifier.
            args : `tuple`
                Optional item return fields.

        _______
        Returns

            item : `moncli.entities.Item`
                The updated item.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The item's assets/files.
            board : `moncli.entities.board.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.column_value.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.user.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.group.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.user.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.update.Update`
                The item's updates.
        """

        item_data = client.move_item_to_group(
            self.__creds.api_key_v2,
            self.id,
            group_id,
            *args)
        return Item(creds=self.__creds, **item_data)


    def archive(self, *args):
        """Archive this item.

        __________
        Parameters

            args : `tuple`
                Optional item return fields.

        _______
        Returns

            item : `moncli.entities.Item`
                The updated item.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The item's assets/files.
            board : `moncli.entities.board.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.column_value.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.user.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.group.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.user.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.update.Update`
                The item's updates.
        """

        item_data = client.archive_item(
            self.__creds.api_key_v2,
            self.id,
            *args)
        return Item(creds=self.__creds, **item_data)


    def delete(self, *args):
        """Delete this item.

        __________
        Parameters

            args : `tuple`
                Optional item return fields.

        _______
        Returns

            item : `moncli.entities.Item`
                The updated item.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The item's assets/files.
            board : `moncli.entities.board.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.column_value.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.user.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.group.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.user.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.update.Update`
                The item's updates.
        """

        item_data = client.delete_item(
            self.__creds.api_key_v2,
            self.id,
            *args)
        return Item(creds=self.__creds, **item_data)


    def duplicate(self, *args, **kwargs):
        """Duplicate this item.

        __________
        Parameters

            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional keyword arguments for duplicating item.

        _______
        Returns
            
            item : `moncli.entities.Item`
                The duplicated item.

        _____________
        Return Fields
        
            assets : `list[moncli.entities.Asset]`
                The item's assets/files.
            board : `moncli.entities.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.Update`
                The item's updates.

        __________________
        Optional Arguments

            with_updates : `bool`
                Duplicate with the item's updates.
        """

        item_data = client.duplicate_item(
            self.__creds.api_key_v2,
            self.board.id,
            self.id,
            *args,
            *kwargs)
        return en.Item(creds=self.__creds, **item_data)


    def add_update(self, body: str, *args, **kwargs):
        """Change the item's column values.

        __________
        Parameters

            body : `str`
                The update text.
            args : `tuple`
                Optional update return fields.
            kwargs : `dict`
                Optional keyword arguments for adding an update.

        _______
        Returns

            update : `moncli.entities.Update`
                The created update.

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
            replies : `list[moncli.reply.Reply]
                The update's replies.
            text_body : `str`
                The update's text body.
            updated_at : `str`
                The update's last edit date.

        __________________
        Optional Arguments

            parent_id : `str`
                The parent post identifier.
        """

        update_data = client.create_update(
            self.__creds.api_key_v2, 
            body, 
            self.id,
            *args,
            **kwargs)
        return en.Update(creds=self.__creds, **update_data)


    def get_updates(self, *args, **kwargs):
        """Get updates for this item.
 
        __________
        Parameters
 
            args : `tuple`
                Optional update return fields.
            kwargs : `dict`
                Optional keyword arguments for getting item updates.

        _______
        Returns

            update : `list[moncli.entities.Update]`
                The item's updates.

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

        __________________
        Optional Arguments

            limit : `int`
                Number of updates to get; the default is 25.
            page : `int`
                Page number to get, starting at 1.
        """
        
        args = ['updates.' + arg for arg in client.get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)]
        limit = kwargs.pop('limit', 25)
        page = kwargs.pop('page', 1)
        updates_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)],
            limit=1,
            updates={'limit': limit, 'page': page})[0]['updates']
        return [en.Update(creds=self.__creds, **update_data) for update_data in updates_data]


    def delete_update(self, update_id: str, *args):
        """Delete an item's update
        __________
        Parameters

            update_id : `str`
                The update's unique identifier
            args : `tuple`
                The list of optional fields to return.

        _______
        Returns

            update : `moncli.entities.Update`
                The item's deleted update.

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

        updates = self.get_updates(*args)
        target_update = [update for update in updates if update.id == update_id]
        if not target_update:
            raise UpdateNotFound(update_id)
        return target_update[0].delete()


    def clear_updates(self, *args):
        """Clear item's updates.

        __________
        Parameters

            args : `tuple`
                The list of optional fields to return.

        _______
        Returns

            item : `moncli.entities.Item`
                The updated item.

        _____________
        Return Fields

            assets : `list[moncli.entities.asset.Asset]`
                The item's assets/files.
            board : `moncli.entities.board.Board`
                The board that contains this item.
            column_values : `list[moncli.entities.column_value.ColumnValue]`
                The item's column values.
            created_at : `str`
                The item's create date.
            creator : `moncli.entities.user.User`
                The item's creator.
            creator_id : `str`
                The item's unique identifier.
            group : `moncli.entities.group.Group`
                The group that contains this item.
            id : `str`
                The item's unique identifier.
            name : `str`
                The item's name.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.user.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.update.Update`
                The item's updates.
        """

        args = client.get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
        item_data = client.clear_item_updates(
            self.__creds.api_key_v2,
            self.id,
            *args)
        return en.Item(creds=self.__creds, **item_data)


class ColumnValueRequired(Exception):
    def __init__(self):
        self.message = "A column value is required if no 'column_id' value is present."

class UpdateNotFound(Exception):
    def __init__(self, update_id: str):
        self.message = "Item does not contain update with ID '{}'.".format(update_id)
