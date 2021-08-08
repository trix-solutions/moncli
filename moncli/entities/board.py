from schematics.models import Model
from schematics.types import StringType, IntType
from .. import api_v2 as client, enums, entities as en
from ..api_v2 import constants
from ..entities import column_value as cv


class _Board(Model):
    """The base data model for a board"""

    id = StringType(required=True)
    name = StringType()
    board_folder_id = IntType()
    board_kind = StringType()
    communication = StringType()
    description = StringType()
    permissions = StringType()
    pos = StringType()
    state = StringType()
    workspace_id = StringType()
    updated_at = StringType()


class Board(_Board):
    """The entity model for a board

        Properties

            activity_logs : `list[moncli.entities.ActivityLog]`
                The board log events.
            board_folder_id : `int`
                The board's folder unique identifier.
            board_kind : `str`
                The board's kind (public / private / share).
            columns : `list[moncli.entities.Column]`
                The board's visible columns.
            communication : `str`
                Get the board communication value - typically meeting ID.
            description : `str`
                The board's description.
            groups : `list[moncli.entities.Group]`
                The board's visible groups.
            id : `str`
                The unique identifier of the board.
            items : `list[moncli.entities.Item]`
                The board's items (rows).
            name : `str`
                The board's name.
            owner : `moncli.entities.User`
                The owner of the board.
            permissions : `str`
                The board's permissions.
            pos : `str`
                The board's position.
            state : `str`
                The board's state (all / active / archived / deleted).
            subscribers : `list[moncli.entities.User]`
                The board's subscribers.
            tags : `list[moncli.entities.objects.Tag]`
                The board's specific tags.
            top_group : `moncli.entities.Group`
                The top group at this board.
            updated_at : `str`
                The last time the board was updated at (ISO8601 DateTime).
            updates : `list[moncli.entities.Update]`
                The board's updates.
            views : `list[moncli.entities.BoardView]`
                The board's views.
            workspace : `moncli.entities.Workspace`
                The workspace that contains this board (null for main workspace).
            workspace_id : `str`
                The board's workspace unique identifier (null for main workspace).

        Methods

            get_activity_logs : `list[moncli.entities.ActivityLog]`
                Get the board log events. 
            get_views : `list[moncli.entities.BoardView]`
                Get the board's views.
            add_subscribers : `list[moncli.entities.User]`
                Add subscribers to this board.
            get_subscribers : `list[monlci.entities.User]`
                Get board subscribers.
            delete_subscribers : `list[monlci.entities.User]`
                Remove subscribers from the board.
            add_column : `moncli.entities.Column`
                Create a new column in board.
            get_columns : `list[moncli.entities.Column]`
                Get the board's visible columns.
            add_group : `moncli.entities.Group`
                Creates a new group in the board.
            get_groups : `list[moncli.entities.Group]`
                Get the board's visible groups.
            get_group : `moncli.entities.Group`
                Get a group belonging to the board by ID or title.
            add_item : `moncli.entities.Item`
                Create a new item in the board.
            get_items : `list[moncli.entities.Item]`
                Get the board's items (rows).
            get_items_by_column_values : `list[moncli.entities.Item]`
                Search items in this board by their column values.
            get_column_value : `moncli.entities.ColumnValue`
                Create a column value from a board's column.
            create_webhook : `moncli.entities.Webhook`
                Create a new webhook.
            delete_webhook : `moncli.entities.Webhook`
                Delete a new webhook.
            get_workspace : `moncli.entities.Workspace`
                Get the board's workspace that contains this board (null for main workspace).
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds', None)
        self.__activity_logs = kwargs.pop('__activity_logs', None)
        self.__columns = kwargs.pop('__columns', None)
        self.__groups = kwargs.pop('__groups', None)
        self.__items = kwargs.pop('__items', None)
        self.__subscribers = kwargs.pop('__subscribers', None)
        self.__views = kwargs.pop('__views', None)
        self.__tags = kwargs.pop('__tags', None)
        self.__updates = kwargs.pop('_updates', None)
        self.__workspace = kwargs.pop('__workspace', None)

        activity_logs = kwargs.pop('activity_logs', None)
        columns = kwargs.pop('columns', None)
        groups = kwargs.pop('groups', None)
        items = kwargs.pop('items', None)
        subscribers = kwargs.pop('subscribers', None)
        tags = kwargs.pop('tags', None)
        updates = kwargs.pop('updates', None)
        views = kwargs.pop('views', None)
        workspace = kwargs.pop('workspace', None)

        super(Board, self).__init__(kwargs)
        
        if activity_logs and not self.__activity_logs:
            self.__activity_logs = [en.ActivityLog(log) for log in activity_logs]
        if columns and not self.__columns:
            self.__columns = [en.Column(column) for column in columns]
        if groups and not self.__groups:
            self.__groups = [en.Group(creds=self.__creds, **groups) for group in groups]
        if items and not self.__items:
            self.__items = [en.Item(creds=self.__creds, __board=self, **item) for item in items]
        if subscribers and not self.__subscribers:
            self.__items = [en.User(creds=self.__creds, **subscriber) for subscriber in subscribers]
        if tags and not self.__tags:
            self.__tags = [en.Tag(tag) for tag in tags]
        if views and not self.__views:
            self.__views = [en.BoardView(view) for view in views]
        if updates and not self.__updates:
            self.__updates = [en.Update(update) for update in updates]
        if workspace and not self.__workspace:
            self.__workspace = en.Workspace(workspace)
        

    def to_primitive(self, role=None, app_data=None, **kwargs):
        o = super().to_primitive(role, app_data, **kwargs)
        if self.__activity_logs != None:
            o['activity_logs'] = [log.to_primitive() for log in self.__activity_logs]
        if self.__columns:
            o['columns'] = [column.to_primitive() for column in self.__columns]
        if self.__groups:
            o['groups'] = [group.to_primitive() for group in self.__groups]
        if self.__items:
            o['items'] = [item.to_primitive() for item in self.__items]
        if self.__items:
            o['subscribers'] = [item.to_primitive() for item in self.__subscribers]
        if self.__tags:
            o['tags'] = [item.to_primitive() for item in self.__tags]
        if self.__updates:
            o['updates'] = [item.to_primitive() for item in self.__updates]
        if self.__items:
            o['views'] = [item.to_primitive() for item in self.__views]
        return o

    def __repr__(self):
        return str(self.to_primitive())
 
    @property
    def activity_logs(self):
        """The board log events"""

        if self.__activity_logs == None:
            self.__activity_logs = self.get_activity_logs()
        return self.__activity_logs

    @property
    def columns(self):
        """Retrieve board columns"""

        if not self.__columns:
            self.__columns = self.get_columns()
        return self.__columns

    @property
    def groups(self):
        """Retrieve board groups"""
        
        if not self.__groups:
            self.__groups = self.get_groups()
        return self.__groups

    @property
    def items(self):
        """Retrieve board items"""

        if not self.__items:
            self.__items = self.get_items()
        return self.__items

    @property
    def subscribers(self):
        """Retrieve board subscribing users"""

        if not self.__subscribers:
            self.__subscribers = self.get_subscribers()
        return self.__subscribers

    @property
    def tags(self):
        """Retrieve board tags."""
        if self.__tags == None: 
            self.__tags = self.get_tags()
        return self.__tags

    @property
    def updates(self):
        """Retrieve board updates."""
        if self.__updates == None: 
            self.__updates = self.get_updates()
        return self.__updates

    @property
    def views(self):
        """Retrieve board updates."""
        if self.__views == None:
            self.__views = self.get_views()
        return self.__views

    @property
    def workspace(self):
        """Retrieve workspace"""

        if not self.__workspace:
            self.__workspace = self.get_workspace()
        return self.__workspace


    def get_activity_logs(self, *args, **kwargs):
        """Get board log events.
        
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
                item_ids : `list[str]`
                    Item id to filter
                from : `str`
                    From timespamp (ISO8601).
                to : `str`
                    To timespamp (ISO8601).
        """

        args = ['activity_logs.{}'.format(arg) for arg in client.get_field_list(constants.DEFAULT_ACTIVITY_LOG_QUERY_FIELDS, *args)]
        if kwargs:
            kwargs = {'activity_logs': kwargs}

        activity_logs_data = client.get_boards(
            self.__creds.api_key_v2,
            'id', 'name',
            *args,
            ids=[self.id],
            **kwargs)[0]['activity_logs']

        return [en.ActivityLog(activity_log) for activity_log in activity_logs_data]


    def get_views(self, *args, **kwargs):
        """Get the board's views.

            Parameters

                args : `tuple`
                    The list of board view return fields.
                kwargs : `dict`
                    Optional keyword arguments for querying board views.

            Returns

                views : `list[moncli.entities.BoardView]`
                    The board's collection of board views.

            Return Fields

                id : `str`
                    The view's unique identifier.
                name : `str`
                    The view's name.
                settings_str : `str`
                    The view's settings in a string from.
                type : `str`
                    The view's type.

            Optional Arguments

                ids : `str`
                    The list of view unique identifiers.
                type :  `str`
                    The view's type.
        """

        args = ['views.{}'.format(arg) for arg in client.get_field_list(constants.DEFAULT_BOARD_VIEW_QUERY_FIELDS)]
        if kwargs:
            kwargs = {'views': kwargs}

        views_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[self.id],
            **kwargs)[0]['views']

        return [en.BoardView(view) for view in views_data]


    def add_subscribers(self, user_ids: list, *args, **kwargs):
        """Add subscribers to this board.

            Parameters

                user_ids : `list[str]`
                    User ids to subscribe to a board.
                args : `tuple`
                    List of user return fields.
                kwargs : `dict`
                    Additional keyword arguments for adding subscribers to board.
            
            Returns

                user : `list[moncli.entity.User]`
                    The users subscribed to this board.
            
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

            Optional Arguments

                kind : `moncli.enums.SubscriberKind`
                    Subscribers kind (subscriber / owner).
        """

        subscribers_data = client.add_subscribers_to_board(
            self.__creds.api_key_v2,
            self.id,
            user_ids,
            *args,
            **kwargs)

        return [en.User(creds=self.__creds, **user) for user in subscribers_data]

    
    def get_subscribers(self, *args):
        """Get board subscribers

            Parameters

                args : `tuple`
                    The list of user return fields.
                
            Returns

                subscribers : `list[moncli.entity.User]`
                    The board subscribers.

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

        args = ['subscribers.{}'.format(arg) for arg in client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS, *args)]
        kwargs = {
            'ids': [self.id]
        }

        users_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            **kwargs)[0]['subscribers']

        return [en.User(creds=self.__creds, **user) for user in users_data]


    def delete_subscribers(self, user_ids: list, *args):
        """Remove subscribers from the board.

            Parameters

                user_ids : `list[str]`
                    User ids to unsubscribe from board.
                args : `tuple`
                    The list of user return fields.

            Returns

                subscribers : `list[moncli.entities.User]`
                    The users unsubscribed from the board.
            
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
        
        users_data = client.delete_subscribers_from_board(
            self.__creds.api_key_v2,
            self.id,
            user_ids,
            *args)

        return [en.User(creds=self.__creds, **user) for user in users_data]


    def add_column(self, title: str, column_type: enums.ColumnType, *args, **kwargs):
        """Create a new column in board.
    
            Parameters

                title : `str`
                    The new column's title.
                column_type : `moncli.enums.ColumnType`
                    The type of column to create.
                args : `tuple`
                    The list of column return fields.
                kwargs : `dict`
                    The optional keywork arguments.

            Returns

                column : `moncli.entities.Column`
                    The created column.

            Return Fields

                archived : `bool`
                    Is the column archived or not.
                id : `str`
                    The column's unique identifier.
                pos : `str`
                    The column's position in the board.
                settings_str : `str`
                    The column's settings in a string form.
                title : `str`
                    The column's title.
                type : `str`
                    The column's type.
                width : `int`
                    The column's width.

            Optional Arguments

                defaults : `json`
                    The new column's defaults.
        """

        column_data = client.create_column(
            self.__creds.api_key_v2, 
            self.id, 
            title, 
            column_type, 
            *args,
            **kwargs)

        return en.Column(column_data)

   
    def get_columns(self, *args, **kwargs):
        """Get the board's visible columns.

            Parameters

                args : `tuple`
                    The list of column return fields.
                kwargs : `dict`
                    The optional keywork arguments.

            Returns

                columns : `list[moncli.entities.Column]`
                    The board's columns.

            Return Fields

                archived : `bool`
                    Is the column archived or not.
                id : `str`
                    The column's unique identifier.
                pos : `str`
                    The column's position in the board.
                settings_str : `str`
                    The column's settings in a string form.
                title : `str`
                    The column's title.
                type : `str`
                    The column's type.
                width : `int`
                    The column's width.

            Optional Arguments

                ids : `str`
                    A list of column unique identifiers.
        """

        args = client.get_field_list(constants.DEFAULT_COLUMN_QUERY_FIELDS, *args)
        args = ['columns.' + arg for arg in args]
        column_kwargs = {}
        if kwargs:
            column_kwargs['columns'] = kwargs

        column_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)],
            limit=1,
            **column_kwargs)[0]['columns']

        return [en.Column(data) for data in column_data]


    def add_group(self, group_name: str, *args):
        """Creates a new group in the board.
    
            Parameters

                group_name : `str`
                    The name of the new group.
                args : `tuple`
                    The list of group return fields.

            Returns

                group : `moncli.entities.Group`
                    The created group.

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

        group_data = client.create_group(
            self.__creds.api_key_v2,
            self.id,
            group_name,
            *args)

        return en.Group(
            creds=self.__creds,
            __board=self,
            **group_data)


    def get_groups(self, *args, **kwargs):
        """Get the board's visible groups.

            Parameters

                args : `tuple`
                    The list of group return fields.
                kwargs : `dict`
                    Optional keyword arguments for getting board groups.

            Returns

                groups : `list[moncli.entities.Groups]`
                    The board's groups.

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

            Optional Arguments

                ids : `list[string]`
                    A list of group unique identifiers.
        """

        args = ['groups.' + arg for arg in client.get_field_list(constants.DEFAULT_GROUP_QUERY_FIELDS, *args)]
        group_kwargs = {}
        if kwargs:
            group_kwargs['groups'] = kwargs

        groups_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)],
            **group_kwargs)[0]['groups']

        return [en.Group(creds=self.__creds, __board=self, **data) for data in groups_data]
  

    def get_group(self, id: str = None, title: str = None, *args):
        """Get a group belonging to the board by ID or title.

            Parameters

                id : `str`
                    The group's unique identifier.
                    NOTE: This parameter is mutually exclusive and cannot be used with 'title'.
                title : `str`
                    The group's title.
                    NOTE: This parameter is mutually exclusive and cannot be used with 'id'.
                args : `tuple`
                    The list of group return fields.
        
            Returns

                group : `moncli.entities.Group`
                    The board's requested group.
        
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

        if id is None and title is None:
            raise NotEnoughGetGroupParameters()
        
        if id is not None and title is not None:
            raise TooManyGetGroupParameters()

        if id is not None:
            return self.get_groups(*args, ids=[id])[0]
        
        else:
            return [group for group in self.get_groups(*args) if group.title == title][0]


    def add_item(self, item_name: str, *args, **kwargs):
        """Create a new item in the board.

            Parameters

                item_name : `str`
                    The new item's name.

            Returns

                item : `moncli.entities.Item`
                    The created item.

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

                group_id : `str`
                    The group's unique identifier.
                column_values : `json`
                    The column values of the new item.
        """

        column_values = kwargs.pop('column_values', None)
        if column_values:
            if type(column_values) == dict:
                kwargs['column_values'] = column_values
            elif type(column_values) == list:
                kwargs['column_values'] = { value.id: value.format() for value in column_values }
            else:
                raise InvalidColumnValue(type(column_values).__name__)

        item_data = client.create_item(
            self.__creds.api_key_v2, 
            item_name, 
            self.id, 
            *args, 
            **kwargs)

        return en.Item(creds=self.__creds, __board=self, **item_data)


    def get_items(self, get_column_values: bool = False, *args, **kwargs):
        """Get the board's items (rows).

            Parameters

                args : `tuple`
                    The list of item return fields.
                get_column_values: `bool`
                    Flag used to include column values with the returned items.
                kwargs : `dict`
                    The optional keyword arguments for getting items.

            Returns

                items : `list[moncli.entities.Item]`
                    The board's items.
            
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

                ids : `list[str]`
                    The list of items unique identifiers.
                limit : `int`
                    Number of items to get.
                page : `int`
                    Page number to get, starting at 1.
        """
        
        if get_column_values:
            args = list(args)
            column_value_args = ['items.column_values.{}'.format(arg) for arg in constants.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]
            column_value_args.extend(['items.id', 'items.name'])
            for arg in column_value_args:
                if arg not in args:
                    args.append(arg)
        else:
            args = ['items.' + arg for arg in client.get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)]

        item_kwargs = {}
        if kwargs:
            item_kwargs['items'] = kwargs

        items_data = client.get_boards(
            self.__creds.api_key_v2,
            *args, 
            ids=[int(self.id)],
            **item_kwargs)[0]['items']

        return [en.Item(creds=self.__creds, __board=self, **item_data) for item_data in items_data] 


    def get_items_by_column_values(self, column_value: en.ColumnValue, get_column_values: bool = False, *args, **kwargs):
        """Search items in this board by their column values.
    
            Parameters

                column_value : `moncli.entites.ColumnValue`
                    The column value to search on.
                get_column_values: `bool`
                    Flag used to include column values with the returned items.
                args : `tuple`
                    The list of item return fields.
                kwargs : `dict`
                    The optional keyword arguments for searching items.
        
            Returns

                items : `list[moncli.entities.Item]`
                    The board's queried items.
        
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

                limit : `int`
                    Number of items to get.
                page : `int`
                    Page number to get, starting at 1.
                column_id : `str`
                    The column's unique identifier.
                column_value : `str`
                    The column value to search items by.
                column_type : `str`
                    The column type.
                state : `moncli.enumns.State`
                    The state of the item (all / active / archived / deleted), the default is active.
        """

        if get_column_values:
            args = list(args)
            column_value_args = ['column_values.{}'.format(arg) for arg in constants.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]
            column_value_args.extend(['id', 'name'])
            for arg in column_value_args:
                if arg not in args:
                    args.append(arg)

        if type(column_value) == cv.DateValue:
            value = column_value.date
        elif type(column_value) == cv.StatusValue:
            value = column_value.label
        else:
            value = column_value.format()

        items_data = client.get_items_by_column_values(
            self.__creds.api_key_v2, 
            self.id, 
            column_value.id, 
            value, 
            *args,
            **kwargs)

        return [en.Item(creds=self.__creds, __board=self, **item_data) for item_data in items_data]


    def get_column_values(self):
        """This method has not yet been implemented."""
        pass


    def get_column_value(self, id: str = None, title: str = None, **kwargs):
        """Create a column value from a board's column.

            Parameters

                id : `str`
                    The column's unique identifier.
                title : `str`
                    The column's title.
                kwargs : `dict`
                    The raw column value data to add.
        
            Returns

                column_value : `list[moncli.entities.ColumnValue]`
                    A new column_value instance.
        """

        if id is None and title is None:
            raise NotEnoughGetColumnValueParameters()

        if id is not None and title is not None:
            raise TooManyGetColumnValueParameters()

        columns = { column.id: column for column in self.columns }
        if id is not None:
            column = columns[id]
        elif title is not None:
            column = [column for column in columns.values() if column.title == title][0]

        column_type = column.column_type      
        return cv.create_column_value(column_type, id=column.id, title=column.title, settings_str=column.settings_str, **kwargs)


    def create_webhook(self, url: str, event: enums.WebhookEventType, *args, **kwargs):
        """Create a new webhook.
    
            Parameters

                url : `str`
                    The webhook URL.
                event : `moncli.enums.WebhookEventType`
                    The event to listen to (incoming_notification / change_column_value / change_specific_column_value / create_item / create_update).
                args : `tuple`
                    The list of webhook return fields.
                kwargs : `dict`
                    The optional keyword arguments for creating a webhook.
        
            Returns

                webhook : `moncli.entities.Webhook`
                    The created webhook.
        
            Return Fields

                board_id : `str`
                    The webhook's board id.
                id : `str`
                    The webhook's unique identifier.
            
            Optional Arguments

                config : `dict`
                    The webhook config.
                    Example: This argument is currenlty only available for the 'change_specific_column_value' event.
                    >>> board.create_webhook('http://test.website.com/webhook/test', WebhookEventType.change_specific_column_value, {'columnId': 'column_1'})
        """

        # Modify kwargs to config if supplied.
        if kwargs:
            if event != enums.WebhookEventType.change_specific_column_value:
                raise WebhookConfigurationError(event)
            kwargs = {'config': kwargs}

        webhook_data = client.create_webhook(
            self.__creds.api_key_v2, 
            self.id, 
            url, 
            event,
            *args,
            **kwargs)

        webhook_data['is_active'] = True
        return en.objects.Webhook(webhook_data)


    def delete_webhook(self, webhook_id: str, *args):
        """Delete a new webhook.
    
            Parameters

                id : `str`
                    The webhook's unique identifier.
                args : `tuple`
                    The list of webhook return fields.
        
            Returns

                webhook : `moncli.entities.Webhook`
                    The deleted webhook.
        
            Return Fields

                board_id : `str`
                    The webhook's board id.
                id : `str`
                    The webhook's unique identifier.
        """

        webhook_data = client.delete_webhook(
            self.__creds.api_key_v2, 
            webhook_id,
            *args)

        webhook_data['is_active'] = False
        return en.objects.Webhook(webhook_data)


    def get_workspace(self, *args):
        """Retrieves the board workspace
    
            Parameters

                args : `tuple`
                    The workspace return fields.
        
            Returns

                workspace : `list[moncli.entities.Workspace]`
                    The board workspace.
        
            Return Fields

                id : `str`
                    The workspace's unique identifier.
                name : `str`
                    The workspace's name.
                kind : `str`
                    The workspace's kind (open / closed)
                description : `str`
                    The workspace's description
        """
        
        args = client.get_field_list(constants.DEFAULT_WORKSPACE_QUERY_FIELDS, *args)
        args = ['workspace.{}'.format(arg) for arg in args]

        workspace_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[self.id])[0]['workspace']

        return en.Workspace(workspace_data)

    
    def get_updates(self, *args, **kwargs):
        """Retrieves the board's updates
 
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

        args = ['updates.'+ arg for arg in client.get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)]
        updates_kwargs = {}
        if kwargs:
            updates_kwargs = {'updates': kwargs}

        updates_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[self.id],
            **updates_kwargs)[0]['updates']

        return [en.Update(creds=self.__creds, **data) for data in updates_data]

    
    def get_tags(self, *args):
        """Retrieves the board's tags

            Parameters

                args : `tuple`
                    The list of tag return fields.
                kwargs : `dict`
                    Optional keyword arguments for querying tags.

            Returns

                tags : `list[moncli.entities.Tag]`
                    A collection of tags.

            Return Fields

                color : `str`
                    The tag's color.
                id : `str`
                    The tag's unique identifier.
                name : `str`
                    The tag's name.

            Optional Arguments

                ids : `list[str]`
                    The list of tags unique identifiers.
        """

        args = ['tags.'+ arg for arg in client.get_field_list(constants.DEFAULT_TAG_QUERY_FIELDS, *args)]

        tags_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[self.id])[0]['tags']

        return [en.Tag(data) for data in tags_data]

        
class TooManyGetGroupParameters(Exception):
    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a group."
        

class NotEnoughGetGroupParameters(Exception):
    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a group."


class InvalidColumnValue(Exception):
    def __init__(self, column_value_type: str):
        self.message = "Unable to use column value of type '{}' with the given set of input parameters".format(column_value_type)


class TooManyGetColumnValueParameters(Exception):
    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a column value."
        

class NotEnoughGetColumnValueParameters(Exception):
    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a column value."

class WebhookConfigurationError(Exception):
    def __init__(self, event: enums.WebhookEventType):
        self.message = "Webhook event type '{}' does not support configuraitons".format(event.name)
