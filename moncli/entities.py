from datetime import datetime

from . import api_v2 as client
from .constants import DATETIME_FORMAT
from .enums import BoardKind, ColumnType, NotificationTargetType


class MondayClient():

    def __init__(self, user_name: str, api_key_v1: str, api_key_v2: str):
     
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2

        me: User = self.get_me()
        if me.email.lower() != user_name.lower():
            raise AuthorizationError(user_name)
        

    def create_board(self, board_name: str, board_kind: BoardKind, *argv):

        resp = client.create_board(self.__api_key_v2, board_name, board_kind, *argv)

        return Board(self.__api_key_v1, self.__api_key_v2, **resp)
    

    def get_boards(self, **kwargs):

        result = []

        resp_boards = client.get_boards(self.__api_key_v2, 'id', 'name', **kwargs)

        for board_data in resp_boards:
            result.append(Board(self.__api_key_v1, self.__api_key_v2, **board_data))

        return result


    def get_board(self, id: str = None, name: str = None):

        field_list = [
            'id', 
            'name', 
            'board_folder_id', 
            'board_kind', 
            'description', 
            'items.id', 
            'owner.id', 
            'permissions',
            'pos',
            'state']

        if id != None and name != None:
            raise TooManyGetBoardParameters()

        elif id == None and name == None:
            raise NotEnoughGetBoardParameters()

        # Search for single board by ID
        elif id != None:
            resp_boards = client.get_boards(
                self.__api_key_v2, 
                *field_list,
                ids=int(id),
                limit=1)

            if len(resp_boards) == 0:
                raise BoardNotFound('id', id)

            return Board(self.__api_key_v1, self.__api_key_v2, **resp_boards[0])

        # Page through boards until name match appears.
        else:

            # Hard configure the pagination rate.
            page = 1
            page_limit = 1000
            record_count = 1000
            while record_count >= page_limit:
                resp_boards = client.get_boards(
                    self.__api_key_v2, 
                    *field_list,
                    limit=page_limit,
                    page=page)

                target_boards = [board for board in resp_boards if board['name'].lower() == name.lower()]

                if len(target_boards) == 0:
                    page += 1
                    record_count = len(resp_boards)
                    continue

                return Board(self.__api_key_v1, self.__api_key_v2, **resp_boards[0])
        
            if len(target_boards) == 0:
                raise BoardNotFound('name', name)        


    def archive_board(self, board_id: str):

        archive_board_resp = client.archive_board(
            self.__api_key_v2, 
            board_id,
            'id')

        return Board(self.__api_key_v1, self.__api_key_v2, **archive_board_resp)

    
    def get_items(self, ids, **kwargs):

        items_resp = client.get_items(
            self.__api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            ids=ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 

    
    def get_updates(self, **kwargs):
        
        resp = client.get_updates(
            self.__api_key_v2, 
            'id',
            'body',
            **kwargs)

        return [Update(**data) for data in resp]


    def create_notification(self, text: str, user_id: str, target_id: str, target_type: NotificationTargetType, **kwargs):

        resp = client.create_notification(
            self.__api_key_v2, 
            text, 
            user_id, 
            target_id,
            target_type,
            'id',
            'text',
            **kwargs)

        return Notification(**resp)


    def create_or_get_tag(self, tag_name: str, **kwargs):
        
        resp = client.create_or_get_tag(
            self.__api_key_v2, 
            tag_name,
            'id',
            'name',
            'color')

        return Tag(**resp)

    
    def get_tags(self, **kwargs):
        
        resp = client.get_tags(
            self.__api_key_v2,
            'id',
            'name',
            'color',
            **kwargs)

        return [Tag(**tag_data) for tag_data in resp]


    def get_users(self, **kwargs):
        
        resp = client.get_users(
            self.__api_key_v2, 
            'id',
            'name',
            'url',
            'email',
            'enabled',
            'account.id',
            'teams.id',
            'birthday',
            'country_code',
            'created_at',
            'is_guest',
            'is_pending',
            'join_date',
            **kwargs)

        return [User(self.__api_key_v1, self.__api_key_v2, **user_data) for user_data in resp]


    def get_teams(self, **kwargs):
        
        resp = client.get_teams(
            self.__api_key_v2,
            'id',
            'name',
            'picture_url',
            'users.id',
            **kwargs)

        return [Team(self.__api_key_v1, self.__api_key_v2, **team_data) for team_data in resp]

    
    def get_me(self):

        resp = client.get_me(
            self.__api_key_v2, 
            'id',
            'name',
            'url',
            'email',
            'enabled',
            'account.id',
            'teams.id',
            'birthday',
            'country_code',
            'created_at',
            'is_guest',
            'is_pending',
            'join_date')

        return User(self.__api_key_v1, self.__api_key_v2, **resp)


class Board():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__columns = None
        self.__groups = None
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2

        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            if key == 'board_folder_id':
                self.board_folder_id = value
            
            elif key == 'board_kind':
                self.board_kind = value

            elif key == 'description':
                self.description = value

            elif key == 'items':
                self.__item_ids = [int(item['id']) for item in value]

            elif key == 'owner':
                self.__owner_id: str = value['id']

            elif key == 'permissions':
                self.permissions = value

            elif key == 'pos':
                self.position = value

            elif key == 'state':
                self.state = value


    def create_column(self, title:str, column_type: ColumnType, *argv):

        resp = client.create_column(
            self.__api_key_v2, 
            self.id, 
            title, 
            column_type, 
            *argv)

        return Column(api_key_v2=self.__api_key_v2, **resp)

    
    def change_column_value(self, item_id: str, column_id: str, value: str, *argv):

        resp = client.change_column_value(
            self.__api_key_v2, 
            item_id, 
            column_id, 
            self.id,
            value, 
            *argv)

        return Item(self.__api_key_v1, self.__api_key_v2, **resp)

    
    def change_multiple_column_values(self, item_id: str, column_values: dict, *argv):

        resp = client.change_multiple_column_value(
            self.__api_key_v2,
            item_id,
            self.id,
            column_values,
            *argv)

        return Item(self.__api_key_v1, self.__api_key_v2, **resp)

    
    def get_columns(self):

        if self.__columns == None:

            board = client.get_boards(
                self.__api_key_v2,
                'columns.id',
                'columns.archived',
                'columns.settings_str',
                'columns.title',
                'columns.type',
                'columns.width',
                ids=int(self.id))[0]

            self.__columns = [
                Column(api_key_v2=self.__api_key_v2, board_id=self.id, **column_data) 
                for column_data 
                in board['columns']
            ]

        return self.__columns

    def add_group(self, group_name: str, *argv):

        group_data = client.create_group(
            self.__api_key_v2,
            self.id,
            group_name,
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.id,
            **group_data)


    def duplicate_group(self, group_id: str, add_to_top: bool = False, group_title: str = None, *argv):
        
        group_data = client.duplicate_group(
            self.__api_key_v2, 
            self.id, 
            group_id, 
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.id,
            **group_data)


    def get_groups(self):

        if self.__groups == None:
            
            board = client.get_boards(
                self.__api_key_v2,
                'groups.id',
                'groups.title',
                'groups.archived',
                'groups.color',
                'groups.deleted',
                'groups.items.id',
                'groups.position',
                ids=int(self.id))[0]

            self.__groups = [
                Group(api_key_v1=self.__api_key_v1, api_key_v2=self.__api_key_v2, board_id=self.id, **group_data)
                for group_data
                in board['groups']
            ]

        return self.__groups


    def archive_group(self, group_id: str, *argv):
        
        group_data = client.archive_group(
            self.__api_key_v2, 
            self.id,
            group_id,
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.id,
            **group_data)


    def delete_group(self, group_id: str, *argv):
        
        group_data = client.delete_group(
            self.__api_key_v2,
            self.id,
            group_id,
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.id,
            **group_data)


    def add_item(self, item_name: str, **kwargs):

        item = client.create_item(self.__api_key_v2, item_name, self.id, 'id', **kwargs)

        return item['id']


    def get_items(self):
        
        items_resp = client.get_items(
            self.__api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            ids=self.__item_ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 


    def get_items_by_column_values(self, column_id: str, column_value: str, *argv, **kwargs):
        
        items_data = client.get_items_by_column_values(
            self.__api_key_v2, 
            self.id, 
            column_id, 
            column_value, 
            *argv, 
            **kwargs)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_data]


    def move_item_to_group(self, item_id: str, group_id: str, *argv):
        
        item_data = client.move_item_to_group(
            self.__api_key_v2,
            item_id,
            group_id)

        return Item(self.__api_key_v1, self.__api_key_v2, **item_data)


    def archive_item(self, item_id: str, *argv):

        item_data = client.archive_item(
            self.__api_key_v2,
            item_id,
            *argv)
        
        return Item(self.__api_key_v1, self.__api_key_v2, **item_data)

    
    def delete_item(self, item_id: str, *argv):
        
        item_data = client.delete_item(
            self.__api_key_v2,
            item_id,
            *argv)

        return Item(self.__api_key_v1, self.__api_key_v2, **item_data)


    def add_update(self, body: str, item_id: str, *argv):
        
        update_data = client.create_update(
            self.__api_key_v2,
            body,
            item_id,
            *argv)

        return Update(**update_data)


class Column():

    def __init__(self, **kwargs):
        self.__api_key_v1 = kwargs['api_key_v1']
        self.__api_key_v2 = kwargs['api_key_v2']
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'archived':
                self.archived = value

            elif key == 'settings_str':
                self.settings_str = value

            elif key == 'title':
                self.title = value
            
            elif key == 'type':
                self.type = value

            elif key == 'width':
                self.width = value

            elif key == 'board_id':
                self.board_id = value

    
    def change_value(self, item_id, value: str, *argv):

        item_data = client.change_column_value(
            self.__api_key_v2,
            item_id,
            self.id,
            self.board_id,
            value,
            *argv)
        
        return Item(self.__api_key_v1, self.__api_key_v2, **item_data)


    def change_multiple_value(self, item_id: str, column_values: str, *argv):
        
        item_data = client.change_multiple_column_value(
            self.__api_key_v2,
            item_id,
            self.board_id,
            column_values,
            *argv)

        return Item(self.__api_key_v1, self.__api_key_v2, **item_data)


class Group():

    def __init__(self, **kwargs):
        self.__api_key_v1 = kwargs['api_key_v1']
        self.__api_key_v2 = kwargs['api_key_v2']
        self.id = kwargs['id']
        self.board_id = kwargs['board_id']
        self.__item_ids = None

        for key, value in kwargs.items():

            if key == 'title':
                self.title = value

            elif key == 'archived':
                self.archived = value
            
            elif key == 'color':
                self.color = value

            elif key == 'deleted':
                self.deleted = value

            elif key == 'items':
                self.__item_ids = [int(item['id'] for item in value)]

            elif key == 'position':
                self.position = value
    

    def duplicate(self, group_title: str, add_to_top: bool = False, *argv):
        
        group_data = client.duplicate_group(
            self.__api_key_v2, 
            self.board_id, 
            self.id, 
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.board_id,
            **group_data)


    def archive(self, *argv):
        
        group_data = client.archive_group(
            self.__api_key_v2,
            self.board_id,
            self.id,
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.board_id,
            **group_data)


    def delete(self, *argv):
        
        group_data = client.delete_group(
            self.__api_key_v2,
            self.board_id,
            self.id,
            *argv)

        return Group(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            board_id=self.board_id
            **group_data)


    def add_item(self, item_name: str, column_values: str = None, *argv):
        
        item_data = client.create_item(
            self.__api_key_v2,
            item_name,
            self.board_id,
            *argv,
            column_values=column_values)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)


    def get_items(self):

        items_resp = client.get_items(
            self.__api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            ids=self.__item_ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 


    def get_items_by_column_values(self, column_id: str, column_value: str, *argv, **kwargs):
        
        items_data = client.get_items_by_column_values(
            self.__api_key_v2,
            self.board_id,
            self.id,
            column_value,
            *argv,
            **kwargs)

        return [
            Item(api_key_v1=self.__api_key_v1, api_key_v2=self.__api_key_v2, **item_data)
            for item_data
            in items_data
        ]

    
    def move_item(self, item_id: str, group_id: str, *argv):
        
        item_data = client.move_item_to_group(
            self.__api_key_v2, 
            item_id, 
            group_id,
            *argv)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)


    def archive_item(self, item_id: str, *argv):
        
        item_data = client.archive_item(
            self.__api_key_v2,
            item_id,
            *argv)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)

    
    def delete_item(self, item_id: str, *argv):
        
        item_data = client.delete_item(
            self.__api_key_v2,
            item_id, 
            *argv)
            
        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)


