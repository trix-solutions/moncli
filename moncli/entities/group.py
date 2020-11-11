from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, entities as en
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

    __________
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

    _______
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
        self.__creds = kwargs.pop('creds')
        self.__board_id = kwargs.pop('board_id')
        self.__items = None
        items = kwargs.pop('items', None)
        if items:
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

        __________
        Parameters

            args : `tuple`
                The list of group fields to return.

        _______
        Returns

            group : `moncli.entities.Group`
                The duplicated group.

        _____________
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
        
        __________________
        Optional Arguments

            add_to_top : `bool`
                Should the new group be added to the top.
            group_title : `str`
                The group's title.
        """

        group_data = client.duplicate_group(
            self.__creds.api_key_v2, 
            self.__board_id, 
            self.id, 
            *args,
            **kwargs)
        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)


    def archive(self, *args):
        """Archives this group.

        __________
        Parameters

            args : `tuple`
                The list of group fields to return.

        _______
        Returns

            group : `moncli.entities.Group`
                The archived group.

        _____________
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
            self.__board_id,
            self.id, 
            *args)
        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)


    def delete(self, *args):
        """Delete this group.

        __________
        Parameters

            args : `tuple`
                The list of group fields to return.

        _______
        Returns

            item : `moncli.entities.Item`
                The deleted item.

        _____________
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
            self.__board_id,
            self.id, 
            *args)
        return Group(
            creds=self.__creds,
            board_id=self.__board_id,
            **group_data)


    def add_item(self, item_name: str, *args, **kwargs):
        """Add item to this group.

        __________
        Parameters

            item_name : `str`
                The new item's name.
            args : `tuple`
                The list of item fields to return.
            kwargs : `dict`
                Optional keyword arguments for adding an item to this group.

        _______
        Returns

            item : `moncli.entities.Item`
                The newly added item to the group.

        _____________
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

        __________________
        Optional Arguments

            column_values : `json`
                The column values of the new item.
        """

        item_data = client.create_item(
            self.__creds.api_key_v2,
            item_name,
            self.__board_id, 
            *args,
            group_id=self.id,
            **kwargs)
        return en.Item(creds=self.__creds, **item_data)


    def get_items(self, *args, **kwargs):
        """Get items from this group.

        __________
        Parameters

            args : `tuple`
                The list of item fields to return.

        _______
        Returns

            items : `list[moncli.entities.Item]`
                The collection of items belonging to the group.

        _____________
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

        __________________
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

        args = client.get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
        args = ['groups.items.' + field for field in args]
        if kwargs:
            kwargs = {'groups': {'items': kwargs}}
        items_data = client.get_boards(
            self.__creds.api_key_v2, 
            *args,
            ids=[int(self.__board_id)],
            limit=1,
            groups={'ids': [self.id]},
            **kwargs)[0]['groups'][0]['items']
        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data]
