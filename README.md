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
### Creating a Client ###
Before creating a new __MondayClient__, you will first need to retrieve your API v1 and v2 access keys by navigating to __https://<your_instance_name>.monday.com/admin/integrations/api__ and copying both the API v1 (personal or company) and API v2 keys.  

To create a new Monday.com client, simply run Python 3 and execute the following commands.
```
$ import moncli
$ client = MondayClient('api_key_v1', 'api_key_v2', 'username')
```
Please note that the __MondayClient__ object requires that the input 'username' matches the user declared on the API v2 token for authentication purposes.

### Creating a board ###
Boards can be created with the __MondayClient__ object using the following command.  The __\*argv__ parameter can be used to determine which fields on the new board to return.  In the example below, only the _id_ field of the __Board__ object is returned after creation.
```
$ from moncli import BoardKind
$ new_board = client.create_board('new_public_board', BoardKind.public, 'id')
```
Please consult the Monday.com API v2 documentation at https://monday.com/developers/v2 for additional imformation regarding the __Board__ object return fields.

### Getting boards ###
The following command will retrieve boards by name.  In addition, key-value parameters may be used to refine the search.  By default, the __MondayClient__ will return a list of boards containing only their _id_ and _name_ values.
```
$ boards = client.get_boards(page=1, limit=50)
```
The following command above will return a list of at most 50 board objects.  The full list of queryable parameters for __Board__ objects includes:
* limit (int) - the maximum number of boards to return
* page (int) - the page index starting at 1
* ids (list[int]) - a list of board IDs to find and return
* board_kind (BoardKind) - the type of board to return (public, private, share)
* state (State) - the current state of the board (all, active, archived, deleted)
* newest_first (bool) - indicates whether to sort by created date descending

Once a list of boards has been retrieved, you can use the _id_ field to retrieve detailed board information for a particular board. This can be done using the command below. 
```
$ retrieved_board = client.get_board(id=boards[0].id)
```

Additionally, if you already know the name of the board that you wish to retrieve, simply use the same command with the _name_ parameter instead containing the name of the board to retrieve.
```
$ retrieved_board = client.get_board(name='some_board')
```
Please note that querying boards by name is not a built-in feature for Monday.com and may be less performant that searching for a board by ID.

### Archiving a board ###
The following command will archive a board and will return only a __Board__ object with an _id_ property corresponding to the archived board.
```
$ archived_board = client.archive_board(retrieved_board.id)
```

### Getting items ###


### Getting updates ###


### Creating a notification ###


### Creating a new/retriving an existing tag ###


### Getting tags ###


### Getting users ###


### Getting teams ###


### Getting... me ###



## Using Boards ##
### Creating a column ###


### Changing a column value ###


### Changing multiple column values ###


### Getting columns ###


### Getting groups ###


### Getting items ###


### Adding an item ###



## Working with Columns and Groups ##
### Getting group items ###



## Working with Items ##
### Getting column values ###



## Working with Users, Teams, and Accounts ##
### Get user account ###


### Get user's teams ###


### Sending a notification ###


### Getting users on a team ###


### Getting the account payment plan ###



## Additional Questions/Feature Requests:
Please feel free to log an issue or request a new feature by submitting a new issue or reaching out to me at andrew.shatz@trix.solutions. Thank you and happy coding!!!