class Item():

    def __init__(self, **kwargs):
        self.__api_key_v1 = kwargs['api_key_v1']
        self.__api_key_v2 = kwargs['api_key_v2']
        self.__column_values = None
        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'board':
                
                if type(value) == type(Board):
                    self.board = value
                
                elif type(value) is dict:
                    
                    if value.__contains__('name'):
                        self.board = Board(self.__api_key_v1, self.__api_key_v2, **value)

                    else:
                        self.__board_id = value['id']

            elif key == 'column_values':
                self.__column_values = [ColumnValue(**column_values) for column_values in value]

            elif key == 'creator_id':
                self.creator_id = value

            elif key == 'group':
                self.__group_id = value['id']

            elif key == 'state':
                self.state = value
            
            elif key == 'subscribers':
                self.__subscriber_ids = [int(item['id']) for item in value]

        
    def get_column_values(self):

        if self.__column_values == None:           
            item = client.get_items(
                self.__api_key_v2,
                'column_values.id',
                'column_values.text',
                'column_values.title',
                'column_values.value',
                'column_values.additional_info',
                ids=int(self.id))
                
            self.__column_values = [ColumnValue(**column_values) for column_values in item['column_values']]

        return self.__column_values

    
    def change_column_value(self, column_id: str, value: str, *argv):
        
        item_data = client.change_column_value(
            self.__api_key_v2,
            self.id,
            column_id,
            self.board.id,
            value,
            *argv)


        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)

    
    def change_multiple_column_values(self, column_values: str, *argv):
        
        item_data = client.change_multiple_column_value(
            self.__api_key_v2,
            self.id,
            self.board.id,
            column_values,
            *argv)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)

    
    def move_to_group(self, group_id: str, *argv):
        
        item_data = client.move_item_to_group(
            self.__api_key_v2,
            self.id,
            group_id)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)


    def archive(self, *argv):
        
        item_data = client.archive_item(
            self.__api_key_v2,
            self.id,
            *argv)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)


    def delete(self, *argv):
        
        item_data = client.delete_item(
            self.__api_key_v2,
            self.id,
            *argv)

        return Item(
            api_key_v1=self.__api_key_v1,
            api_key_v2=self.__api_key_v2,
            **item_data)


    def add_update(self, body: str, *argv):
        
        update_data = client.create_update(
            self.__api_key_v2, 
            body, 
            self.id,
            *argv)

        return Update(**update_data)

    
    def get_updates(self, *argv, **kwargs):
        
        updates_data = client.get_updates(*argv, **kwargs)

        return [Update(**update_data) for update_data in updates_data]


