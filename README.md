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


### Getting boards ###


### Archiving a board ###


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
