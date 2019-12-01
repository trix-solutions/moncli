# moncli
A Python Client and CLI tool for Monday.com

## Setup ##
To add the moncli package to your project, simply execute the following command within your Python 3 environment using pip.  Please note that this package is currently available for Python 3
```
$ pip3 install moncli
```


## Using the Monday.com client ##
The __MondayClient__ object is the entry point for all client activities and includes functionality for board, item, tag, and user management.  The following section will briefly overview what can be done with the __MondayClient__ object.

### Creating a Client ###
Before creating a new __MondayClient__, you will first need to retrieve your API v1 and v2 access keys by navigating to __https://<your_instance_name>.monday.com/admin/integrations/api__ and copying both the API v1 (personal or company) and API v2 keys.  

To create a new Monday.com client, simply run Python 3 and execute the following commands.
```
>>> from moncli import MondayClient
>>> client = MondayClient(user_name='user@email.com', api_key_v1='api_key_v1', api_key_v2='api_key_v2')
```
Please note that the __MondayClient__ object requires that the input 'username' matches the user declared on the API v2 token for authentication purposes.


### Creating a board ###
Boards can be created with the __MondayClient__ object using the following command.  The __\*argv__ parameter can be used to determine which fields on the new board to return.  In the example below, only the _id_ field of the __Board__ object is returned after creation.
```
>>> from moncli import BoardKind
>>>
>>> # Create a new board with default fields
>>> new_board = client.create_board(board_name='New Public Board', board_kind=BoardKind.public)
>>>
>>> # Create a new board with customized return fields
>>> field_list = ['id', 'name']
>>> new_board_with_custom_fields = client.create_board(board_name='New Public Board With Fields', board_kind=BoardKind.public, *field_list)
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
* ids (list\[int\]) - the IDs of the tags to return


### Getting users ###
Users can be retrieved from the __MondayClient__ object using the following command.
```
>>> from moncli import UserKind
>>> users = client.get_users(kind=UserKind.guests)
```
This example will retrieve the first 25 (default limit) guest users.  Optional parameters when querying __Users__ include:
* ids (list\[int\]) - the IDs of the users to return
* kind (UserKind) - the kind of users (all, non-guests, guests, pending) to return
* limit (int) - the maximum number of users per page to return
* newest_first (bool) - indicates whether to sort by created date descending


### Getting teams ###
Teams can be retrieved from the __MondayClient__ object using the following command.
```
>>> teams = client.get_teams(ids=[1234567,2345678])
```
This example will retrieve a list of __Team__ objects containing the input IDs.  Optional parameters when querying __Team__ objects include:
* ids (list\[int\]) - the IDs of the teams to return


### Getting... me ###
Finally, the __MondayClient__ can fetch the user associated with the API v2 token as a __User__ object using the following command.
```
>>> me = client.get_me()
```
This command is currently used by the __MondayClient__ to authorize the use of the API v2 token and can be put to very good use when sending notifications to other users from your own.


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


## Customized Queries and Mutations ##
Coming soon...

## Additional Questions/Feature Requests:
Please feel free to log an issue or request a new feature by submitting a new issue or reaching out to me at andrew.shatz@trix.solutions. Thank you and happy coding!!!
