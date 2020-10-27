# moncli
A Python Client and CLI tool for Monday.com

### Table of Contents ###
* [Setup](#setup). 
* [Getting Started...](#getting-started)  
   * [Introducing the MondayClient](#introducing-the-mondayclient)
   * [Managing Boards](#managing-boards)
   * [Working with Columns, Groups, and Items](#working-with-groups-and-items)
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
* [Working with Column Values](#working-with-column-values)  
* [Using the API v2 Client](#using-the-api-v2-client)  
* [Creating Custom GraphQL Queries](#creating-custom-graphql-queries)  
  

## Setup ##
To add the moncli package to your project, simply execute the following command within your Python 3 environment using pip.  Please note that this package is currently available for Python 3
```
$ pip3 install moncli
```
   
## Getting Started... ##

### Introducing the MondayClient ###
Getting started with the moncli Python package is simple.  To begin, create a __MondayClient__ istance using the following code below:
```
>>> from moncli import MondayClient
>>> client = MondayClient(user_name='user@email.com', api_key_v1='api_key_v1', api_key_v2='api_key_v2')
```
The __MondayClient__ object is the entry point for all client activities and includes functionality for board, item, tag, and user management.

The _api_key_v1_ and _api_key_v2_ parameters represent the user/account monday.com API access keys and can be found by navigating to __https://<your_instance_name>.monday.com/admin/integrations/api__ and copying both the API v1 (personal or company) and API v2 keys.

Additional information regarding __MondayClient__ properties/methods can be found in the [MondayClient](#mondayclient) section below.

### Managing Boards ###
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

### Working with Columns, Groups, and Items ###
Columns contain metadata that pertains to the data types available to current and future board items. Board columns are represented by the __Column__ object.  A new column is created and returned as a __Column__  

Groups serve as collections of items for a board.  Once created by the __Board__ object using the _get_groups_ method, the __Group__ object gives users various methods for modification and item management as discussed in the following section.

### Changing Column Values ###

### Posting Updates ###

### Uploading Files ###

## Moncli Entities ##
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
[{'id': '1234567', 'text_body': 'Hello World'}]
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
{'id': '1234567', 'text_body': 'Hello World'}
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
>>> text = 'Hello World'
>>> user_id = '1234'
>>> target_id = '1235'
>>> notification_type = NotificationTargetType.Post
>>> notification = client.create_notification(text, user_id, target_id, notification_type, 'id', 'text')
>>> notification
{'id': '123456789', 'text': 'Hello World'}
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

#### Methods ####

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
|id|str|The column's unique identifier.|
|title|str|The column's title.|
|settings (Optional)|moncli.entities.objects.StatusSettings/moncli.entities.objects.DropdownSettings(#other-entities)|Column settings required for retrieving a status or dropdown column.|

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
            
#### Methods ####

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


### Update ###

### File ###

### User ###

### Account ###

### Other Entities ###

## Working with Column Values ##

## Using the API v2 Client ##
(Coming soon...)

## Creating Custom GraphQL Queries ##
(Coming soon...)


### Getting items ###
Items can be retrieved with the __MondayClient__ object using the following command. 
```
>>> items = client.get_items(limit=25, newest_first=True)
```
This example will retrieve the 25 most recently created items.  Optional parameters to use when querying __Item__ objects include:
* limit (int) - the maximum number of items per page to return
* page (int) - the page index starting at 1
* ids (list[int]) - the IDs of the items to return
* newest_first (bool) - indicates whether to sort by created date descending



## Using Boards ##
Boards are cornerstones for any Monday.com setup, and __Board__ objects are no exception containing functionality for general data management with columns, groups, and items.  The next sections below will provide an overview of the full board functionality available.


### Adding a column ###
To add a column to a board, simply execute the _add_column_ method on the __Board__ object as shown below.  
```
>>> from moncli import ColumnType
>>>
>>> new_column = board.add_column(title='New Text Column', column_type=ColumnType.text)
```
The __Column__ object returned contains the _id_, _name_, and _type_ fields of the newly created column.


### Adding a group ###
A group can be added to a board using the _add_group_ method on the __Board__ object as shown below.
```
>>> new_group = board.add_group(group_name='New Group')
```
The __Group__ object returned contains the _id_ and _title_ fields of the newly created group.


### Adding an item ###
A new item can be added to the default group of a board using the _add_item_ method on the  __Board__ object as shown below.
```
>>> new_item = board.add_item(item_name='New Item')
```
The __Item__ object returned contains the _id_ and _name_ fields of the newly created item. 

An __Item__ object can be created with column values using the optional _column_values_ parameter.  Values for this parameter can be input as a dictionary in which each key represents the ID of the column to update and the value represents the value to add.  
```
>>> column_values = {'text_column_1': 'New Text Value'}
>>> new_item_with_values = board.add_item(item_name='New Item With Text Value', column_values=column_values)
```

This method also accepts a list of __ColumnValue__ objects for adding column values to new items.  
```
>>> from moncli import create_column_value, ColumnType
>>>
>>> column_value = create_column_value(id='text_column_1', column_type=ColumnType.text, text='New Text Value created using TextValue object')
>>>
>>> new_item_with_values_2 = board.add_item(item_name='New Item Using Column Values', column_values=[column_value])
```
More information about the __ColumnValue__ object and its various types can be found futher down in the Readme document. Information on how to change values for different field types can be found [here](https://monday.com/developers/v2#column-values-section)


### Getting columns, groups, and items ###
To retrieve all columns, groups, and items associated with a __Board__ object, simply execute the following commands respectively.
```
>>> columns = board.get_columns()
>>>
>>> groups = board.get_groups()
>>>
>>> items = board.get_items()
```

### Getting items by column value ###
The __Board__ object can also retrieve contained items by column value using the _get_items_by_column_values_ method as shown below.
```
>>> from moncli import create_column_value, ColumnType
>>>
>>> status_value = create_column_value(id='status_column_1', column_type=ColumnType.status, label='Done')
>>> board.get_items_by_column_values(column_value=status_value)
```
The method returns a list of __Item__ objects containing the same fields as mentioned in the _get_items_ method above.

### Getting a column value ###
The __Board__ object can also return a new __ColumnValue__ object with an empty or a user-populated value using the _get_column_value_ method as shown below
```
>>> # Get empty column value from board
>>> empty_column = board.get_column_value(id='text_column_01')
>>>
>>> # Get column value from board with user-populated data
>>> not_empty_column = board.get_column_value(title='Text Column 01', value='Za Waarudo!')
```

## Working with Groups ##
Groups serve as collections of items for a board.  Once created by the __Board__ object using the _get_groups_ method, the __Group__ object gives users various methods for modification and item management as discussed in the following section.

### Duplicating a group ###
The __Group__ object can duplicate an existing group using the _duplicate_ method as shown below.
```
>>> duplicate_group = group.duplicate(group_title='New Duplicate Group', add_to_top=True)
```
The method above creates a new group and adds it to the first group position on the associated board and returns a __Group__ object with the _id_ and _title_ fields of the duplicated group.


### Archiving a group ###
The __Group__ object can also archive a group using the _archive_ method as shown below.
```
>>> archived_group = group.archive()
```

This method returns a __Group__ object with the _id_, _title_, and _archived_ fields of the archived group.


### Delete the group ###
The __Group__ object can also delete the corresponding group using the _delete_ method as shown below.
```
>>> deleted_group = group.delete()
```
This method returns a __Group__ object with the _id_, _title_, and _archived_ fields of the deleted group.

### Adding an item to a board ###
In addition to modifying the group, the __Group__ object can both add and retrieve items.  Items can be added to groups using the _add_item_ method on the __Group__ object as shown below.
```
>>> group.add_item(item_name='New Item in Group')
```
Similar to the _add_item_ method on the __Board__ object, this method is also capable of adding column values to newly created items.  Please refer to the _add_item_ method on the __Board__ object for a detailed example.


### Getting group items ###
Much like __Board__ objects, __Group__ objects can return a list of contained items using the following command.
```
>>> items = group.get_items()
```
Please note that only items associated to the group will be returned.  The method returns a list of __Item__ objects containing the same return fields as mentioned in the __Board__ _get_items_ method.


## Working with Items ##
The __Item__ object gives users access to functionality for managing items within and between groups, updating column values, and creating updates. The full list of of functionality is described in detail in the following section.

### Getting column values ###
Column values for an item can be retrieved from the __Item__ object using the _get_column_values_ method as shown below.
```
>>> column_values = item.get_column_values()
```
This method returns a list of __ColumnValue__ objects containing the current state of the item's column values.  These objects can be used for retrieving items by column value and updating one or many column values for an item.  Please consult the section on the __ColumnValue__ object below for more information.

### Getting a column value ###
In addition to retrieving all column values for an item, the __Item__ object also contains the _get_column_value_ method which can retrieve a single column value as a __ColumnValue__ object by either id or name.  Examples of both are demonstrated below.
```
>>> # Get column value by ID
>>> column_value = item.get_column_value(id='text_column_1')
>>>
>>> # Get column value by name
>>> column_value = item.get_column_value(name='My Text Column')
```
Please note that the _get_column_value_ method can only accept either the id or name parameter and will raise an exception if either both or none of the parameters are used.


### Changing a column value ###
The __Item__ object can be used to update the value of a single column using the _change_column_value_ method.  This method can accept a __ColumnValue__ when performing an update as shown below.
```
>>> from moncli import create_column_value, ColumnType
>>>
>>> column_value = create_column_value(id='number_column_1', column_type=ColumnType.numbers, number=8675309)
>>> item = item.change_column_value(column_value=column_value)
```

The _change_column_value_ method can also update individual column values using raw data in the form of dictionaries.  However, the _column_id_ parameter is required in addition to the _column_value_ parameter.  For numeric and text types, the column value is a string, but for complex column types the value for the _column_value_ parameter is a dictionary.  Examples of both are shown below.
```
>>> # Updating a numeric column value
>>> item = item.change_column_value(id='number_column_1', column_value=str(8675309))
>>>
>>> # Updating a complex column value
>>> column_value = {'timezone': 'America/New_York'}
>>> item = item.change_column_value(id='world_clock_column_1', column_value=column_value)
```

The _create_column_value_ method returns an __Item__ object containing the _id_ and _name_ fields of the updated item.


### Updating multiple column values ###
In addition to updating a single column value, the __Item__ object can update multiple column values using the _change_multiple_column_values_ method.  This method accepts a list of __ColumnValue__ objects in the example demonstrated below.
```
>>> number_value = create_column_value(id='number_column_1', column_type=ColumnType.numbers, number=43770)
>>> timezone_value = create_column_value(id='world_clock_column_1', column_type=ColumnType.world_clock, timezone='America/Chicago')
>>>
>>> item = item.change_multiple_column_values(column_values=[number_value, timezone_value]
```

The _change_multiple_column_values_ method also accepts a dictionary type in which the keys represent the IDs of the columns to be updated and the values are the value to update as shown below.
```
>>> column_values = {'number_column_1': 43770, 'world_clock_column_1': {'timezone: 'America/Chicago'}}
>>>
>>> item = item.change_multiple_column_values(column_values=column_values)
```
This method returns a list of __Item__ objects with the _id_ and _name_ fields of the updated items.


### Moving an item between groups ###
Items can be moved from one group to another using the _move_to_group_ method on the __Item__ object as shown below.
```
>>> moved_item = item.move_to_group(group_id='other_group_1')
```
This method returns an __Item__ object containing the _id_ and _name_ fields of the moved item.


### Archiving an item ###
Items can be archived using the _archive_ method on the __Item__ object as shown below.
```
>>> archived_item = item.archive()
```
This method returns an __Item__ object containing the _id_ and _name_ fields of the archived item.


### Deleting an item ###
Items can be deleted using the _delete_ method on the __Item__ object as shown below.
```
>>> deleted_item = item.delete()
```
This method returns an __Item__ object containing the _id_ and _name_ fields of the deleted item.


### Adding an update ###
Updates can be added to items using the _add_update_ method on the __Item__ object as shown below.
```
>>> update = item.add_update(body='This is the body for an update')
```
This method creates an update for the item on behalf of the user that owns the API V2 token and returns an __Update__ object containing the _id_ and _body_ fields of the added update.


## Working with Users, Teams, and Accounts ##
### Get user account ###
The __Account__ object contains information pertaining to the Monday.com service subscription and can be retrieved from the __User__ object with the following command.
```
>>> account = user.get_account()
```
The __Account__ object also contains the payment plan information via the __Plan__ object and can be retrieved using the following command.
```
>>> plan = account.get_plan()
```

### Get user's teams ###
Any given user can be assigned to multiple different teams, and a list of these __Team__ objects can be retrieved from the __User__ object with the following command.
```
>>> teams = user.get_teams()
```

### Sending a notification ###
Similar to sending notifications from the __MondayClient__ object, the __User__ object can send notifications with the following command.
```
>>> from moncli import NotificationTargetType
>>>
>>> notification = user.send_notification(text='text', target_id='2345678', target_type=NotificationTargetType.Project)
```
Please consult the Monday.com API v2 guide [here](https://monday.com/developers/v2#mutations-section-notifications) regarding additional optional parameters and return fields.

### Getting users on a team ###
Similar to retrieving __Team__ objects from a __User__ object, __Team__ objects can also retrieve all containing users as __User__ objects with the following command.
```
>>> team_users = team.get_users()
```

## Working with Column Values ##
When adding or changing column values for new and existing items, the __ColumnValue__ object serves to simplify and streamline the process of mapping data to and from items in Monday.com.  Each __ColumnValue__ comes with an _id_ and _title_ that are intrinsic with any column value model.  Each column value type that can be updated corresponds with one of many subclasses of the __ColumnValue__ object containing additional properties that are unique for the given column data type.  

This section provides and overview retrieving, creating, and using available __ColumnValue__ object types.

### Retrieving column values ###
__ColumnValue__ objects can be retrieved from either __Board__ or __Item__ objects.  
A __ColumnValue__ with the mapped _id_ and _title_ fields but no value can be retrieved from a __Board__ object using the _get_column_value_ method as shown below.
```
>>> # Empty column values may be retrieved from boards by column id or title
>>> empty_column_value_by_id = board.get_column_value(id='text_column_1')
>>> empty_column_value_by_title = board.get_column_value(title='Address')
```

__Item__ objects on the other hand will return the value state of the column in addition to the _id_ and _title_ mapping fields.  However, if the current value of the item column value is empty, then the retrieved __ColumnValue__ object will also be empty.  
The _get_column_values_ method will return a list of all column values for the item. 
```
>>> column_values = item.get_column_values()
>>>
>>> # Assume column 1 is a text column with a value
>>> column_values[0].text
'Hello, world!'
>>>
>>> # Assume column 2 is a numbers column with no value
>>> column_values[1].number
>>>
```

Much like the __Board__ object, A single column value can be retrieved from __Item__ objects using the _get_column_value_ method using either the column _id_ or _title_ fields.
```
>>> # Column values may be retrieved from items by column id or title
>>> column_value_by_id = item.get_column_value(id='text_column_1')
>>> column_value_by_title = item.get_column_value(title='Salutation')
```


### Creating column values ###
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

An example for creating a new __ColumnValue__ object is shown below.  In addition to the _id_ and _column_type_ parameters, column values can be added to the __ColumnValue__ objects when using the type-specific __ColumnValue__ properties as a named argument. Please note that the board column IDs must be pre-defined and know prior to using this function effectively.
```
>>> # Empty checkbox column value
>>> from moncli import create_column_value
>>>
>>> new_empty_checkbox_column_value = create_column_value(id='checkbox_column_1', column_type=ColumnType.checkbox)
>>> new_empty_checkbox_column.checked
False
>>>
>>> # Checkbox column value with input value
>>> new_checkbox_column_value = create_column_value(id='checkbox_column_1', column_type=ColumnType.checkbox, checked=True)
>>> new_checkbox_column_value.checked
True
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


## Additional Questions/Feature Requests:
Please feel free to log an issue or request a new feature by submitting a new issue or reaching out to me at andrew.shatz@trix.solutions. Thank you and happy coding!!!
