from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, enums, entities as en
from ..api_v2 import constants
from ..decorators import default_field_list, optional_arguments


class _User(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    created_at = types.StringType()
    url = types.StringType()
    email = types.StringType()
    enabled = types.BooleanType()
    birthday = types.StringType()
    country_code = types.StringType()
    is_guest = types.BooleanType()
    is_pending = types.BooleanType()
    join_date = types.StringType()
    location = types.StringType()
    mobile_phone = types.StringType()
    phone = types.StringType()
    photo_original = types.StringType()
    photo_thumb = types.StringType()
    photo_tiny = types.StringType()
    time_zone_identifier = types.StringType()
    title = types.StringType()
    utc_hours_diff = types.IntType()


class User(_User):
    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__account = None
        account = kwargs.pop('account', None)
        if account:
            self.__account = en.Account(creds=self.__creds, **account)
        self.__teams = None
        teams = kwargs.pop('teams', None)
        if account:
            self.__teams = [en.Account(creds=self.__creds, **team) for team in teams]
        super(User, self).__init__(kwargs)

    @property
    def account(self):
        if not self.__account:
            self.__account = self.get_account()
        return self.__account

    @property
    def teams(self):
        if not self.__teams:
            self.__teams = self.get_teams()
        return self.__teams

    def __repr__(self):
        o = self.to_primitive()
        
        if self.__account:
            o['account'] = self.__account
        if self.__teams:
            o['teams'] = [team.to_primitive() for team in self.__teams]

        return str(o)

    @default_field_list(config.DEFAULT_ACCOUNT_QUERY_FIELDS)
    def get_account(self, *args):
        args = ['account.' + arg for arg in args]
        account_data = client.get_users(
            self.__creds.api_key_v2, 
            *args,
            ids=[int(self.id)])[0]['account']

        return Account(
            creds=self.__creds,
            **account_data)
    
    @default_field_list(config.DEFAULT_TEAM_QUERY_FIELDS)
    def get_teams(self, *args):
        args = ['teams.' + arg for arg in args]
        teams_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['teams']

        return [Team(creds=self.__creds, **team_data) for team_data in teams_data]
    
    @optional_arguments(constants.CREATE_NOTIFICATION_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_NOTIFICATION_QUERY_FIELDS)
    def send_notification(self, text: str, target_id: str, target_type: enums.NotificationTargetType, *args, **kwargs):
        notification_data = client.create_notification(
            self.__creds.api_key_v2, 
            text, 
            self.id, 
            target_id, 
            target_type, 
            *args, 
            **kwargs)

        return en.Notification(notification_data)


class _Team(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    picture_url = types.StringType()


class Team(_Team):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__users = None
        users = kwargs.pop('users', None)
        if users:
            self.__users = [en.User(creds=self.__creds, **user) for user in users]
        super(Team, self).__init__(kwargs)

    @property
    def users(self):
        if not self.__users:
            self.__users = self.get_users()
        return self.__users

    def __repr__(self):
        o = self.to_primitive()
        if self.__users:
            o['users'] = self.__users
        return str(o)

    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_users(self, *args):
        args = ['users.' + arg for arg in args]
        users_data = client.get_teams(
            self.__creds.api_key_v2, 
            *args,
            ids=[int(self.id)])[0]['users']
        return [User(creds=self.__creds, **user_data) for user_data in users_data]


class _Account(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    first_day_of_the_week = types.StringType()
    logo = types.StringType()
    show_timeline_weekends = types.BooleanType()
    slug = types.StringType()


class Account(_Account):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__plan = None
        plan = kwargs.pop('plan', None)
        if plan:
            self.__plan = en.Plan(plan)
        super(Account, self).__init__(kwargs)

    @property
    def plan(self):
        if not self.__plan:
            self.__plan = self.get_plan()
        return self.__plan

    @property
    def first_day_of_the_week_enum(self):
        if self.first_day_of_the_week:
            return enums.FirstDayOfTheWeek[self.first_day_of_the_week]

    def __repr__(self):
        o = self.to_primitive()
        if self.__plan:
            o['plan'] = self.__plan
        return str(o)

    @default_field_list(config.DEFAULT_PLAN_QUERY_FIELDS)
    def get_plan(self, *args):
        args = ['plan.' + arg for arg in args]
        plan_data = client.get_account(
            self.__creds.api_key_v2, 
            *args)['plan']
        return en.Plan(plan_data)