class ColumnValue():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value

            elif key == 'title':
                self.title = value

            elif key == 'value':
                self.value = value

            elif key == 'additional_info':
                self.additional_info = value


class Update():

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        
        for key, value in kwargs.items():

            if key == 'body':
                self.body = value


class Notification():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value


class Tag():

    def __init__(self, **kwargs):

        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            elif key == 'color':
                self.color = value

class User():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2
          
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            elif key == 'url':
                self.url = value

            elif key == 'email':
                self.email = value

            elif key == 'enabled':
                self.enabled = value

            elif key == 'teams':
                self.__team_ids = [int(team_data['id']) for team_data in value]

            if key == 'birthday':
                self.birthday = value

            elif key == 'country_code':
                self.country_code = value

            elif key == 'created_at': 
                self.create_at = value

            elif key == 'is_guest':
                self.is_guest = value

            elif key == 'is_pending':
                self.is_pending = value

            elif key == 'join_date':
                self.join_date = value

            elif key == 'location':
                self.locaiton = value

            elif key == 'mobile_phone':
                self.mobile_phone = value

            elif key == 'phone':
                self.phone = value

            elif key == 'photo_original':
                self.photo_original = value

            elif key == 'photo_thumb':
                self.photo_thumb = value

            elif key == 'title':
                self.title = value

            elif key == 'utc_hours_diff':
                self.utc_hours_diff = value

        
    def get_account(self):

        resp = client.get_users(
            self.__api_key_v2, 
            'account.first_day_of_the_week',
            'account.id',
            'account.name',
            'account.show_timeline_weekends',
            'account.slug',
            'account.logo',
            ids=int(self.id))

        return Account(self.__api_key_v2, user_id=self.id, **resp[0]['account'])

    
    def get_teams(self):

        resp = client.get_teams(
            self.__api_key_v2,
            'id',
            'name',
            'picture_url',
            'users.id',
            ids=self.__team_ids)

        return [Team(self.__api_key_v1, self.__api_key_v2, **team_data) for team_data in resp]

    
    def send_notification(self, text: str, target_id: str, target_type: NotificationTargetType, *argv, **kwargs):

        client.create_notification(self.__api_key_v2, text, self.id, target_id, target_type, *argv, **kwargs)


