from schematics.models import Model
from schematics import types

from .. import api_v2 as client, entities as en
from ..api_v2 import constants

class _Group(Model):
    """Group base model"""

    id = types.StringType(required=True)
    title = types.StringType()
    archived = types.BooleanType()
    color = types.StringType()
    deleted = types.BooleanType()
    position = types.StringType()


class Group(_Group):
    """ A group of items in a board.

        Properties

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

        Methods

            duplicate : `moncli.entities.Group`
                Duplicate this group.
            archive : `moncli.entities.Group`
                Archives this group.
            delete : `moncli.entities.Group`
                Delete this group.
            add_item : `moncli.entities.Item`
                Add item to this group.
            get_items : `list[moncli.entities.Item]`
                Get items from this group.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds', None)
        self.__board = kwargs.pop('__board', None)
        self.__items = kwargs.pop('__items', None)

        items = kwargs.pop('items', None)
        if items != None and not self.__items:
            self.__items = [en.Item(creds=self.__creds, **items)]

        super(Group, self).__init__(kwargs)
    
    def __repr__(self):
        o = self.to_primitive()
        if self.__items:
            o['items'] = [item.to_primitive() for item in self.__items]
        return str(o)

    @property
    def items(self):
        """The items in the group."""
        if not self.__items:
            self.__items = self.get_items()
        return self.__items


    def duplicate(self, add_to_top: bool = False, *args, **kwargs):
        """Duplicate this group.

            Parameters

                args : `tuple`
                    The list of group fields to return.

            Returns

                group : `moncli.entities.Group`
                    The duplicated group.

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

                add_to_top : `bool`
                    Should the new group be added to the top.
                group_title : `str`
                    The group's title.
        """

        group_data = client.duplicate_group(
            self.__creds.api_key_v2, 
            self.__board.id, 
            self.id, 
            *args,
            **kwargs)
        return Group(
            creds=self.__creds,
            __board=self.__board.id,
            **group_data)


    def archive(self, *args):
        """Archives this group.

            Parameters

                args : `tuple`
                    The list of group fields to return.

            Returns

                group : `moncli.entities.Group`
                    The archived group.

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

        group_data = client.archive_group(
            self.__creds.api_key_v2,
            self.__board.id,
            self.id, 
            *args)
        return Group(
            creds=self.__creds,
            __board=self.__board,
            **group_data)


    def delete(self, *args):
        """Delete this group.

            Parameters

                args : `tuple`
                    The list of group fields to return.

            Returns

                item : `moncli.entities.Item`
                    The deleted item.

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

        group_data = client.delete_group(
            self.__creds.api_key_v2,
            self.__board,
            self.id, 
            *args)
        return Group(
            creds=self.__creds,
            __board=self.__board,
            **group_data)


    def add_item(self, item_name: str, *args, **kwargs):
        """Add item to this group.

            Parameters

                item_name : `str`
                    The new item's name.
                args : `tuple`
                    The list of item fields to return.
                kwargs : `dict`
                    Optional keyword arguments for adding an item to this group.

            Returns

                item : `moncli.entities.Item`
                    The newly added item to the group.

            Return Fields

                assets : `list[moncli.entities.set.Asset]`
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

        item_data = client.create_item(
            self.__creds.api_key_v2,
            item_name,
            self.__board.id, 
            *args,
            group_id=self.id,
            **kwargs)
        return en.Item(creds=self.__creds, **item_data)


    def get_items(self, get_column_values: bool = True, *args, **kwargs):
        """Get items from this group.
    
            Parameters

                get_column_values: `bool`:
                    Retrieves item column values if set to `True`.
                args : `tuple`
                    The list of item fields to return.
        
            Returns

                items : `list[moncli.entities.Item]`
                    The collection of items belonging to the group.
        
            Return Fields

                assets : `list[moncli.entities.set.Asset]`
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
                    Number of items to get; the default is 25.
                page : `int`
                    Page number to get, starting at 1.
                ids : `list[str]`
                    A list of items unique identifiers.
                newest_first : `bool`
                    Get the recently created items at the top of the list.
        """

        if get_column_values:
            args = list(args)
            column_value_args = ['groups.items.column_values.{}'.format(arg) for arg in constants.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]
            column_value_args.extend(['groups.items.id', 'groups.items.name'])
            for arg in column_value_args:
                if arg not in args:
                    args.append(arg)
        else:
            args = client.get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
            args = ['groups.items.' + field for field in args]
            
        group_kwargs = {'groups': {'ids': [self.id]}}
        if kwargs:
            group_kwargs['groups']['items'] = kwargs
        items_data = client.get_boards(
            self.__creds.api_key_v2, 
            *args,
            ids=[int(self.__board.id)],
            limit=1,
            **group_kwargs)[0]['groups'][0]['items']
        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data]
