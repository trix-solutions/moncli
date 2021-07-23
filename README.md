# moncli
A Python Client and CLI tool for Monday.com

### Table of Contents ###
* [Setup](#setup). 
* [Getting Started...](#getting-started)  
   * [Introducing the MondayClient](#introducing-the-mondayclient)
   * [Managing Boards](#managing-boards)
   * [Working with Columns, Groups, and Items](#working-with-columns-groups-and-items)
   * [Changing Column Values](#changing-column-values)
   * [Posting Updates](#posting-updates)
   * [Uploading Files](#uploading-files)
* [Moncli Entities](#moncli-entities)  
   * [MondayClient](#mondayclient)  
   * [Board](#board)  
   * [Group](#group)  
   * [Item](#item)  
   * [Update](#update)  
   * [File/Asset](#file)  
   * [User](#user)  
   * [Account](#account)  
   * [Other Entities](#other-entities)  
* [Column Values](#column-values)  
* [Using the API v2 Client](#using-the-api-v2-client)  
* [Creating Custom GraphQL Queries](#creating-custom-graphql-queries)  
  

# Setup #
To add the moncli package to your project, simply execute the following command within your Python 3 environment using pip.  Please note that this package is currently available for Python 3
```
$ pip3 install moncli
```
   
# Getting Started... #

## Introducing the MondayClient ##
Getting started with the moncli Python package is simple.  To begin, create a default __MondayClient__ istance using the following code below:
```
>>> from moncli import client
>>> client.api_v2_key = api_v2_key
```
The __MondayClient__ object is the entry point for all client activities and includes functionality for board, item, tag, and user management.

The _api_key_v1_ and _api_key_v2_ parameters represent the user/account monday.com API access keys and can be found by navigating to __https://<your_instance_name>.monday.com/admin/integrations/api__ and copying both the API v1 (personal or company) and API v2 keys.

Additional information regarding __MondayClient__ properties/methods can be found in the [MondayClient](#mondayclient) section below.

## Managing Boards ##
Boards are cornerstones for any Monday.com setup, and __Board__ objects are no exception containing functionality for general data management with columns, groups, and items.  The next sections below will provide some general tools regarding __Board__ management.

New boards are created with the __MondayClient__ instance using the _create_board_ method as shown in the example below. 
```
>>> # Import Boardkind enum for parameter input.
>>> from moncli import BoardKind
>>>
>>> # Create a new public board
>>> board_name = 'New Public Board'
>>> board_kind = BoardKind.public
>>> new_board = client.create_board(board_name, board_kind)
```  

Existing boards are also retrieved with the __MondayClient__ using the _get_boards_ method using the _ids_ keyword argument as shown below.
```
>>> board_ids = ['12345']
>>> retrieved_boards = client.get_boards(ids=[board_ids])
```

When looking to retrieve only a single board by either id or name, the _get_board_ method is also available on the __MondayClient__ instance using either the _id_ or _name_ keyword argument as shown below.  
```
>>> # Retrieve a board by ID.
>>> board_id = '12345'
>>> board_by_id = client.get_board(id=board_id)
>>>
>>> # Retrieve a board by Name
>>> board_name = 'Existing Public Board'
>>> retrieved_board = client.get_board(name='board_name')
```

__PLEASE NOTE:__ Querying boards by name is not a built-in feature for Monday.com and may be less performant that searching for a board by ID.

Finally, boards are archived using the _archive_board_ method on the __MondayClient__ instance as shown below.
```
>>> board_id = '12345'
>>> archived_board = client.archive_board(board_id)
```

Additional information regarding the __Board__ object can be found in the [Board](#board) section below.  

## Working with Columns, Groups, and Items ##

### Adding and Getting Columns ###

Columns contain metadata that pertains to the data types available to current and future board items. Board columns are represented by the __Column__ object.  A new column is created from a __Board__ instance using the *add_column* method and returned as a __Column__ object as shown below.

```
>>> from moncli import ColumnType
>>>
>>> new_column = board.add_column(title='New Text Column', column_type=ColumnType.text)
```

Columns are retrieved from a __Board__ instance using the *get_columns* method as shown below.

```
>>> columns = board.get_columns('id', 'title', 'type')
```

### Managing Groups ###

Groups contain lists of items within a board.  In moncli, these groups are realized as __Group__ objects are are retrieved from a __Board__ in the following way.

```
>>> groups = board.get_groups('id','name')
```

Groups are also created via a __Board__ instance, as shown below.

```
>>> group_name = 'New Group'
>>> group = board.add_group(group_name, 'id', 'name')
```

Once created a group may be duplicated, archived or deleted in the following ways.

```
>>> # Duplicate a group.
>>> duplicate_group = group.duplicate()
>>>
>>> # Archive a group.
>>> archived_group = group.archive()
>>>
>>> # Delete a group.
>>> deleted_group = group.delete()
```

### Using Items ###

Items in monday.com represent individual records containing column value data.  These items exist inside of the various board groups.  Items are created by either a __Board__ or __Group__ instance as shown below.  Please note that when creating items from a __Board__ instance, the item is placed into the topmost group if the *group_id* parameter is not specified.

```
>>> item_name = 'New Item 1'
>>>
>>> # Add item via board.
>>> group_id = 'group_1'
>>> item = board.add_item(item_name, group_id=group_id)
>>>
>>> # Add item via group.
>>> item = group.add_item(item_name)
```

An __Item__ object can be created with column values using the optional *column_values* parameter.  Values for this parameter can be input as a dictionary in which each key represents the ID of the column to update and the value represents the value to add.  

```
>>> column_values = {'text_column_1': 'New Text Value'}
>>> new_item_with_values = board.add_item(item_name='New Item With Text Value', column_values=column_values)
```

Items are also retrieved by either a __Client__, __Board__, or __Group__ instance via the *get_items* methods.  It is important to note that the __Client__ instance has access to all items created within the account that are accessible to the user.  When using a __Board__ or a __Group__ instance, only items accessible to the user within the respective board or group are available to query.

Once an __Item__ instance is retrieved, it can be moved between groups, duplicated, archived, or deleted as shown in the example below.

```
>>> # Move item to group.
>>> item.move_to_group('group_2')
>>>
>>> # Duplicate item with updates
>>> item.duplicate(with_updates=True)
>>>
>>> # Archive an item.
>>> item.archive()
>>> 
>>> # Delete an item.
>>> item.delete()
```


## Changing Column Values ##

The column values of an item may also be retrieved and updated from an __Item__ instance in the following way as shown below.  
```
>>> # First get the column value.
>>> # Index for item.column_values may be the column id, title, or the list index integer.
>>> column_value = item.column_values['text_colunn_1']
>>> # Update the column text
>>> column_value.text = 'Update Text'
>>> # Now update the column value in the item.
>>> item.change_column_value(column_value)
```

Multiple column values are retrieved and updated from the __Item__ instance using the *change_multiple_column_values* and *get_column_values* methods respectively.  More information on these methods can be found below in the [Item](#item) section of this document.

## Posting Updates ##
Updates represent interactions between users within a monday.com account with respect to a given item and are represented in moncli as an __Update__ object.  __Update__ instances are retrieved using the *get_updates* method from either a __MondayClient__ instance, which can retrieve all updates within the account accessible to the login user, or an __Item__ instance, which only has access to updates within the particular item.  

Updates are added to an item using the *add_update* method from the __Item__ instance as shown below.
```
>>> update = item.add_update('Hello, World!')
```

Once created, replies are also added to an update using the *add_reply* method from the __Update__ instance as shown below.
```
>>> reply = update.add_reply('Right back at you!')
```

Finally updates are removed from the __Item__ instance using either the *delete_update* method for removing a specific update, or the *clear_all_updates* method to remove all updates on the item as shown below.
```
>>> # Remove one update
>>> item.delete_update(update.id)
>>>
>>> # Remove all updates
>>> item.clear_all_updates()
```

More information regarding Updates and Replies can be found in the [Update](#update) and [Reply](#other-entities) sections in the documentation below.

## Uploading Files ##

Files, or assets, represent files uploaded to items via a file-type column or updates via the *add_file* method on both __Item__ and __Update__ objects. 

When adding files to an item, a file column via the __FileColumn__ object must be identified as the column in which to place the newly uploaded file.  This is demonstrated in the example below.
```
>>> # First get the file column.
>>> file_column = item.get_column_value(id='file_column_1')
>>> # Then upload the file.
>>> asset = item.add_file(file_column, '/users/test/monday_files/test.jpg')
```

Adding files to an update only requires the file path of the file to upload as shown below.
```
>>> asset = update.add_file('/users/test/monday_files/test.jpg')
```

Files are retrieved using the *get_files* method available on any __MondayClient__, __Item__, or __Update__ instance.  It is important to note that all files within the account accessible to the user are retrieved from the __MondayClient__ instance, while only files within the respective item or update are retrieved for __Item__ and __Update__ instances respectively.

Currently, the monday.com API only supports removing all files from a file column within an item.  This is done using the *remove_files* method of the __Item__ instance in the example shown below.
```
>>> # First get the file column.
>>> file_column = item.get_column_value(id='file_column_1')
>>> # Then clear all files.
>>> assets = item.remove_files(file_column)
```

To remove files from an update, the only option currently available is to delete the update containing the file.  This is done using the *delete_update* method via an __Item__ instance or directly on an __Update__ instance with the *delete* method.

More information regarding the __Asset__ object is found in the [File/Asset](#file) section of the documentation below.

# Moncli Entities #
The moncli client returns entities representing Monday.com objects after executing a successful request to the API.  These entities not only contain properties representing the return fields of the query/mutation, but also contain various methods for retrieving other related entities.   

Aside from required parameters, entity methods also contain an \*args parameter that allows for a collection of custom return field inputs. Simply add the name of the field to return (as defined by the monday.com query) as a string. To return nested fields, simply list out the full path of the field in dot notation (ex. 'items.id' will return items associated with the query with a populated _id_ property.   

Optional parameters for moncli entity methods are added as keyword arguments via the \*kwargs variable.

## MondayClient ##
This section contains all properties and methods contained within the __MondayClient__ object.  

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|me          |[User](#user)      |The client login user.      |

### Methods ###

**create_board**  
Create a new board.
Returns: [moncli.entities.Board](#board)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|board_name    |str                      |The board's name.                           |
|board_kind    |moncli.enums.BoardKind   |The board's kind (public / private / share).|
|workspace_id  |str                      |Optional workspace id.                      |
|template_id   |str                      |Optional board template id.                 |

*Example*
```
>>> from moncli import BoardKind
>>> 
>>> board_name = 'New Public Board'
>>> board_kind = BoardKind.public
>>> new_board = client.create_board(board_name, board_kind, 'id', 'name')
>>> new_board
{'id': '12345', 'name': 'New Public Board'}
```

**get_boards**  
Get a collection of boards.  
Returns: [list[moncli.entities.Board]](#board)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit (Optional)|int|Number of boards to get; the default is 25.|
|page (Optional)|int|Page number to get, starting at 1.|
|ids (Optional)|list[str]|A list of boards unique identifiers.|
|board_kind (Optional)|moncli.enums.BoardKind|The board's kind (public / private / share)|
|state|moncli.enums.State|The state of the board (all / active / archived / deleted), the default is active.|

*Example*
```
>>> ids = ['12345']
>>> boards = client.get_boards('id', 'name', ids=ids)
>>> boards
[{'id': '12345', 'name': 'New Public Board'}]
```

**get_board**  
Get a board by unique identifier or name.  
Returns: [moncli.entities.Board](#board)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The unique identifier of the board to retrieve.  NOTE: This parameter is mutually exclusive and cannot be used with 'name'.|
|name|str|The name of the board to retrieve.  NOTE: This parameter is mutially exclusive and cannot be used with 'id'.|

*Example*
```
>>> id = '12345
>>> board = client.get_board(id, None, 'id', 'name')
>>> board
{'id': '12345', 'name': 'New Public Board'}
>>>
>>> name = 'New Public Board'
>>> board = client.get_board(None, name, 'id', 'name')
>>> board
{'id': '12345', 'name': 'New Public Board'}
```

**get_board_by_id**  
Get a board by unique identifier.   
Returns: [moncli.entities.Board](#board)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The unique identifier of the board.|

*Example*
```
>>> id = '12345
>>> board = client.get_board_by_id(id, 'id', 'name')
>>> board
{'id': '12345', 'name': 'New Public Board'}
```


**get_board_by_name**  
Get a board by name.   
Returns: [moncli.entities.Board](#board)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|name|str|The name of the board to retrieve.|

*Example*
```
>>> name = 'New Public Board
>>> board = client.get_board_by_name(name, 'id', 'name')
>>> board
{'id': '12345', 'name': 'New Public Board'}
```

**archive_board**  
Archive a board.   
Returns: [moncli.entities.Board](#board)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|board_id|str|The board's unique identifier.|

*Example*
```
>>> id = '12345'
>>> archived_board = client.archive_board(id, 'id', 'name', 'state')
>>> archived_board
{'id': '12345', 'name': 'New Public Board', 'state': 'archived'}
```

**get_assets**  
Get a collection of assets by IDs.   
Returns: [list[moncli.entities.Asset]](#file)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids|list[str]|Ids of the assets/files you want to get.|

*Example*
```
>>> assets_ids = ['12345678']
>>> assets = client.get_assets(assets_ids, 'id', 'name', 'public_url')
>>> assets
[{'id': '12345678', 'name': 'test.jpg', 'public_url': 'https://test.monday.com/files/test.jpg'}]
```

**get_items**  
Get a collection of items.     
Returns: [list[moncli.entities.Item]](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit (Optional)|int|Number of items to get; the default is 25.|
|page (Optional)|int|Page number to get, starting at 1.|
|ids (Optional)|list[str]|A list of items unique identifiers.|
|newest_first (Optional)|bool|Get the recently created items at the top of the list.|

*Example*
```
>>> item_ids = ['123456']
>>> items = client.get_items('id', 'name', ids=ids)
>>> items
[{'id': '123456', 'name': 'New Item'}]
```

**get_updates**  
Get a collection of updates.  
Returns: [list[moncli.entities.Update]](#update)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit (Optional)|int|Number of updates to get; the default is 25.|
|page (Optional)|int|Page number to get, starting at 1.|

*Example*
```
>>> updates = client.get_updates('id', 'text_body')
>>> updates
[{'id': '1234567', 'text_body': 'Hello, World!'}]
```

**delete_update**  
Delete an update.   
Returns: [moncli.entities.Update](#update)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The update's unique identifier.|

*Example*
```
>>> update_id = '1234567'
>>> deleted_update = client.delete_update(update_id, 'id','text_body')
>>> deleted_update
{'id': '1234567', 'text_body': 'Hello, World!'}
```

**clear_item_updates**  
Clear an item's updates.     
Returns: [moncli.entities.Item](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|item_id|str|The item's unique identifier.|

*Example*
```
>>> item_id = '123456'
>>> item = client.clear_item_updates(item_id, 'id', 'name', 'updates.id')
>>> item
{'id': '123456', 'name': 'New Item', 'updates': []}
```

**create_notification**  
Create a new notification.  
Returns: [moncli.entities.Notification](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|text|str|The notification text.|
|user_id|str|The user's unique identifier.|
|target_id|str|The target's unique identifier.|
|target_type|moncli.enums.NotificationTargetType|The target's type (Project / Post)|
|payload|json|The notification payload.|

*Example*
```
>>> from moncli.enums import NotificationTargetType
>>>
>>> text = 'Hello, World!'
>>> user_id = '1234'
>>> target_id = '1235'
>>> notification_type = NotificationTargetType.Post
>>> notification = client.create_notification(text, user_id, target_id, notification_type, 'id', 'text')
>>> notification
{'id': '123456789', 'text': 'Hello, World!'}
```

**create_or_get_tag**  
Create a new tag or get it if it already exists.    
Returns: [moncli.entities.Tag](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|tag_name|str|The new tag's name|
|board_id (Optional)|str|The private board id to create the tag at (not needed for public boards).|

*Example*
```
>>> tag_name = 'New Tag'
>>> tag = client.create_or_get_tag(tag_name, 'id', 'name')
>>> tag
{'id': '1234567890', 'name': 'New Tag'}
```

**get_tags**  
Get a collection of tags.  
Returns: [list[moncli.entities.Tag]](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|list[str]|The list of tags unique identifiers.|

*Example*
```
>>> tags_ids = ['1234567890']
>>> tags = client.get_tags('id','name', ids=tags_ids)
>>> tags
[{'id': '1234567890', 'name': 'New Tag'}]
```

**get_users**  
Get a collection of users.  
Returns: [list[moncli.entities.User]](#user)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|list[str]|A list of users unique identifiers.|
|kind (Optional)|moncli.entities.UserKind|The kind to search users by (all / non_guests / guests / non_pending).|
|newest_first (Optional)|bool|Get the recently created users at the top of the list.|
|limit (Optional)|int|Number of users to get.|

*Example*
```
>>> ids = ['1234']
>>> users = client.get_users('id', 'name', ids=ids)
>>> users
[{'id': '1234', 'name': 'Test User'}]
```

**get_teams**  
Get a collection of teams.  
Returns: [list[moncli.entities.Team]](#user)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|list[str]|A list of teams unique identifiers.|

*Example*
```
>>> ids = ['123']
>>> teams = client.get_teams('id', 'name', ids=ids)
>>> teams
{'id': '123', 'name': 'Test Team'}
```

**get_me**  
Get the conected user's information.   
Returns: [moncli.entities.User](#user)

*Example*
```
>>> user = client.get_me('id','name')
>>> user
{'id': '1234', 'name': 'Test User'}
```

**get_account**  
Get the connected user's account.   
Returns: [moncli.entities.Account](#account)

*Example*
```
>>> account = client.get_account('name', 'first_day_of_the_week')
>>> account
{'name': 'Test Account', 'first_day_of_the_week': 'monday'}
```

**create_workspace**  
Create a new workspace.   
Returns: [moncli.entities.Workspace](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|name|str|The workspace's name.|
|kind|moncli.enums.WorkspaceKind|The workspace's kind (open / closed)|
|description (Optional)|str|The workspace's description.|

*Example*
```
>>> from moncli.enums import WorkspaceKind
>>>
>>> name = 'New Workspace'
>>> kind = WorkspaceKind.open
>>> workspace = client.create_workspace(name, kind, 'id', 'name')
>>> workspace
{'id': '12', 'name': 'New Workspace'}
```

## Board ##
This section contains all properties and methods contained within the __Board__ object.  

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|activity_logs|[list[moncli.entities.ActivityLog]](#other-entities)|The board log events.|
|board_folder_id|str|The board's folder unique identifier.|
|board_kind|str|The board's kind (public / private / share).|
|columns|[list[moncli.entities.Column]](#other-entities)|The board's visible columns.|
|communication|str|Get the board communication value - typically meeting ID.|
|description|str|The board's description.|
|groups|[list[moncli.entities.Group]](#group)|The board's visible groups.|
|id|str|The unique identifier of the board.|
|items|[list[moncli.entities.Item]](#item)|The board's items (rows).|
|name|str|The board's name.|
|owner|[moncli.entities.User](#user)|The owner of the board.|
|permissions|str|The board's permissions.|
|pos|str|The board's position.|
|state|str|The board's state (all / active / archived / deleted).|
|subscribers|[list[moncli.entities.User]](#user)|The board's subscribers.|
|tags|[list[moncli.entities.Tag]](#other-entities)|The board's specific tags.
|top_group|[moncli.entities.Group](#group)|The top group at this board.
|updated_at|str|The last time the board was updated at (ISO8601 DateTime).|
|updates|[list[moncli.entities.Update]](#update)|The board's updates.
|views|[list[moncli.entities.BoardView]](#other-entities)|The board's views.|
|workspace|[moncli.entities.Workspace](#other-entities)|The workspace that contains this board (null for main workspace).|
|workspace_id|str|The board's workspace unique identifier (null for main workspace).

### Methods ###

**get_activity_logs**  
Get the board log events.   
Returns: [list[moncli.entities.ActivityLog]](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit|int|Number of items to get, the default is 25.|
|page|int|Page number to get, starting at 1.|
|user_ids|list[str]|User ids to filter.|
|column_ids|list[str]|Column ids to filter.|
|group_ids|list[str]|Group ids to filter.|
|item_ids|list[str]|Item id to filter|
|from|str|From timespamp (ISO8601).|
|to|str|To timespamp (ISO8601).|

*Example*
```
>>> activity_logs = board.get_activity_logs('id','data')
>>> activity_logs
[{'id': '12345678901', 'data': 'INSERT_COLIMN_DATA_HERE'}]
```

**get_views**  
Get the board's views.   
Returns: [list[moncli.entities.BoardView]](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|str|The list of view unique identifiers.|
|type (Optional)|str|The view's type.|

*Example*
```
>>> views = board.get_views('id', 'name')
>>> views
[{'id': 'test_view_1', 'name': 'Test View 1'}]
```

**add_subscribers**  
Add subscribers to this board.   
Returns: list[moncli.entities.User]](#user)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|user_ids|list[str]|User ids to subscribe to a board.|
|kind (Optional)|moncli.enums.SubscriberKind|Subscribers kind (subscriber / owner).|

*Example*
```
>>> user_ids = ['1234']
>>> subscribers = board.add_subscribers(user_ids, 'id', 'name')
>>> subscribers
[{'id': '1234', 'name': 'Test User'}]
```

**get_subscribers**  
Get board subscribers.   
Returns: list[moncli.entities.User]](#user)

*Example*
```
>>> subscribers = board.get_subscribers('id', 'name')
>>> subscribers
[{'id': '1234', 'name': 'Test User'}]
```

**delete_subscribers**  
Remove subscribers from the board.   
Returns: list[moncli.entities.User]](#user)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|user_ids|list[str]|User ids to unsubscribe from board.

*Example*
```
>>> user_ids = ['1234']
>>> subscribers = board.delete_subscribers(user_ids, 'id', 'name')
>>> subscribers
[{'id': '1234', 'name': 'Test User'}]
```

**add_column**  
Create a new column in board.   
Returns: [moncli.entities.Column](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|title|str|The new column's title.|
|column_type|moncli.enums.ColumnType|The type of column to create.|
|defaults (Optional)|json|The new column's defaults.|

*Example*
```
>>> from moncli.enums import ColumnType
>>>
>>> title = 'New Text Column'
>>> column_type = ColumnType.text
>>> column = board.add_column(title, column_type, 'id','name')
>>> column
{'id': 'text_column_1', 'name': 'New Text Column'}
```

**get_columns**  
Get the board's visible columns.   
Returns: [list[moncli.entities.Column]](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|str|A list of column unique identifiers.|

*Example*
```
>>> columns = board.get_columns()
>>> columns
{'id': 'text_column_1', 'name': 'New Text Column'}
```

**add_group**  
Creates a new group in the board.   
Returns: [moncli.entities.Group](#group)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|group_name|str|The name of the new group.|

*Example*
```
>>> group_name = 'New Group'
>>> group = board.add_group(group_name, 'id', 'name')
{'id': 'group_1', 'name': 'New Group'}
```

**get_groups**  
Get the board's visible groups.   
Returns: [list[moncli.entities.Group]](#group)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|list[string]|A list of group unique identifiers.|

*Example*
```
>>> groups = board.get_groups('id', 'name')
[{'id': 'group_1', 'name': 'New Group'}]
```

**get_group**  
Get a group belonging to the board by ID or title.   
Returns: [moncli.entities.Group](#group)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The group's unique identifier.  NOTE: This parameter is mutually exclusive and cannot be used with 'title'.|
|title|str|The group's title.  NOTE: This parameter is mutually exclusive and cannot be used with 'id'.|

*Example*
```
>>> # Get group by id.
>>> group_id = 'group_1'
>>> group = board.get_group(group_id, None, 'id', 'name')
{'id': 'group_1', 'name': 'New Group'}
>>>
>>> # Get group by name.
>>> group_name = 'New Group'
>>> group = board.get_group(None, group_name, 'id', 'name')
{'id': 'group_1', 'name': 'New Group'}
```

**add_item**  
Create a new item in the board.   
Returns: [moncli.entities.Item](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|item_name|str|The new item's name.|
|group_id (Optional)|str|The group's unique identifier.|
|column_values (Optional)|json|The column values of the new item.|
                
*Example*
```
>>> item_name = 'New Item'
>>> item = board.add_item(item_name, 'id', 'name')
>>> item
{'id': '1234567', 'name': 'New Item'}
```

**get_items**  
Get the board's items (rows).   
Returns: [list[moncli.entities.Item]](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|ids (Optional)|list[str]|The list of items unique identifiers.|
|limit (Optional)|int|Number of items to get.|
|page (Optional)|int|Page number to get, starting at 1.|

*Example*
```
>>> items = board.get_items('id', 'name')
>>> items
[{'id': '1234567', 'name': 'New Item'}]
```

**get_items_by_column_values**  
Search items in this board by their column values.   
Returns: [list[moncli.entities.Item]](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|column_value|moncli.entites.ColumnValue|The column value to search on.|
|limit (Optional)|int|Number of items to get.|
|page (Optional)|int|Page number to get, starting at 1.|
|column_id (Optional)|str|The column's unique identifier.|
|column_value (Optional)|str|The column value to search items by.|
|column_type (Optional)|str|The column type.|
|state (Optional)|moncli.enumns.State|The state of the item (all / active / archived / deleted), the default is active.|

*Example*
```
>>> column_id = 'test_column'
>>> column_value = board.get_column_value(column_id)
>>> column_value.text = 'Search Text'
>>> items = board.get_items_by_column_values(column_value, 'id', 'name')
>>> items
[{'id': '1234567', 'name': 'New Item'}]
```

**get_column_value**  
Create a column value from a board's column.   
Returns: [moncli.entities.ColumnValue](#working-with-column-values)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The column's unique identifier. NOTE: This parameter is mutually exclusive and cannot be used with 'title'|
|title|str|The column's title. NOTE: This parameter is mutually exclusive and cannot be used with 'id'|

*Example*
```
>>> column_value = board.get_column_value('test_column', 'Test Column')
>>> column_value
{'id': 'test_column', 'name': 'Test Column', 'value': '{\"text\": \"Test Value\"}'}
```

**create_webhook**  
Create a new webhook.   
Returns: [moncli.entities.Webhook](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|url|str|The webhook URL.|
|event|moncli.enums.WebhookEventType|The event to listen to (incoming_notification / change_column_value / change_specific_column_value / create_item / create_update).|
|config (Optional)|dict|The webhook config.|

*Example*
```
>>> from moncli.enums import WebhookEventType
>>>
>>> url = 'http://test.website.com/webhook/test'
>>> event = WebhookEventType.create_item
>>> webhook = board.create_webhook(url, event, 'id', 'board_id')
>>> webhook
{'id': '2345', 'board_id': '12345'}
>>>
>>> # Create a webhook using the config parameter.
>>> event = WebhookEventType.change_specific_column_value
>>> config = {'columnId': 'column_1'}
>>> webhook = board.create_webhook(url, event, 'id', 'board_id', config=config)
>>> webhook
{'id': '2346', 'board_id': '12345'}
```

**delete_webhook**  
Delete a new webhook.   
Returns: [moncli.entities.Webhook](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The webhook's unique identifier.|

*Example*
```
>>> webhook_id = '2345'
>>> webhook = board.delete_webhook(webhook_id, 'id', 'board_id')
>>> webhook
{'id': '2345', 'board_id': '12345'}
```

**get_workspace**  
Get the board's workspace that contains this board (null for main workspace).   
Returns: [moncli.entities.Workspace](#other-entities)

*Example*
```
>>> workspace = board.get_workspace('name', 'kind')
>>> workspace
{'name': 'New Workspace', 'kind': 'open'}
```

## Group ##
This section contains all properties and methods contained within the __Group__ object.  

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|archived|bool|Is the group archived or not.|
|color|str|The group's color.|
|deleted|bool|Is the group deleted or not.|
|id|str|The group's unique identifier.|
|items|[list[moncli.entities.Item]]|The items in the group.|
|position|str|The group's position in the board.|
|title|str|The group's title.|
            
### Methods ###

**duplicate**  
Duplicate this group.  
Returns: [moncli.entities.Group](#group)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|add_to_top (default=False)|bool|Should the new group be added to the top.|
|group_title (Optional)|str|The group's title.|

*Example*
```
>>> duplicate = group.duplicate('id', 'name')
>>> duplicate
{'id': 'group_2', 'name': 'New Group (Duplicate)'}
```

**archive**  
Archives this group.  
Returns: [moncli.entities.Group](#group)

*Example*
```
>>> archived_group = group.archive('id', 'name', 'archived')
>>> archived_group
{'id': 'group_1', 'name': 'New Group', 'archived': True}
```

**delete**  
Delete this group.  
Returns: [moncli.entities.Group](#group)

*Example*
```
>>> deleted_group = group.delete('id', 'name', 'deleted')
>>> archived_group
{'id': 'group_1', 'name': 'New Group', 'deleted': True}
```

**add_item**  
Add item to this group.  
Returns: [moncli.entities.Item](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|item_name|str|The new item's name.|
|column_values (Optional)|json|The column values of the new item.|

*Example*
```
>>> item_name = 'New Item 1'
>>> item = group.add_item(item_name, 'id', 'name')
>>> item
{'id': 1234567', 'name': 'New Item 1}
```

**get_items**  
Get items from this group.  
Returns: [list[moncli.entities.Item]](#item)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit (Optional)|int|Number of items to get; the default is 25.|
|page (Optional)|int|Page number to get, starting at 1.|
|ids (Optional)|list[str]|A list of items unique identifiers.|
|newest_first (Optional)|bool|Get the recently created items at the top of the list.|

*Example*
```
>>> items = group.get_items('id', 'name')
>>> items
[{'id': '1234567', 'name': 'New Item 1'}]
```

## Item ##
This section contains all properties and methods contained within the __Board__ object.  

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|assets|[list[moncli.entities.Asset]](#file)|The item's assets/files.|
|board|[moncli.entities.Board](#board)|The board that contains this item.|
|column_values|[list[moncli.entities.ColumnValue]](#column-values)|The item's column values.|
|created_at|str|The item's create date.|
|creator|[moncli.entities.User](#user)|The item's creator.|
|creator_id|str|The item's unique identifier.|
|group|[moncli.entities.Group](#group)|The group that contains this item.|
|id|str|The item's unique identifier.|
|name|str|The item's name.|
|state|str|The board's state (all / active / archived / deleted)|
|subscriber|[moncli.entities.User](#user)|The pulse's subscribers.|
|updated_at|str|The item's last update date.|
|updates|[moncli.entities.Update](#update)|The item's updates.|

### Methods ###

**add_file**  
Add a file to a column value.  
Returns: [moncli.entities.Asset](#file)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|file_column|[moncli.entities.FileValue](#column-values)|The file column value to be updated.|
|file_path|str|The file path.|

*Example*
```
>>> file_column = item.get_column_value(id='file_column_1')
>>> file_path = '/users/test/monday_files/test.jpg'
>>> asset = item.add_file(file_column, file_path, 'id', 'name', 'url')
>>> asset
{'id': '1234567890', 'name': 'test.jpg', 'url': 'https://test.monday.com/files/test.jpg'}
```

**get_files**  
Retrieves the file assets for the login user's account.  
Returns: [list[moncli.entities.Asset]](#file)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|column_ids (optional)|list[str]|A list of column IDs from which to retrieve file assets.|

*Example*
```
>>> assets = item.get_files('id', 'name', 'url')
>>> assets
[{'id': '1234567890', 'name': 'test.jpg', 'url': 'https://test.monday.com/files/test.jpg'}]
```

**remove_files**  
Removes files from a column value.  
Returns: [list[moncli.entities.Asset]](#file)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|file_column|moncli.entities.FileValue|The file column value to be updated.|

*Example*
```
>>> file_column = item.get_column_value(id='file_column_1')
>>> item = item.remove_files(file_column, 'id', 'name')
>>> item
{'id': '1234567', 'name': 'New Item 1'}
```

**get_board**  
Get the board that contains this item.  
Returns: [moncli.entities.Board](#board)  

*Example*
```
>>> board = item.get_board('id', 'name')
>>> board
{'id': '12345', 'name': 'New Public Board'}
```

**get_creator**  
Get the item's creator.  
Returns: [moncli.entities.User](#user)  

*Example*
```
>>> creator = item.get_creator('id', 'name')
>>> creator
{'id': '1234', 'name': 'Test User'}
```

**get_column_values**  
Get the item's column values.  
Returns: [list[moncli.entities.ColumnValue]](#column-values)  

*Example*
```
>>> column_values = item.get_column_values('id', 'title')
>>> column_values
[{'id': 'text_column_1', 'title': 'New Text Column'}]
```

**get_column_value**  
Get an item's column value by ID or title.  
Returns: [moncli.entities.ColumnValue](#column-values)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|id|str|The column's unique identifier. NOTE: This parameter is mutually exclusive and cannot be used with 'title'.|
|title|str|The column's title. NOTE: This parameter is mutually exclusive and cannot be used with 'id'.|

*Example*
```
>>> # Get column value by id.
>>> column_id = 'text_column_1'
>>> column_value = item.get_column_value(id=column_id)
>>> column_value
{'id': 'text_column_1', 'title': 'New Text Column'}
>>> # Get column value by title.
>>> column_title = 'New Text Column'
>>> column_value = item.get_column_value(title=column_title)
>>> column_value
{'id': 'text_column_1', 'title': 'New Text Column'}
```

**change_column_value**  
Change an item's column value.  
Returns: [moncli.entities.Item](#item)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|column_value|[moncli.entities.ColumnValue](#column-values)|The column value to update.|

*Example*
```
>>> # Get and update column value before changing it.
>>> column_value = item.get_column_value(id='text_column_1')
>>> column_value.text = 'Updated Text'
>>> item.change_column_value(column_value)
```

**change_multiple_column_values**  
Change the item's column values.  
Returns: [moncli.entities.Item](#item)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|column_values|[list[moncli.entities.ColumnValue]](#column-values) / dict|The column value to update. NOTE: This value can either be a list of moncli.entities.ColumnValue objects or a formatted dictionary.|

*Example*
```
>>> # Get and update column value before changing it.
>>> column_value = item.get_column_value(id='text_column_1')
>>> column_value.text = 'Updated Text'
>>> # Update column value as ColumnValue list.
>>> item.change_multiple_column_values([column_value])
>>> # Update column value as dict.
>>> item.change_multiple_column_values({'text': 'Updated Text'})
```

**create_subitem**  
Create subitem.   
Returns: [moncli.entities.Item](#item)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|item_name|str|The new item's name.|
|column_values (Optional)|json|The column values of the new item.|

*Example*
```
>>> item_name = 'New Subitem'
>>> subitem = item.create_subitem(item_name, 'id', 'name', 'board.name')
>>> subitem
{'id': '1234568', 'name': 'New Subitem', 'board': {'name': 'Some monday.com-generated Board'}}
```

**move_to_group**  
Move item to a different group.  
Returns: [moncli.entities.Item](#item)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|group_id|str|The group's unique identifier.|

*Example*
```
>>> group_id = 'group_2'
>>> item = item.move_to_group(group_id, 'id', 'group.id', 'group.name')
>>> item
{'id': '1234567', 'group':{'id': 'group_2', 'name': New Group 2'}}
```

**archive**  
Archive this item.  
Returns: [moncli.entities.Item](#item)  

*Example*
```
>>> item = item.archive('id', 'state')
>>> item
{'id': '1234567', 'state': 'archived'}
```

**delete**  
Delete this item.  
Returns: [moncli.entities.Item](#item)  

*Example*
```
>>> item = item.delete('id', 'state')
>>> item
{'id': '1234567', 'state': 'deleted'}
```

**duplicate**  
Duplicate this item.  
Returns: [moncli.entities.Item](#item)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|with_updates (Optional)|bool|Duplicate with the item's updates.|

*Example*
```
>>> duplicate = item.duplicate('id', 'name')
>>> duplicate
{'id': '1234568','name': 'New Item 2'}
```

**add_update**  
Create a new update for this item.  
Returns: [moncli.entities.Update](#update)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|body|str|The update text.|
|parent_id (Optional)|str|The parent post identifier.|

*Example*
```
>>> body = 'Hello, World!'
>>> update = item.add_update(body, 'id', 'text_body')
>>> update
{'id': '123456781', 'text_body': 'Hello, World!'}
```

**get_updates**  
Get updates for this item.  
Returns: [moncli.entities.Update](#update)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit (Optional)|int|Number of updates to get; the default is 25.|
|page (Optional)|int|Page number to get, starting at 1.|

*Example*
```
>>> updates = item.get_updates()
>>> updates 
[{'id': '123456781', 'text_body': 'Hello, World!'}]
```

**delete_update**   
Delete item update.  
Returns: [moncli.entities.Update](#update)  

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|update_id|str|The update's unique identifier.|       

*Example*
```
>>> update_id = '123456781'
>>> item.delete_update(update_id)
```

**clear_updates**  
Clear all updates for item.
Returns: [moncli.entities.Item](#item)  

*Example*
```
>>> item = item.clear_updates('id', 'updates.id')
>>> item
{'id': '123456781', 'updates': []}
```

**get_activity_logs**  
Get the items event logs.   
Returns: [list[moncli.entities.ActivityLog]](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|limit|int|Number of items to get, the default is 25.|
|page|int|Page number to get, starting at 1.|
|user_ids|list[str]|User ids to filter.|
|column_ids|list[str]|Column ids to filter.|
|group_ids|list[str]|Group ids to filter.|
|item_ids|list[str]|Item id to filter|
|from|str|From timespamp (ISO8601).|
|to|str|To timespamp (ISO8601).|

*Example*
```
>>> activity_logs = item.get_activity_logs('id','data')
>>> activity_logs
[{'id': '12345678901', 'data': 'INSERT_COLIMN_DATA_HERE'}]
```

## Update ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|assets|[list[moncli.entities.Asset]](#file)|The update's assets/files.|
|body|str|The update's html formatted body.|
|created_at|str|The update's creation date.|
|creator|moncli.entities.User|The update's creator.|
|creator_id|str|The unique identifier of the update creator.|
|id|str|The update's unique identifier.|
|item_id|str|The update's item ID.|
|replies|[list[moncli.entities.Reply]](#other-entities)|The update's replies.|
|text_body|str|The update's text body.|
|updated_at|str|The update's last edit date.|


### Methods ###

**get_creator**  
Get the update's creator.  
Returns: [moncli.entities.User](#user)      

*Example*
```
>>> creator = update.get_creator('id', 'name')
>>> creator
{'id': '1234', 'name': 'Test User'}
```

**add_reply**  
Add reply to update.  
Returns: [moncli.entities.Reply](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------| 
|body|str|The text body of the reply.|

*Example*
```
>>> body = 'Right back at you!'
>>> update.add_reply(body)
```

**get_replies**  
Add reply to update.  
Returns: [moncli.entities.Reply](#other-entities)   

*Example*
```
>>> replies = update.get_replies('text_body')
>>> replies
{'text_body': 'Right back at you!'}
```

**add_file**  
Add a file to update.  
Returns: [moncli.entities.Reply](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|   
|file_path|str|The path to the file to upload.|  

*Example*
```
>>> file_path = '/users/test/monday_files/test.jpg'
>>> asset = update.add_file(file_path, 'name', 'url')
>>> asset
{'name': 'test.jpg', 'url': 'https://test.monday.com/files/test.jpg'}
```

**get_files**  
Get update's files.    
Returns: [moncli.entities.Reply](#other-entities)
    
*Example*
```
>>> assets = update.get_files('name', 'url')
>>> assets
[{'name': 'test.jpg', 'url': 'https://test.monday.com/files/test.jpg'}]
```

**delete**
Delete an update.  
Returns: [moncli.entities.Reply](#other-entities)  

*Example*
```
>>> update.delete()
```

## File ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|id|str|The file's unique identifier.|
|created_at|str|The file's creation date.|
|file_extension|str|The file's extension.|
|file_size|int|The file's size in bytes.|
|name|str|The file's name.|
|public_url|str|Public url to the asset, valid for 1 hour.|
|uploaded_by|moncli.entities.User|The user who uploaded the file.|
|url|str|The file url.|
|url_thumbnail|str|Url to view the asset in thumbnail mode. Only available for images.|

### Methods ###

**get_uploaded_by_user**  
Get the user who uploaded the file.  
Returns: [moncli.entities.User](#user)  

*Example*
```
>>> uploaded_by = asset.get_uploaded_by_user('id', 'name')
>>> uploaded_by
{'id': '1234', 'name': 'Test User'}
```

## User ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|account|moncli.entities.user.Account|The user's account.|
|birthday|str|The user's birthday.|
|country_code|str|The user's country code.|
|created_at|str|The user's creation date.|
|email|str|The user's email.|
|enabled|bool|Is the user enabled or not.|
|id|str|The user's unique identifier.|
|is_guest|bool|Is the user a guest or not.|
|is_pending|bool|Is the user a pending user.|
|is_view_only|bool|Is the user a view only user or not.|
|join_date|str|The date the user joined the account.|
|location|str|The user' location.|
|mobile_phone|str|The user's mobile phone number.|
|name|str|The user's name.|
|phone|str|The user's phone number.|
|photo_original|str|The user's photo in the original size.|
|photo_small|str|The user's photo in small size (150x150).|
|photo_thumb|str|The user's photo in thumbnail size (100x100).|
|photo_thumb_small|str|The user's photo in small thumbnail size (50x50).|
|photo_tiny|str|The user's photo in tiny size (30x30).|
|teams|[list[moncli.entities.user.Team]](#other-entities)|The teams the user is a member in.|
|time_zone_identifier|str|The user's time zone identifier.|
|title|str|The user's title.|
|url|str|The user's profile url.|
|utc_hours_diff|int|The user's UTC hours difference.|

### Methods ###

**get_account**  
Get the user's account.   
Returns: [moncli.entities.Account](#other-entities)

*Example*
```
>>> account = user.get_account('id', 'name')
>>> account
{'id': '1', 'name': 'Test Account'}
```

**get_teams**  
Get teams the user is a member in.  
Returns: [list[moncli.entities.Team]](#other-entities)

*Example*
```
>>> teams = user.get_teams('id', 'name')
>>> teams
[{'id': '12', 'name': 'Test Team'}]
```

**send_notification**  
Create a new notification.  
Returns: [moncli.entities.Notification](#other-entities)

*Parameters*
| Name | Type | Description | 
|---|:------------:|:----------------|
|text|str|The notification text.|
|target_id|str|The target's unique identifier.|
|target_type|moncli.enums.NotificationTargetType|The target's type (Project / Post)|
|payload (Optional)|json|The notification payload.|

*Example*
```
>>> from moncli.enums import NotificationTargetType
>>>
>>> text = 'Hello, World!'
>>> target_id = '1235'
>>> notification_type = NotificationTargetType.Post
>>> notification = user.create_notification(text, target_id, notification_type, 'id', 'text')
>>> notification
{'id': '123456789', 'text': 'Hello, World!'}
```

# Other Entities #
This section contains property and method information of other entities available using moncli.

## Board View ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|account_id|str|The user's payment account.|
|created_at|str|The activity log's created date.|
|data|str|The item's column values in string form.|
|entity|str|The monday.com object being updated.|
|id|str|The activity log's unique identifier.|
|user_id|str|The user who performed the change.|

## Column ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|archived|bool|Is the column archived or not.|
|id|str|The column's unique identifier.|
|pos|str|The column's position in the board.|
|settings_str|strThe column's settings in a string form.|
|settings|moncli.entities.Settings|The settings in entity form (status / dropdown)|
|title|str|The column's title.|
|type|str|The column's type.|
|column_type|[moncli.entities.ColumnType](#column-types)|The column's type as an enum.|
|width|int|The column's width.|

## Notification ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|id|str|The notification`s unique identifier.|
|text|str|the notification text.|

## Tag ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|color|str|The tag's color.|
|id|str|The tag's unique identifier.|
|name|str|The tag's name.|

## Webhook ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|board_id|str|The webhook's board id.|
|id|str|The webhook's unique identifier.|
|is_active|bool|If the webhook is still active.|

## Workspace ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|description|str|The workspace's description.|
|id|int|The workspace`s unique identifier.|
|kind|moncli.enums.WorkspaceKind|The workspace's kind (open / closed).|
|name|str|The workspace's name.|

## Account ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|first_day_of_the_week|str|The first day of the week for the account (sunday / monday).|
|id|int|The account's unique identifier.|
|logo|str|The account's logo.|
|name|str|The account's name.|
|plan|moncli.entities.Plan|The account's payment plan.|
|show_timeline_weekends|bool`|Show weekends in timeline.|
|slug|str|The account's slug.|

### Methods ###

**get_plan**  
Get the account's payment plan.  
Returns: [list[moncli.entities.Plan]](#other-entities)  

*Example*
```
>>> plan = team.get_plan('version')
>>> plan
{'version': '33'}
```

## Team ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|id|int|The team's unique identifier.|
|name|str|The team's name.|
|picture_url|str|The team's picture url.|
|users|[moncli.entities.User](#user)|The users in the team.|

### Methods ###

**get_users**  
Get the users in the team.  
Returns: [list[moncli.entities.User]](#user)  

*Example*
```
>>> users = team.get_users('id', 'name')
>>> users
[{'id': '1234', 'name': 'Test User}]
```

## Plan ##

### Properties ###
|Name        |Type               |Description                 |
|------------|:-----------------:|:---------------------------|
|max_users|int|The maximum users allowed in the plan.|
|period|str|The plan's time period.
|tier|str|The plan's tier.|
|version|int|The plan's version.|


## Column Values ##
A __ColumnValue__ can also be created without the need for __Board__ or __Item__ objects using the universal _create_column_value_ function.  This method creates a __ColumnValue__ object from the input column _id_ and _column_type_ parameter (with an optional _title_ field). The __ColumnType__ enum is used for the _column_type_ parameter, and all values available for column value updating are listed below:
* name
* text
* long_text
* numbers
* status
* dropdown
* people
* world_clock
* country
* email
* phone
* link
* date
* timeline
* tags
* hour
* week
* checkbox
* rating
* file

An example for creating a new __ColumnValue__ object is shown below. Please note that the board column IDs must be pre-defined and know prior to using this function effectively.
```
>>> # Empty checkbox column value
>>> from moncli import create_column_value
>>>
>>> new_empty_checkbox_column_value = create_column_value(id='checkbox_column_1', column_type=ColumnType.checkbox)
>>> new_empty_checkbox_column.checked
False
```

__ColumnValue__ objects are also created from __Board__ objects using the _get_column_value_ method.  This method is especially useful when working with column values for columns with settings, status and dropdown columns in particular.  The method above is used as shown below.
```
>>> # Get status column by column id.
>>> status_column_id = 'status'
>>> status = board.get_column_value('status')
>>> 
>>> # Or get status column by title.
>>> status = board.get_column_value(title='Status')
>>>
>>> status.label = 'Done'
```

For more information regarding the __ColumnValue__ object type specific properties, please refer to the __Available column value types__ section below.


### Using column values ###
With access to the __ColumnValue__ objects, item column values can effectively be updated using the API.  Updating the value of the __ColumnValue__ object is simply a matter of updating the value of the type-specific property for the column value to be updated.  An example with a simple text column and more complex week column are shown below.
```
>>> # Updating the value of a text column
>>> text_column_value.text = 'Changed text here'
>>>
>>> # Updating the value of a week column
>>> week_column_value.start_date = '2019-09-09'
>>> week_column_value.end_date = '2019-09-15'
```

For more information regarding the __ColumnValue__ object type specific properties, please refer to the __Available column value types__ section below.


### Available column value types ###
Column values are managed by various __ColumnValue__ subclasses that contain the type-specific properties for updating. This section provides an exhastive list of all available __ColumnValue__ subclasses that can be used for updating item column values.


#### TextValue ####
ColumnType: text

Properties:
* _text_ (str) - input text string


#### NumberValue ####
ColumnType: numbers

Properties:
* _number_ (int/flt) - input integer or float value


#### StatusValue ####
ColumnType: status

Properties:
* _index_ (int) - the index of the status (required)
* _label_ (str) - the label of the status (required)

Methods:
* _change_status_by_index_ (index: int) - changes the status by the index according to status settings
* _change_status_by_label_ (label: str) - changes the status by the label according to status settings


#### DropdownValue ####
ColumnType: dropdown

Properties:
* _ids_ (list\[int\]) - dropdown value IDs (required)
* _labels_ (list\[str\]) - dropdown value labels (required)

Notes:
* _ids_ and _labels_ properties are mutually exclusive and cannot both be used


#### PeopleColumn ####
ColumnType: people

Properties:
* _persons_and_teams_ (list) - people by ID and kind ('person' or 'team')

Methods:
* _add_people_ (id: int, kind: __PeopleKind__) - adds a person or team
* _remove_people_ (id: int) - removes a person or team by id

Usage:
```
>>> # Adding people
>>> people_value.add_people(id=12345, kind=PeopleKind.person)
>>> people_value.add_people(id=67890, kind=PeopleKind.team)
>>> people_value.persons_and_teams
[{'id': 12345, 'kind': 'person'}, {'id': 67890, 'kind': 'team'}]
>>>
>>> # Removing people
>>> people_value.remove_people(id=67890)
>>> people_value.persons_and_teams 
[{'id': 12345, 'kind': 'person'}]
```


#### Timezone Value ####
ColumnType: world_clock

Properties:
* _timezone_ (str) - input tz database timezone string

Notes:
* Full list of timezones avaliable [here](https://momentjs.com/timezone/).


#### CountryValue ####
ColumnType: country

Properties:
* _country_code_ (str) - input ISO2 country code string (required)
* _country_name_ (str) - input country name (required)

Notes:
* Full list of _country_code_ and _country_name_ values available [here](http://country.io/names.json)


#### EmailValue ####
ColumnType: country

Properties:
* _email_ (str) - input email address (required)
* _text_ (str, default: _email_) - input email value label


#### PhoneValue ####
ColumnType: phone

Properties:
* _phone_ (str) - input phone number string as only digits (required)
* _country_short_name_ (str) - input ISO2 country code string (required)

Notes:
* Full list of _country_code_ and _country_name_ values available [here](http://country.io/names.json)


#### LinkValue ####
ColumnType: link

Properties:
* _url_ (str) - input link url (required)
* _text_ (str, default: _url_) - input link value label


#### DateValue ####
ColumnType: date

Properties:
* _date_ (str) - UTC date string in 'YYYY-MM-dd' format (required)
* _time_ (str, default: '00:00:00') - UTC time string in hh:mm:ss format


#### TimelineValue ####
ColumnType: timeline

Properties:
* _from_date_ (str) - UTC date string in 'YYYY-MM-dd' format (required)
* _to_date_ (str) - UTC date string in 'YYYY-MM-dd' format (required)


#### TagsValue ####
ColumnType: tags

Properties:
* _tag_ids_ (list\[int\]) - tag IDs


#### HourValue ####
ColumnType: hour

Properties:
* _hour_ (int) - hour value
* _minute_ (int, default: 0) - minute value


#### WeekValue ####
ColumnType: week

Properties:
* _start_date_ (str) - UTC date string in 'YYYY-MM-dd' format (required)
* _end_date_ (str) - UTC date string in 'YYYY-MM-dd' format (required)


#### CheckboxColumn ####
ColumnType: checkbox

Properties:
* _checked_ (bool) - is checked


#### RatingValue ####
ColumnType: rating

Properties:
* _rating_ (int) - rating value (0-5)

## Using the API v2 Client ##
(Coming soon...)

## Creating Custom GraphQL Queries ##
(Coming soon...)

## Additional Questions/Feature Requests:
Please feel free to log an issue or request a new feature by submitting a new issue or reaching out to me at andrew.shatz@trix.solutions. Thank you and happy coding!!!
