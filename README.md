# moncli
A Python Client and CLI tool for Monday.com

## Setup ##
To install the moncli package, downlaod the source code from the __master__ branch and navigate to the _moncli_ directory containing the _setup.py_ script. 
```
$ cd \moncli
```
The package can then be installed onto your current Python 3 environment when running the following command.
```
$ python3 setup.py install
```


## Using the Monday.com client ##
The __MondayClient__ object is the entry point for all client activities and includes functionality for board, item, tag, and user management.  The following section will briefly overview what can be done with the __MondayClient__ object.

### Creating a Client ###
Before creating a new __MondayClient__, you will first need to retrieve your API v1 and v2 access keys by navigating to __https://<your_instance_name>.monday.com/admin/integrations/api__ and copying both the API v1 (personal or company) and API v2 keys.  

To create a new Monday.com client, simply run Python 3 and execute the following commands.
```
>>> import moncli
>>> client = MondayClient(username='user@email.com', api_key_v1='api_key_v1', api_key_v2='api_key_v2')
```
Please note that the __MondayClient__ object requires that the input 'username' matches the user declared on the API v2 token for authentication purposes.


### Creating a board ###
Boards can be created with the __MondayClient__ object using the following command.  The __\*argv__ parameter can be used to determine which fields on the new board to return.  In the example below, only the _id_ field of the __Board__ object is returned after creation.
```
>>> from moncli import BoardKind
>>>
>>> return_fields = ['id']
>>> new_board = client.create_board(board_name='new_public_board', board_kind=BoardKind.public, *return_fields)
```
Please consult the Monday.com API v2 documentation [here](https://monday.com/developers/v2) for additional imformation regarding the __Board__ object return fields.


### Getting boards ###
The following command will retrieve boards by name.  In addition, key-value parameters may be used to refine the search.  By default, the __MondayClient__ will return a list of boards containing only their _id_ and _name_ values.
```
>>> boards = client.get_boards(page=1, limit=50)
```
The following command above will return a list of at most 50 board objects.  The full list of queryable parameters for __Board__ objects includes:
* limit (int) - the maximum number of boards per page to return
* page (int) - the page index starting at 1
* ids (list[int]) - the IDs of boards to return
* board_kind (BoardKind) - the type of board to return (public, private, share)
* state (State) - the current state of the board (all, active, archived, deleted)
* newest_first (bool) - indicates whether to sort by created date descending

Once a list of boards has been retrieved, you can use the _id_ field to retrieve detailed board information for a particular board. This can be done using the command below. 
```
>>> retrieved_board = client.get_board(id=boards[0].id)
```

Additionally, if you already know the name of the board that you wish to retrieve, simply use the same command with the _name_ parameter instead containing the name of the board to retrieve.
```
>>> retrieved_board = client.get_board(name='some_board')
```
Please note that querying boards by name is not a built-in feature for Monday.com and may be less performant that searching for a board by ID.

It is also important to note that while it is possible to query data for board columns, groups, and items in addition, the client requires that additional queryies be made for the additional data respectively after the initial board query.  These additional queries will be covered in more detail in the [Using Boards](https://github.com/trix-solutions/moncli/blob/initial-documentation/README.md#using-boards) section below.


### Archiving a board ###
The following command will archive a board and will return only a __Board__ object with an _id_ property corresponding to the archived board.
```
>>> archived_board = client.archive_board(board_id=retrieved_board.id)
```


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


### Getting updates ###
Updates can be retrieved with the __MondayClient__ object using the following command.
```
>>> updates = client.get_updates(limit=10)
```
This example will retrieve the last 10 updates.  Optional parameters to use when querying __Update__ objects include:
* limit (int) - the maximum number of updates per page to return
* page (int) - the page index starting at 1


### Creating a notification ###
The __MondayClient__ object can be used to send notifications between users with the following command.
```
>>> from moncli import NotificationTargetType
>>>
>>> notification = client.create_notification(text='notification_text', user_id='1234567', target_id='2345678', target_type=NotificationTargetType.Post) 
```
Optional parameters to use when creating and sending a notification include:
* payload (json) - the notification payload


### Creating a new/retriving an existing tag ###
Creating a new/retrieving an existing tag can be done by the __MondayClient__ object using the following command.
```
>>> new_tag = client.get_or_create_tag(tag_name='new_tag')
```
Optional parameters available when running the above command include:
* board_id (str) - the ID of the private board using the tag (N/A for public boards)


### Getting tags ###
The __MondayClient__ can also retrieve __Tag__ objects using the following commannd
```
>>> tags = client.get_tags()
```
Optional parameters to use when retrieving __Tag__ objects include:
* ids (list[int]) - the IDs of the tags to return


### Getting users ###
Users can be retrieved from the __MondayClient__ object using the following command.
```
>>> from moncli import UserKind
>>> users = client.get_users(kind=UserKind.guests)
```
This example will retrieve the first 25 (default limit) guest users.  Optional parameters when querying __Users__ include:
* ids (list[int]) - the IDs of the users to return
* kind (UserKind) - the kind of users (all, non-guests, guests, pending) to return
* limit (int) - the maximum number of users per page to return
* newest_first (bool) - indicates whether to sort by created date descending


### Getting teams ###
Teams can be retrieved from the __MondayClient__ object using the following command.
```
>>> teams = client.get_teams(ids=[1234567,2345678])
```
This example will retrieve a list of __Team__ objects containing the input IDs.  Optional parameters when querying __Team__ objects include:
* ids (list[int]) - the IDs of the teams to return


### Getting... me ###
Finally, the __MondayClient__ can fetch the user associated with the API v2 token as a __User__ object using the following command.
```
>>> me = client.get_me()
```
This command is currently used by the __MondayClient__ to authorize the use of the API v2 token and can be put to very good use when sending notifications to other users from your own.


## Using Boards ##
Boards are cornerstones for any Monday.com setup, and __Board__ objects are no exception containing functionality for general data management with columns, groups, and items.  The next sections below will provide an overview of the full board functionality available.

### Creating a column ###
To create a column with a __Board__ object, simply execute the command below.  
```
>>> from moncli import ColumnType
>>>
>>> new_column = board.create_column(title='New Text Column', column_type=ColumnType.text)
```
The __Column__ object returned contains only contains data for the _id_ field by default, but data for additional fields may be returned using the __\*argv__ parameter at the end of the function.  Information on additional __Column__ fields can be found in the Monday.com API v2 documentation [here](https://monday.com/developers/v2)

### Changing one or multiple column values ###
The __Board__ object can also change a single column value for an item using the following command.
```
>>> updated_item = board.change_column_value(item_id='1234567', column_id='text1', value='Hello again, world!')
```

In addition to changing single column values, the __Board__ object can also change multiple column values for an item using the following command.
```
>>> column_values = {'text1'='Hello again, world!", 'date1'='1970-01-01'}
>>> updated_item = board.change_multiple_column_values(item_id='1234567', column_values=column_values)
```
Information on how to change values for different field types can be found [here](https://monday.com/developers/v2#column-values-section)
It is important to note that the __Item__ object returned contains only contains data for the _id_ field by default, but data for additional fields may be returned using the __\*argv__ parameter at the end of the function.  Information on additional __Item__ fields can be found [here](https://monday.com/developers/v2#queries-section-items)

### Getting columns, groups, and items ###
To retrieve all columns, groups, and items associated with a __Board__ object, simply execute the following commands respectively.
```
>>> columns = board.get_columns()
>>>
>>> groups = board.get_groups()
>>>
>>> items = board.get_items()
```

### Adding an item ###
A new item can be added to a __Board__ object using the following command
```
>>> new_item = board.add_item(item_name='New Item')
```
An __Item__ object can be created with column values using the optional __column_values__ parameter.  Information on how to change values for different field types can be found [here](https://monday.com/developers/v2#column-values-section)

## Working with Columns and Groups ##
### Getting group items ###
Similar to __Board__ objects, __Group__ objects can return a list of contained items using the following command.
```
>>> items = group.get_items()
```


## Working with Items ##
### Getting column values ###
To reduce the query complexity for retrieving __Item__ objects from the Monday.com API, the full list of column values for an item can be acquired using the following command.
```
>>> column_values = item.get_column_values()
```


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


## Customized Queries and Mutations ##
Coming soon...

## Additional Questions/Feature Requests:
Please feel free to log an issue or request a new feature by submitting a new issue or reaching out to me at andrew.shatz@trix.solutions. Thank you and happy coding!!!
