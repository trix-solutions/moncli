# moncli
A Python Client and CLI tool for Monday.com

### Table of Contents ###
* [Getting Started](#getting-started)
   * [Setup](#setup)  
   * [Configuring the Client](#configuring-the-client)
* [Using Moncli](#using-moncli)
   * [Functions, Return Fields, and Arguments](#functions-return-fields-and-arguments)
   * [Managing Boards](#managing-boards)
   * [Working with Columns, Groups, and Items](#working-with-columns-groups-and-items)
   * [Changing Column Values](#changing-column-values)
   * [Posting Updates](#posting-updates)
   * [Uploading Files](#uploading-files)  
   * [Monday Models and Types](#monday-models-and-types)
  
# Getting Started

## Setup
To add the moncli package to your project, simply execute the following command within your Python 3 environment using pip.  Please note that this package is only available for Python 3
```shell
$ pip3 install moncli
```

## Configuring the Client
Getting started with the moncli Python package is simple.  To begin, import the default __MondayClient__ instance and set the API key using the following code below:
```python
from moncli import client
client.api_key = api_key_v2
```

The API key can also be set globally using the following code.  Please note that this will be the preferred method for setting the API key moving forward. The former should only be used when needing access to multiple clients for different accounts.
```python
import moncli
moncli.api.api_key = api_key_v2
```

In addition, if you find that requests going to the monday.com API time out due to environmental issues, extend the timeout using the _connnection_timeout_ property as shown below:
```python
moncli.api.connection_timeout = 30
```

Please note that standard requests have a default timeout of 10 seconds while file upload requests have a default timeout of 5 minutes.

The __MondayClient__ object is the entry point for all client activities and includes functionality for board, item, tag, and user management.

The _api_key_v1_ and _api_key_v2_ parameters represent the user/account monday.com API access keys and can be found by navigating to __https://<your_instance_name>.monday.com/admin/integrations/api__ and copying both the API v1 (personal or company) and API v2 keys.

# Using Moncli

## Functions, Return Fields, and Arguments
Moncli uses Domain-driven Design (DDD) principles to provide an easy-to-use interface for monday.com API functionality.  Each of the respective elements of the monday.com domain (boards, groups, items, etc.) are encapsulated inside of entity classes that not only preserve the state of the monday.com object but also expose additional API functionality through the use of class methods.

Many methods have required input parameters, but all of them contain the capability of using both the arguments (args) and key-word arguments (kwargs) parameters for custom return field and argument values respectively.

For example, the following code retrieves an item from a board.
```python
board = client.get_boards(ids=[board_id])[0]
board_items = board.get_items()
```

If there is a need to reduce complexity, as the retrieval of items is truly only dependent upon the ID of the retrieved board, the code may be rewritten in the following way.
```python
# In this case, the ids input parameter is a key-word argument and thus follows the 'id' list argument.
board = client.get_boards('id', ids=[board_id])[0]
board.id # Returns board_id
board.name # Returns None, as it was not retrieved
board_items = board.get_items()
```

The rewritten code does provide greater improvements around complexity of the initial call, but the _get_items_ method call from the __Board__ instance only returns the default item fields that are simple native types (strings, ints, floats, datetimes, etc.) Moncli supports the use of nested return field values to address this issue as seen with the code below.
```python
board = client.get_boards('id', ids=[board_id])[0]
# Return items with just the id, name, and the id, title, and value for their respective column values
board_items = board.get_items('id', 'name', 'column_values.id', 'column_values.title', 'column_value.value')
```

While this method works, the sheer number of return input fields can become unwieldy rather quickly.  To address this, Moncli also supports a special list notation for input fields that allows users to input a list of fields to return at the leaf level using a single return field input.  This allows the code to be rewritten in the following way.
```python
board = client.get_boards('id', ids=[board_id])[0]
# Return items with just the id, name, and column value fields using list notation.
board_items = board.get_items('id', 'name', 'column_values.[id, title, value]')
```

This improves readability tremendously, however all fields may be needed, and for monday.com domain entities with many return fields, this too can get unwieldy.  Fortunately, Moncli also supports an all-fields notation for nested return types as shown with the rewritten code below.
```python
board = client.get_boards('id', ids=[board_id])[0]
# Return items with just the id, name, and all column value fields using all-fields notation.
board_items = board.get_items('id', 'name', 'column_values.[*]')
```

Using a combination of both the list and all-fields notation, the efficiency of the code can be greatly improved by condensing everything into a single method call from the __MondayClient__ instance. The code below demonstrates this.
```python
board_items = client.get_boards('id', 'items.[id, name]', 'items.column_values.[*]', ids=[board_id])[0].items
```

Finally, moncli supports the use of nested arguments.  Say that a list of items were needed from a particular group.  This can easily be done using nested arguments as demonstrated below.
```python
board_items = client.get_boards('id', 'items.[id, name]', 'items.column_values.[*]', ids=[board_id], groups={'ids': [group_id]})[0].items
```

Using a combination of return field and argument techniques, there is no shortage of custom querying available.  So long as an entity method has an _*args_ and/or a _**kwargs_ input value, it supports the use of the techniques demonstrated above.


## Managing Boards ##
Boards are cornerstones for any Monday.com setup, and __Board__ objects are no exception containing functionality for general data management with columns, groups, and items.  The next sections below will provide some general tools regarding __Board__ management.

New boards are created with the __MondayClient__ instance using the _create_board_ method as shown in the example below. 
```python
# Import Boardkind enum for parameter input.
from moncli import BoardKind

# Create a new public board
board_name = 'New Public Board'
board_kind = BoardKind.public
new_board = client.create_board(board_name, board_kind)
```  

Existing boards are also retrieved with the __MondayClient__ using the _get_boards_ method using the _ids_ keyword argument as shown below.
```
board_ids = ['12345']
retrieved_boards = client.get_boards(ids=[board_ids])
```

When looking to retrieve only a single board by either id or name, the _get_board_ method is also available on the __MondayClient__ instance using either the _id_ or _name_ keyword argument as shown below.  
```python
# Retrieve a board by ID.
board_id = '12345'
board_by_id = client.get_board(id=board_id)

# Retrieve a board by Name
board_name = 'Existing Public Board'
retrieved_board = client.get_board(name='board_name')
```

__PLEASE NOTE:__ Querying boards by name is not a built-in feature for Monday.com and may be less performant that searching for a board by ID.

Finally, boards are archived using the _archive_board_ method on the __MondayClient__ instance as shown below.
```python
board_id = '12345'
archived_board = client.archive_board(board_id)
```

## Working with Columns, Groups, and Items

### Adding and Getting Columns

Columns contain metadata that pertains to the data types available to current and future board items. Board columns are represented by the __Column__ object.  A new column is created from a __Board__ instance using the *add_column* method and returned as a __Column__ object as shown below.
```python
from moncli import ColumnType

new_column = board.add_column(title='New Text Column', column_type=ColumnType.text)
```

Columns are retrieved from a __Board__ instance using the *get_columns* method as shown below.
```python
columns = board.get_columns('id', 'title', 'type')
```

### Managing Groups

Groups contain lists of items within a board.  In moncli, these groups are realized as __Group__ objects are are retrieved from a __Board__ in the following way.
```python
groups = board.get_groups('id','name')
```

Groups are also created via a __Board__ instance, as shown below.
```python
group_name = 'New Group'
group = board.add_group(group_name, 'id', 'name')
```

Once created a group may be duplicated, archived or deleted in the following ways.
```python
# Duplicate a group.
duplicate_group = group.duplicate()

# Archive a group.
archived_group = group.archive()

# Delete a group.
deleted_group = group.delete()
```

### Using Items

Items in monday.com represent individual records containing column value data.  These items exist inside of the various board groups.  Items are created by either a __Board__ or __Group__ instance as shown below.  Please note that when creating items from a __Board__ instance, the item is placed into the topmost group if the *group_id* parameter is not specified.
```python
item_name = 'New Item 1'

# Add item via board.
group_id = 'group_1'
item = board.add_item(item_name, group_id=group_id)

# Add item via group.
item = group.add_item(item_name)
```

An __Item__ object can be created with column values using the optional *column_values* parameter.  Values for this parameter can be input as a dictionary in which each key represents the ID of the column to update and the value represents the value to add.  
``` python
column_values = {'text_column_1': 'New Text Value'}
new_item_with_values = board.add_item(item_name='New Item With Text Value', column_values=column_values)
```

Items are also retrieved by either a __MondayClient__, __Board__, or __Group__ instance via the *get_items* methods.  It is important to note that the __Client__ instance has access to all items created within the account that are accessible to the user.  When using a __Board__ or a __Group__ instance, only items accessible to the user within the respective board or group are available to query.

Additionally, the column values may also be easily requested by using the _get_column_values_ parameters when retrieving items from any __MondayClient__, __Board__, or __Group__ instance.
```python
# Retrieve the item.
item = client.get_items(ids=[item_id_as_int_or_string])

# Retrieve the item with column values
item = client.get_items(ids=[item_id_as_int_or_string], get_column_values=True)
```

Once an __Item__ instance is retrieved, it can be moved between groups, duplicated, archived, or deleted as shown in the example below.

```python
# Move item to group.
item.move_to_group('group_2')

# Duplicate item with updates
item.duplicate(with_updates=True)

# Archive an item.
item.archive()
 
# Delete an item.
item.delete()
```

If the particular board contains a _Subitems_ column, then subitems can be added to a particular using the _create_subitem_ method shown below:
```python
subitem = item.create_subitem(item_name, column_values=column_values_dict)
```

## Changing Column Values ##

The column values of an item may also be retrieved and updated from an __Item__ instance in the following way as shown below.  
```
# First get the column value.
# Index for item.column_values may be the column id, title, or the list index integer.
column_value = item.column_values['text_colunn_1']
# Update the column text
column_value.text_value = 'Update Text'
# Now update the column value in the item.
item.change_column_value(column_value)
```

Multiple column values are retrieved and updated from the __Item__ instance using the *change_multiple_column_values* and *get_column_values* methods respectively.  More information on these methods can be found below in the [Item](#item) section of this document.

## Posting Updates ##
Updates represent interactions between users within a monday.com account with respect to a given item and are represented in moncli as an __Update__ object.  __Update__ instances are retrieved using the *get_updates* method from either a __MondayClient__ instance, which can retrieve all updates within the account accessible to the login user, or an __Item__ instance, which only has access to updates within the particular item.  

Updates are added to an item using the *add_update* method from the __Item__ instance as shown below.
```python
update = item.add_update('Hello, World!')
```

Once created, replies are also added to an update using the *add_reply* method from the __Update__ instance as shown below.
```python
reply = update.add_reply('Right back at you!')
```

Finally updates are removed from the __Item__ instance using either the *delete_update* method for removing a specific update, or the *clear_all_updates* method to remove all updates on the item as shown below.
```python
# Remove one update
item.delete_update(update.id)

# Remove all updates
item.clear_all_updates()
```

## Uploading Files ##

Files, or assets, represent files uploaded to items via a file-type column or updates via the *add_file* method on both __Item__ and __Update__ objects. 

When adding files to an item, a file column via the __FileColumn__ object must be identified as the column in which to place the newly uploaded file.  This is demonstrated in the example below.
```python
# First get the file column.
file_column = item.get_column_value(id='file_column_1')
# Then upload the file.
asset = item.add_file(file_column, '/users/test/monday_files/test.jpg')
```

Adding files to an update only requires the file path of the file to upload as shown below.
```python
asset = update.add_file('/users/test/monday_files/test.jpg')
```

Files are retrieved using the *get_files* method available on any __MondayClient__, __Item__, or __Update__ instance.  It is important to note that all files within the account accessible to the user are retrieved from the __MondayClient__ instance, while only files within the respective item or update are retrieved for __Item__ and __Update__ instances respectively.

Currently, the monday.com API only supports removing all files from a file column within an item.  This is done using the *remove_files* method of the __Item__ instance in the example shown below.
```python
# First get the file column.
file_column = item.get_column_value(id='file_column_1')
# Then clear all files.
assets = item.remove_files(file_column)
```

To remove files from an update, the only option currently available is to delete the update containing the file.  This is done using the *delete_update* method via an __Item__ instance or directly on an __Update__ instance with the *delete* method.

## Monday Models and Types

The **MondayModel** a Python base class that enables developers to define their monday.com boards as a Python class. This powerful new addition allows developers to retrieve individual items from a board as the defined **MondayModel** subclass, make simple value edits to configured fields, and both export data for and save updated data to monday.com via the API. 

Both models and types leverage the [Schematics](https://schematics.readthedocs.io/en/latest/) python package.

A **MondayModel** can be simply created using various **MondayType** classes.  Simply declare a class and inherit the **MondayModel** class to create a new Monday model. Each model comes with the *id* and *name* fields corresponding to the ID and name of the linked monday.com item respectively.

```python
from moncli.models import MondayModel
from moncli.types import *

class WorkTask(MondayModel):
    assignees = PeopleType(title='Assignees')
    status = StatusType(title='Status')
    due_date = DateType(title='Due Date')
    total_hours = NumberType(title='Total Hours')
```

All Moncli entity methods that return an item or list of items can also return them **MondayModel** instances using the *as_model* parameter.

```python
task = client.get_items(ids=[12345678], as_model=WorkTask)[0]
```

Any **MondayModel** instance may be updated and saved to monday.com via the API.

```python
from moncli.column_value import Person

task.assignees.append(Person(123456))
task.status = 'Done'
task.total_hours = 999
task.save() # Saves only fields that have changed
```

## Additional Questions/Feature Requests:

The [Moncli Wiki](https://github.com/trix-solutions/moncli/wiki) contains additional information regarding available entities and functionality.

Please feel free to log an issue or request a new feature by submitting a new issue or reaching out to me at andrew.shatz@trix.solutions. Thank you and happy coding!!!
