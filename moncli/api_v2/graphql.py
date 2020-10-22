import json
from enum import Enum 


class OperationType(Enum):
    """GraphQL query operation type."""
    QUERY = 1
    MUTATION = 2


class ArgumentValueKind(Enum):
    """GraphQL types for arguments and variables."""
    Default = 0
    String = 1
    Int = 2
    Bool = 3
    Enum = 4
    List = 5
    Json = 6
    File = 7


class GraphQLNode():
    """Base node in a GraphQL query.
    
    __________
    Properties
    __________
    name : `str`
        Query node entity name.
    arguments : `dict`
        Arguments associated with the query node entity.

    
    _______
    Methods
    _______
    format_body : `str`
        Formats the GraphQL node into a query string.
    format_arguments : `str`
        Formats arguments as a query string.
    """

    def __init__(self, field_name: str):

        self.name: str = field_name
        self.arguments: dict = {}


    def format_body(self):
        """Formats the GraphQL node into a query string."""
        pass


    def format_arguments(self, body: str):
        """Formats arguments as query string.

        __________
        Parameters
        __________
        body : `str`
            The name of the GraphQL field being formatted with arguments.

        _______
        Returns
        _______
        query_string : `str`
            GraphQL-formatted query string.
        """

        formatted_args = ', '.join(['{}:{}'.format(key, value) for key, value in self.arguments.items()])
        formatted_args = formatted_args.replace("'", '"')
        return '{} ({})'.format(body, formatted_args)


class GraphQLField(GraphQLNode):

    def __init__(self, field_name: str, *args, **kwargs):
        super(GraphQLField, self).__init__(field_name)
        self.__children: dict = {}
        
        self.add_fields(*args)
        self.add_arguments(**kwargs)


    def add_fields(self, *args):

        for field in args:

            if not field or field == '':
                continue
            
            if type(field) is str:
                field_split = field.split('.')
                existing_field = self.get_field(field_split[0])

                # Add the new fields to the existing field
                if existing_field:
                    existing_field.add_fields('.'.join(field_split[1:]))
                    continue

                new_field = GraphQLField(field_split[0])
                new_field.add_fields('.'.join(field_split[1:]))
                self.__children.__setitem__(new_field.name, new_field)

            elif type(field) is GraphQLField:
                self.__children.__setitem__(field.name, field)


    def add_arguments(self, **kwargs):

        for key, value in kwargs.items():
            if isinstance(value, ArgumentValue):
                arg_value : ArgumentValue = value
                formatted_value = arg_value.format()
                if formatted_value:
                    self.arguments.__setitem__(key, formatted_value)
            else:
                field = self.get_field(key)
                if not field:
                    raise GraphQLError('Unable to add arguments to "{}" because it was not specified as an output field'.format(key))

                self.get_field(key).add_arguments(**value)


    def get_field(self, path: str):

        split_path = path.split('.')
        child_name = split_path[0]
        
        if not self.__children.__contains__(child_name):
            return None

        node: GraphQLField = self.__children.get(child_name)
        remaining_path = split_path[1:]

        if (len(remaining_path) == 0):
            return node

        return node.get_field('.'.join(remaining_path))


    def format_body(self):

        body: str = self.name

        if len(self.arguments) > 0:
            body = self.format_arguments(body)

        if len(self.__children) > 0:
            body = self.format_children(body)

        return body

    
    def format_children(self, body: str):

        formatted_children = ', '.join([child.format_body() for child in self.__children.values()])
        return '{} {{ {} }}'.format(body, formatted_children)


class GraphQLOperation(GraphQLField):

    def __init__(self, action_type: OperationType, query_name: str, *args, **kwargs):

        self.action_type = action_type.name.lower()
        super(GraphQLOperation, self).__init__(query_name, *args, **kwargs)
        self.query_variables: dict = {}


    def add_query_variable(self, key: str, value):

        self.query_variables.__setitem__(key, value)  


    def format_body(self):

        body: str = self.name

        if len(self.arguments) > 0:
            body = self.format_arguments(body)

        body = self.format_children(body)

        if len(self.query_variables) > 0:
            var_list = ['${}: {}'.format(key, value) for key, value in self.query_variables.items()]
            var_format = '({})'.format(', '.join(var_list))
            body = '{} {} {{ {} }}'.format(self.action_type, var_format, body)
        else:
            body = '{} {{ {} }}'.format(self.action_type, body)

        return body


class ArgumentValue():
    def __init__(self, value):
        self.value = value

    def format(self):
        return self.value


class StringValue(ArgumentValue):
    def __init__(self, value):
        super(StringValue, self).__init__(str(value))

    def format(self):
        return '"{}"'.format(self.value)


class IntValue(ArgumentValue):
    def __init__(self, value):
        super(IntValue, self).__init__(int(value))

    def format(self):
        return self.value


class BoolValue(ArgumentValue):
    def __init__(self, value):
        super(BoolValue, self).__init__(value)

    def format(self):
        return str(self.value).lower()


class ListValue(ArgumentValue):
    def __init__(self, value):
        super(ListValue, self).__init__(list(value))

    def format(self):
        return self.value

class EnumValue(ArgumentValue):
    def __init__(self, value):
        super(EnumValue, self).__init__(value)

    def format(self):
        enum : Enum = self.value
        return enum.name


class JsonValue(ArgumentValue):
    def __init__(self, value):
        super(JsonValue, self).__init__(value)

    def format(self):
        return json.dumps(json.dumps(self.value))


class FileValue(ArgumentValue):
    def __init__(self, value):
        super(FileValue, self).__init__(value)

    def format(self):
        return str(self.value)


class GraphQLError(Exception):
    def __init__(self, message: str):
        self.message = message


def create_field(field_name: str, *args, **kwargs):

    return GraphQLField(field_name, *args, **kwargs)


def create_query(query_name: str, *args, **kwargs):
    
    return GraphQLOperation(OperationType.QUERY, query_name, *args, **kwargs)


def create_mutation(query_name: str, *args, **kwargs):
    
    return GraphQLOperation(OperationType.MUTATION, query_name, *args, **kwargs)


def create_value(value, value_type: ArgumentValueKind):
    if value_type == ArgumentValueKind.Default:
        return ArgumentValue(value)
    elif value_type == ArgumentValueKind.String:
        return StringValue(value)   
    elif value_type == ArgumentValueKind.Int:
        return IntValue(value)
    elif value_type == ArgumentValueKind.Bool:
        return BoolValue(value)
    elif value_type == ArgumentValueKind.Enum:
        return EnumValue(value)
    elif value_type == ArgumentValueKind.List:
        return ListValue(value)
    elif value_type == ArgumentValueKind.Json:
        return JsonValue(value)