class Account():

    def __init__(self, api_key_v2: str, **kwargs):
        self.__api_key_v2 = api_key_v2
        self.__user_id = kwargs['user_id']

        self.first_day_of_the_week = kwargs['first_day_of_the_week']
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.show_timeline_weekends = kwargs['show_timeline_weekends']
        self.slug = kwargs['slug']

        for key, value in kwargs.items():

            if key == 'logo':
                self.logo = value


    def get_plan(self):

        resp = client.get_users(
            self.__api_key_v2, 
            'account.plan.max_users',
            'account.plan.period',
            'account.plan.tier',
            'account.plan.version',
            ids=int(self.__user_id))

        return Plan(**resp[0]['account']['plan'])


class Team():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2
        
        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'picture_url':
                self.picture_url = value

            if key == 'users':
                self.__user_ids = [int(user['id']) for user in value]

        
    def get_users(self):

        user_resp = client.get_users(
            self.__api_key_v2, 
            'id',
            'name',
            'url',
            'email',
            'enabled',
            'account.id',
            'teams.id',
            ids=self.__user_ids)

        return [User(self.__api_key_v1, self.__api_key_v2, **user_data) for user_data in user_resp]


class Plan():

    def __init__(self, **kwargs):

        for key, value in kwargs.items():

            if key == 'max_users':
                self.max_users = value

            elif key == 'period':
                self.period = value

            elif key == 'tier':
                self.tier = value

            elif key == 'version':
                self.version = value


class AuthorizationError(Exception):

    def __init__(self, user_name: str):

        self.message = 'User {} was not recognized by the applied token'.format(user_name)

class GroupNotFound(Exception):

    def __init__(self, board, group_name):

        self.board_id = board.id
        self.board_name = board.name
        self.group_name = group_name
        self.message = 'Unable to find group {} in board {}.'.format(self.group_name, self.board_name)
    
        

class BoardNotFound(Exception):

    def __init__(self, search_type, value):
        
        if search_type == 'id':
            self.message = 'Unable to find board with name: "{}".'.format(value)
        
        elif search_type == 'name':
            self.message = 'Unable to find board with the ID: "{}".'.format(value)

        else:
            self.message = 'Unable to find the requested board.'

class TooManyGetBoardParameters(Exception):

    def __init__(self):
        self.message = "Unable to use both 'id' and 'name' when querying for a board."

class NotEnoughGetBoardParameters(Exception):

    def __init__(self):
        self.message = "Either the 'id' or 'name' is required when querying a board."