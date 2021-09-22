from schematics.models import Model
from schematics.types import StringType
from .. import api, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType



class _Item(Model):
    """Item Base Model"""

    id = StringType(required=True)
    name = StringType()
    created_at = StringType()
    creator_id = StringType()
    state = StringType()
    updated_at = StringType()


class Item(_Item):
    """An item (table row)
    
        Properties

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
            parent_item: moncli.entities.Item
                The relevant parent item for the subitem.
            state : `str`
                The board's state (all / active / archived / deleted)
            subscriber : `moncli.entities.User`
                The pulse's subscribers.
            updated_at : `str`
                The item's last update date.
            updates : `moncli.entities.Update`
                The item's updates.

        Methods

            add_file : `moncli.entities.Asset`
                Add a file to a column value.
            get_files : `list[moncli.entities.Asset]`
                Retrieves the file assets for the login user's account.
            remove_files : `moncli.entities.Item`
                Removes files from a column value.
            get_board : `moncli.entities.Board`
                Get the board that contains this item.
            get_group : `moncli.entities.Group`
                Get the group containing this item.
            get_creator : `moncli.entities.User`
                Get the item's creator.
            get_column_values : `list[moncli.entities.ColumnValue]`
                Get the item's column values.
            get_column_value : `moncli.entities.ColumnValue`
                Get an item's column value by ID or title.
            get_parent_item: `moncli.entities.Item`
                Get Parent Item of a Subitem.
            change_item_name: `moncli.entities.Item`
                change an Item's column name
            change_column_value : `moncli.entities.Item`
                Change an item's column value.
            change_simple_column_value: `moncli.entities.Item`
                Change an item's column value using simple values.
            change_multiple_column_values : `moncli.entities.Item`
                Change the item's column values.
            change_name: `moncli.entities.Item`
                Change the name of an item.
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
        self.__assets = kwargs.pop('__assets', None)
        self.__board = kwargs.pop('__board', None)
        self.__group = kwargs.pop('__group', None)
        self.__creator = kwargs.pop('__creator', None)
        self.__column_values = en.BaseColumnCollection()
        self.__updates = kwargs.pop('__updates', None)
        self. __parent_item = kwargs.pop(' __parent_item',None)

        assets = kwargs.pop('assets', None)
        board = kwargs.pop('board', None)
        group = kwargs.pop('group', None)
        creator = kwargs.pop('creator', None)
        column_values = kwargs.pop('column_values', None)
        updates = kwargs.pop('updates', None)
        parent_item = kwargs.pop(' __parent_item',None)

        super(Item, self).__init__(kwargs)

        if assets != None and not self.__assets:
            self.__assets = [en.Asset(creds=self.__creds, **asset) for asset in assets]
        if board and not self.__board:
            self.__board = en.Board(creds=self.__creds, **board)
        if group and not self.__group:
            self.__group = en.Group(creds=self.__creds, board_id=self.board.id, **group)
        if creator and not self.__creator:
            self.__creator = en.User(creds=self.__creds, **creator)
        if column_values != None and len(self.__column_values) == 0:
            #Column values are a process around here...
            columns_map = { column.id: column for column in self.board.columns }
            for data in column_values:
                column = columns_map[data['id']]
                self.__column_values.append(en.create_column_value(column.column_type, settings_str=column.settings_str, **data))
        if updates != None and not self.__updates:
            self.__updates = [en.Update(creds=self.__creds, **update_data) for update_data in updates]
        if parent_item and not self.__parent_item: 
            self.__parent_item = en.Item(creds=self.__creds, **parent_item)

    def __repr__(self):
        o = self.to_primitive()
        if self.__assets:
            o['assets'] = self.__assets.to_primitive()
        if self.__board:
            o['board'] = self.__board.to_primitive()
        if self.__creator:
            o['creator'] = self.__creator.to_primitive()
        if self.__column_values:
            o['column_values'] = []
            for value in self.__column_values:
                o['column_values'].append(value.to_primitive())
        if self.__updates:
            o['updates'] = [value.to_primitive() for value in self.__updates]
        if self.__parent_item:
            o['parent_item'] = self.__parent_item.to_primitive
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
    def group(self):
        """The group that contains this item."""
        if not self.__group:
            self.__group = self.get_group()
        return self.__group

    @property
    def creator(self):
        """The item's creator."""
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator

    @property
    def column_values(self):
        """The item's column_values."""
        if len(self.__column_values) == 0:
            self.__column_values = self.get_column_values()
        return self.__column_values

    @property
    def updates(self):
        """The item's updates."""
        if self.__updates == None: 
            self.__updates = self.get_updates()
        return self.__updates
    
    @property
    def parent_item(self):
        """The parent item ."""
        if self.__parent_item == None: 
            self.__parent_item = self.get_parent_item()
        return self.__parent_item


    def add_file(self, file_column: en.FileValue, file_path: str, *args):
        """Add a file to a column value.

            Parameters

                file_column : moncli.entities.FileValue
                    The file column value to be updated.
                file_path : `str`
                    The file path.
                args : `tuple`
                    Optional file return fields.

            Returns

                assets : `moncli.entities.Asset`
                    The newly created file asset.

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

        asset_data = api.add_file_to_column(
            self.id,
            file_column.id,
            file_path,
            *args,
            api_key=self.__creds.api_key_v2)
        return en.Asset(**asset_data)


    def get_files(self, column_ids: list = None, *args):
        """Retrieves the file assets for the login user's account.

            Parameters

                args : `str`
                    The list asset return fields.
                kwargs : `dict`
                    Optional keyword arguments for retrieving file assets from an item.
                
            Returns

                assets : `list[moncli.entities.asset.Asset]`
                    A list of file assets uploaded to the account.

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

            Optional Arguments

                column_ids : `list[str]`
                    A list of column IDs from which to retrieve file assets.     
        """
        
        kwargs = {'ids': [int(self.id)]}
        if column_ids:
            kwargs['assets'] = {'column_ids': column_ids}
        assets_data = api.get_items(
            *api.get_field_list(api.DEFAULT_ASSET_QUERY_FIELDS, 'assets', *args),
            api_key=self.__creds.api_key_v2,
            **kwargs)[0]['assets']
        return [en.Asset(**asset_data) for asset_data in assets_data]


    def remove_files(self, file_column: en.FileValue, *args):
        """Add a file to a column value.

            Parameters

                file_column : moncli.entities.FileValue
                    The file column value to be updated.
                args : `tuple`
                    Optional file return fields.

            Returns

                assets : `moncli.entities.Asset`
                    The deleted file asset.

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

        item_data = api.change_column_value(
            self.id,
            file_column.id,
            self.__board.id,
            file_column.format(),
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)


    def get_board(self, *args):
        """Get the board that contains this item.

            Parameters

                args : `tuple`
                    Optional board return fields.

            Returns

                board : `moncli.entities.Board`
                    The board containing this item.

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

        board_data = api.get_items(
            *api.get_field_list(api.DEFAULT_BOARD_QUERY_FIELDS, 'board', *args),
            api_key=self.__creds.api_key_v2,
            ids=[int(self.id)])[0]['board']
        return en.Board(creds=self.__creds, **board_data)


    def get_group(self, *args):
        """Get the group that contains this item.

            Parameters

                args : `tuple`
                    Optional board return fields.

            Returns

                group : `moncli.entities.Group`
                    The group containing this item.


            Return Fields

                archived : `bool`
                    Is the group archived or not.
                color : `str`
                    The group's color.
                deleted : `bool`
                    Is the group deleted or not.
                id : `str`
                    The group's unique identifier.
                items : `list[moncli.entities.Item]`
                    The items in the group.
                position : `str`
                    The group's position in the board.
                title : `str`
                    The group's title.
        """

        group_data = api.get_items(
            *api.get_field_list(api.DEFAULT_GROUP_QUERY_FIELDS, 'group', *args),
            api_key=self.__creds.api_key_v2,
            ids=[int(self.id)])[0]['group']
        return en.Group(creds=self.__creds, __board=self, **group_data)


    def get_creator(self, *args):
        """Get the item's creator.

            Parameters

                args : `tuple`
                    The list of user return fields.

            Returns

                user : `moncli.entities.User`
                    The item's creator.

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
                is_admin: `bool`
                    Is the user a admin or not.
                is_guest : `bool`
                    Is the user a guest or not.
                is_pending : `bool`
                    Is the user a pending user.
                is_verified: `bool`
                    Is the user is verified
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

        user_data = api.get_items(
            *api.get_field_list(api.DEFAULT_USER_QUERY_FIELDS, 'creator', *args),
            api_key=self.__creds.api_key_v2,
            ids=[int(self.id)])[0]['creator']
        return en.User(creds=self.__creds, **user_data)
   

    def get_column_values(self, *args):
        """Get the item's column values.

            Parameters

                args : `tuple`
                    Optional column value return fields.

            Returns

                column_value : `list[moncli.entities.ColumnValue]`
                    The item's column values.

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
        column_values_data = api.get_items(
            *api.get_field_list(api.DEFAULT_COLUMN_VALUE_QUERY_FIELDS, 'column_values', *args),
            api_key=self.__creds.api_key_v2,
            ids=[int(self.id)])[0]['column_values']

        values = []
        for data in column_values_data:
            id = data['id']
            column = columns_map[id]
            column_type = column.column_type
            data['settings_str'] = column.settings_str
            values.append(en.create_column_value(column_type, **data))
        return en.BaseColumnCollection(values)


    def get_column_value(self, id = None, title = None, *args):
        """Get an item's column value by ID or title.

            Parameters

                id : `str`
                    The column's unique identifier.
                    NOTE: This parameter is mutually exclusive and cannot be used with 'title'.
                title : `str`
                    The column's title.
                    NOTE: This parameter is mutually exclusive and cannot be used with 'id'.
                args : `tuple`
                    Optional column value return fields.

            Returns

                column_value : `moncli.entities.ColumnValue`
                    The item's column value.

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
            return self.column_values[title]

        return self.column_values[id]


    def change_name(self, new_name: str):
        """Change the name of an item.

            Parameters

                nem_name : 'str'
                    The new name of the item.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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
        if new_name == None:
            raise InvalidParameterError()
        item_name = {'name':new_name}

        item_data = api.change_multiple_column_value(
            self.id,
            self.board.id,
            item_name,
            api_key=self.__creds.api_key_v2)


        return en.Item(creds=self.__creds, **item_data)

    def change_column_value(self, column_value = None, get_column_values: bool = None, *args):
        """Get an item's column value by ID or title.

            Parameters

                column_value : `moncli.entities.ColumnValue`
                    The column value to update.
                get_column_values: `bool`:
                    Retrieves item column values if set to `True`.
                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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

        if get_column_values:
            args = list(args)
            for arg in ['column_values.{}'.format(arg) for arg in api.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]:
                if arg not in args:
                    args.append(arg)
            args.extend(['id', 'name'])

        if column_value is None:
            raise ColumnValueRequired()
        if not isinstance(column_value, en.ColumnValue):
            raise en.board.InvalidColumnValue(type(column_value).__name__)
        else:
            column_id = column_value.id
            value = column_value.format()

        item_data = api.change_column_value(
            self.id,
            column_id,
            self.board.id,
            value,
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)
    

    def change_simple_column_value(self, id = None, title = None, value = None, *args):
        """Change the item's column values using simple values.

            Parameters

                id: str
                    The id value of the column 
                title: str 
                    The title of the column
                value: `str`
                    The value to be changed
                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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
        
        if not id and not title :
            raise NotEnoughChangeSimpleColumnValueParameters()
        if id and title :
            raise TooManyChangeSimpleColumnValueParameters()
                
        if id:
            column_value = self.column_values[id]   
        elif title:
            column_value = self.column_values[title]
        
        item_data = api.change_simple_column_value(
            self.id,
            self.board.id,
            column_value.id,
            value,
            *args,
            api_key=self.__creds.api_key_v2)        

        return Item(creds=self.__creds, **item_data)

    def change_multiple_column_values(self, column_values, get_column_values: bool = False, *args):
        """Change the item's column values.

            Parameters

                column_values : `list[moncli.entities.ColumnValue] / dict`
                    The column value to update. 
                    NOTE: This value can either be a list of moncli.entities.ColumnValue objects or a formatted dictionary.
                get_column_values: `bool`:
                    Retrieves item column values if set to `True`.
                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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

        if get_column_values:
            args = list(args)
            for arg in ['column_values.{}'.format(arg) for arg in api.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]:
                if arg not in args:
                    args.append(arg)
            args.extend(['id', 'name'])

        if type(column_values) == dict:
            values = column_values
        elif type(column_values) == list:
            values = { value.id: value.format() for value in column_values }
        else:
            raise en.InvalidColumnValue(type(column_values).__name__)
        item_data = api.change_multiple_column_value(
            self.id,
            self.board.id,
            values,
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)


    def create_subitem(self, item_name: str, *args, **kwargs):
        """Create subitem.

            Parameters
            
                item_name : `str`
                    The new item's name.
                args : `tuple`
                    The list of item return fields.
                kwargs : `dict`
                    Optional arguments for creating subitems.

            Returns
                        
                subitem : `moncli.entities.Item`
                    The created subitem.

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
            
            Optional Arguments
            
                column_values : `json`
                    The column values of the new item.
        """
        
        subitem_data = api.create_subitem(
            self.id,
            item_name,
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)
        return Item(creds=self.__creds, **subitem_data)


    def move_to_group(self, group_id: str, get_column_values = False, *args):
        """Move item to a different group.

            Parameters

                group_id : `str`
                    The group's unique identifier.
                get_column_values: `bool`:
                    Retrieves item column values if set to `True`.
                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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

        if get_column_values:
            args = list(args)
            for arg in ['column_values.{}'.format(arg) for arg in api.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]:
                if arg not in args:
                    args.append(arg)
            args.extend(['id', 'name'])

        item_data = api.move_item_to_group(
            self.id,
            group_id,
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)


    def archive(self, *args):
        """Archive this item.

            Parameters

                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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

        item_data = api.archive_item(
            self.id,
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)


    def delete(self, *args):
        """Delete this item.

            Parameters

                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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

        item_data = api.delete_item(
            self.id,
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)


    def duplicate(self, *args, **kwargs):
        """Duplicate this item.

            Parameters

                args : `tuple`
                    The list of item return fields.
                kwargs : `dict`
                    Optional keyword arguments for duplicating item.

            Returns
                
                item : `moncli.entities.Item`
                    The duplicated item.

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
            
            Optional Arguments

                with_updates : `bool`
                    Duplicate with the item's updates.
        """

        item_data = api.duplicate_item(
            self.board.id,
            self.id,
            *args,
            api_key=self.__creds.api_key_v2,
            *kwargs)
        return Item(creds=self.__creds, **item_data)


    def add_update(self, body: str, *args, **kwargs):
        """Change the item's column values.

            Parameters

                body : `str`
                    The update text.
                args : `tuple`
                    Optional update return fields.
                kwargs : `dict`
                    Optional keyword arguments for adding an update.

            Returns

                update : `moncli.entities.Update`
                    The created update.

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

            Optional Arguments

                parent_id : `str`
                    The parent post identifier.
        """

        update_data = api.create_update(
            body, 
            self.id,
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return en.Update(creds=self.__creds, **update_data)


    def get_updates(self, *args, **kwargs):
        """Get updates for this item.
 
            Parameters
    
                args : `tuple`
                    Optional update return fields.
                kwargs : `dict`
                    Optional keyword arguments for getting item updates.

            Returns

                update : `list[moncli.entities.Update]`
                    The item's updates.

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
                replies : `list[moncli.entities.Reply]`
                    The update's replies.
                text_body : `str`
                    The update's text body.
                updated_at : `str`
                    The update's last edit date.

            Optional Arguments

                limit : `int`
                    Number of updates to get; the default is 25.
                page : `int`
                    Page number to get, starting at 1.
        """
        
        limit = kwargs.pop('limit', 25)
        page = kwargs.pop('page', 1)
        updates_data = api.get_items(
            *api.get_field_list(api.DEFAULT_UPDATE_QUERY_FIELDS, 'updates', *args),
            api_key=self.__creds.api_key_v2,
            ids=[int(self.id)],
            limit=1,
            updates={'limit': limit, 'page': page})[0]['updates']
        return [en.Update(creds=self.__creds, **update_data) for update_data in updates_data]


    def delete_update(self, update_id: str, *args):
        """Delete an item's update

            Parameters

                update_id : `str`
                    The update's unique identifier
                args : `tuple`
                    The list of optional fields to return.

            Returns

                update : `moncli.entities.Update`
                    The item's deleted update.

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

            Parameters

                args : `tuple`
                    The list of optional fields to return.

            Returns

                item : `moncli.entities.Item`
                    The updated item.

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

        item_data = api.clear_item_updates(
            self.id,
            *args,
            api_key=self.__creds.api_key_v2)
        return Item(creds=self.__creds, **item_data)

    
    def get_activity_logs(self, *args, **kwargs):
        """Retrieves an item's activity logs.

            Parameters
            
                args : `tuple`
                    The list of activity log return fields.
                kwargs : `dict`
                    Optional keyword arguments for retrieving activity logs.

            Returns

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board's activity logs.

            Return Fields

                account_id : `str`
                    The unique identifier of the user's account.
                created_at : `str`
                    The create date
                data : `str`
                    The item's column values in string form.
                entity : `str`
                    The activity log's entity.
                event : `str`
                    The activity log's event.
                id : `str`
                    The activity log's unique identifier.
                user_id : `str`
                    The user's unique identifier.

            Optional Arguments

                limit : `int`
                    Number of items to get, the default is 25.
                page : `int`
                    Page number to get, starting at 1.
                user_ids : `list[str]`
                    User ids to filter.
                column_ids : `list[str]`
                    Column ids to filter.
                group_ids : `list[str]`
                    Group ids to filter.
                from : `str`
                    From timespamp (ISO8601).
                to : `str`
                    To timespamp (ISO8601).
        """

        
        kwargs['item_ids'] = [int(self.id)]
        return self.board.get_activity_logs(*args, **kwargs)

    def get_parent_item(self, *args, **kwargs):
        """Get Parent Item of a Subitem.

            Parameters

                args : `tuple`
                    Optional item return fields.

            Returns

                item : `moncli.entities.Item`
                    The parent item.

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
        item_data =  api.get_items(
            *api.get_field_list(api.DEFAULT_ITEM_QUERY_FIELDS, 'parent_item', *args),
            ids=[self.id]
        )[0]['parent_item']
        return Item(creds=self.__creds, **item_data)

class ColumnValueRequired(Exception):
    def __init__(self):
        self.message = "A column value is required if no 'column_id' value is present."

class UpdateNotFound(Exception):
    def __init__(self, update_id: str):
        self.message = "Item does not contain update with ID '{}'.".format(update_id)

class TooManyChangeSimpleColumnValueParameters(Exception):
    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when changing a simple column value"

class NotEnoughChangeSimpleColumnValueParameters(Exception):
    def __init__(self):
        self.message = "Either 'id' or 'title' is required when changing a simple column value"

class InvalidParameterError(Exception):
    def __init__(self):
        self.message = "New name must be present"