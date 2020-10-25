from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, enums, entities as en
from ..api_v2 import constants


class _User(Model):
    """User base model"""

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
    """A monday.com user
    
    __________
    Properties
    
        account : `moncli.entities.user.Account`
            The user's account.
        birthday : `str`
            The user's birthday.
        country_code : `str`
            The user's country code.
        created_at : `str`
            The user's creation date.
        email : `str`
            The user's email.
        enabled : `bool`
            Is the user enabled or not.
        id : `str`
            The user's unique identifier.
        is_guest : `bool`
            Is the user a guest or not.
        is_pending : `bool`
            Is the user a pending user.
        is_view_only : `bool`
            Is the user a view only user or not.
        join_date : `str`
            The date the user joined the account.
        location : `str`
            The user' location.
        mobile_phone : `str`
            The user's mobile phone number.
        name : `str`
            The user's name.
        phone : `str`
            The user's phone number.
        photo_original : `str`
            The user's photo in the original size.
        photo_small : `str`
            The user's photo in small size (150x150).
        photo_thumb : `str`
            The user's photo in thumbnail size (100x100).
        photo_thumb_small : `str`
            The user's photo in small thumbnail size (50x50).
        photo_tiny : `str`
            The user's photo in tiny size (30x30).
        teams : `list[moncli.entities.user.Team]`
            The teams the user is a member in.
        time_zone_identifier : `str`
            The user's time zone identifier.
        title : `str`
            The user's title.
        url : `str`
            The user's profile url.
        utc_hours_diff : `int`
            The user's UTC hours difference.

    _______
    Methods

        get_account : `moncli.entities.Account`
            Get the user's account.
        get_teams : `list[moncli.entities.Team]`
            Get teams the user is a member in.
        send_notification : `moncli.entities.objects.Notification`
            Create a new notification.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__account = None
        account = kwargs.pop('account', None)
        if account:
            self.__account = en.Account(creds=self.__creds, **account)
        self.__teams = None
        teams = kwargs.pop('teams', None)
        if teams != None:
            self.__teams = [Team(creds=self.__creds, **team) for team in teams]
        super(User, self).__init__(kwargs)

    @property
    def account(self):
        """The user's account"""

        if not self.__account:
            self.__account = self.get_account()
        return self.__account

    @property
    def teams(self):
        """The teams the user is a member in."""

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


    def get_account(self, *args):
        """Get the user's account.

        __________
        Parameters

            args : `tuple`
                The list of account return fields.
        
        _______
        Returns

            account : `moncli.entities.Account`
                The user's account.

        _____________
        Return Fields

            first_day_of_the_week : `str`
                The first day of the week for the account (sunday / monday).
            id : `int`
                The account's unique identifier.
            logo : `str`
                The account's logo.
            name : `str`
                The account's name.
            plan : `moncli.entities.Plan`
                The account's payment plan.
            show_timeline_weekends : `bool`
                Show weekends in timeline.
            slug : `str`
                The account's slug.
        """

        args = ['account.' + arg for arg in client.get_field_list(constants.DEFAULT_ACCOUNT_QUERY_FIELDS, *args)]
        account_data = client.get_users(
            self.__creds.api_key_v2, 
            *args,
            ids=[int(self.id)])[0]['account']
        return Account(
            creds=self.__creds,
            **account_data)
    

    def get_teams(self, *args):
        """Get teams the user is a member in.

        __________
        Parameters

            args : `tuple`
                The list of team return fields.

        _______
        Returns

            teams : `list[moncli.entities.Team]`
                Teams the user is a member in.

        _____________
        Return Fields

            id : `int`
                The team's unique identifier.
            name : `str`
                The team's name.
            picture_url : `str`
                The team's picture url.
            users : `moncli.entities.user.User`
                The users in the team.
        """

        args = ['teams.' + arg for arg in client.get_field_list(constants.DEFAULT_TEAM_QUERY_FIELDS, *args)]
        teams_data = client.get_users(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['teams']
        return [Team(creds=self.__creds, **team_data) for team_data in teams_data]
    

    def send_notification(self, text: str, target_id: str, target_type: enums.NotificationTargetType, *args, **kwargs):
        """Create a new notification.

        __________
        Parameters

            text : `str`
                The notification text.
            user_id : `str`
                The user's unique identifier.
            target_id : `str`
                The target's unique identifier.
            target_type : `moncli.enums.NotificationTargetType`
                The target's type (Project / Post)
            args : `tuple`
                The list of noficiation return fields.
            kwargs : `dict`
                Optional keyword arguments.

        _______
        Returns

            notification : `moncli.entities.ActivityLog`
                The new notification.

        _____________
        Return Fields

            id : `str`
                The notification's unique identifier.
            text : `str`
                The notification text.
        
        __________________
        Optional Arguments

            payload : `json`
                The notification payload.
        """

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
    """Team base model."""

    id = types.StringType(required=True)
    name = types.StringType()
    picture_url = types.StringType()


class Team(_Team):
    """A team of users.
    
    __________
    Properties

        id : `int`
            The team's unique identifier.
        name : `str`
            The team's name.
        picture_url : `str`
            The team's picture url.
        users : `moncli.entities.User`
            The users in the team.

    _______
    Methods

        get_users : `list[moncli.entities.User]`
            Get the users in the team.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__users = None
        users = kwargs.pop('users', None)
        if users:
            self.__users = [en.User(creds=self.__creds, **user) for user in users]
        super(Team, self).__init__(kwargs)

    @property
    def users(self):
        """The users in the team."""

        if not self.__users:
            self.__users = self.get_users()
        return self.__users

    def __repr__(self):
        o = self.to_primitive()
        if self.__users:
            o['users'] = self.__users
        return str(o)

    def get_users(self, *args, **kwargs):
        """Get the users in the team.
        
        __________
        Parameters

            args : `tuple`
                The list of user return fields.
            kwargs : `dict`
                Optional keyword arguments for querying the team's users.

        _______
        Returns

            users : `list[moncli.entities.User]`
                The users in the team.

        _____________
        Return Fields

            account : `moncli.entities.Account`
                The user's account.
            birthday : `str`
                The user's birthday.
            country_code : `str`
                The user's country code.
            created_at : `str`
                The user's creation date.
            email : `str`
                The user's email.
            enabled : `bool`
                Is the user enabled or not.
            id : `str`
                The user's unique identifier.
            is_guest : `bool`
                Is the user a guest or not.
            is_pending : `bool`
                Is the user a pending user.
            is_view_only : `bool`
                Is the user a view only user or not.
            join_date : `str`
                The date the user joined the account.
            location : `str`
                The user' location.
            mobile_phone : `str`
                The user's mobile phone number.
            name : `str`
                The user's name.
            phone : `str`
                The user's phone number.
            photo_original : `str`
                The user's photo in the original size.
            photo_small : `str`
                The user's photo in small size (150x150).
            photo_thumb : `str`
                The user's photo in thumbnail size (100x100).
            photo_thumb_small : `str`
                The user's photo in small thumbnail size (50x50).
            photo_tiny : `str`
                The user's photo in tiny size (30x30).
            teams : `list[moncli.entities.Team]`
                The teams the user is a member in.
            time_zone_identifier : `str`
                The user's time zone identifier.
            title : `str`
                The user's title.
            url : `str`
                The user's profile url.
            utc_hours_diff : `int`
                The user's UTC hours difference.
        
        __________________
        Optional Arguments

            ids : `list[int]`
                A list of users unique identifiers.
            kind : `moncli.enums.UserKind`
                The kind to search users by (all / non_guests / guests / non_pending)
            newest_first : `bool`
                Get the recently created users at the top of the list.
            limit : `int`
                Number of users to get.            
        """

        args = ['users.' + arg for arg in client.get_field_list(constants.DEFAULT_USER_QUERY_FIELDS, *args)]
        if kwargs:
            kwargs = {'users': kwargs}
        users_data = client.get_teams(
            self.__creds.api_key_v2, 
            *args,
            ids=[int(self.id)],
            **kwargs)[0]['users']
        return [User(creds=self.__creds, **user_data) for user_data in users_data]


class _Account(Model):
    """Account base model."""

    id = types.StringType(required=True)
    name = types.StringType()
    first_day_of_the_week = types.StringType()
    logo = types.StringType()
    show_timeline_weekends = types.BooleanType()
    slug = types.StringType()


class Account(_Account):
    """Your monday.com account.

    __________
    Properties

        first_day_of_the_week : `str`
            The first day of the week for the account (sunday / monday).
        id : `int`
            The account's unique identifier.
        logo : `str`
            The account's logo.
        name : `str`
            The account's name.
        plan : `moncli.entities.Plan`
            The account's payment plan.
        show_timeline_weekends : `bool`
            Show weekends in timeline.
        slug : `str`
            The account's slug.

    _______
    Methods

        get_plan : `moncli.entities.Plan`
            Get the account's payment plan.
    """

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__plan = None
        plan = kwargs.pop('plan', None)
        if plan:
            self.__plan = en.Plan(plan)
        super(Account, self).__init__(kwargs)

    @property
    def plan(self):
        """A payment plan."""
        if not self.__plan:
            self.__plan = self.get_plan()
        return self.__plan

    @property
    def first_day_of_the_week_enum(self):
        """The first day of the week for the account (sunday / monday)."""

        if self.first_day_of_the_week:
            return enums.FirstDayOfTheWeek[self.first_day_of_the_week]

    def __repr__(self):
        o = self.to_primitive()
        if self.__plan:
            o['plan'] = self.__plan
        return str(o)

    def get_plan(self, *args):
        """Get the account's payment plan.
        
        __________
        Parameters

            args : `tuple`
                The list of plan optional return fields.
        
        _______
        Returns

            plan : `moncli.entities.Plan`
                The account's payment plan.
        
        _____________
        Return Fields

            max_users : `int`
                The maximum users allowed in the plan.
            period : `str`
                The plan's time period.
            tier : `str`
                The plan's tier.
            version : `int`
                The plan's version.
        """
        
        args = ['plan.' + arg for arg in client.get_field_list(constants.DEFAULT_PLAN_QUERY_FIELDS)]
        plan_data = client.get_account(
            self.__creds.api_key_v2, 
            *args)['plan']
        return en.Plan(plan_data)