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
    
        Properties

            name : `str`
                Query node entity name.
            arguments : `dict`
                Arguments associated with the query node entity.

        Methods

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

            Parameters

                body : `str`
                    The name of the GraphQL field being formatted with arguments.

            Returns

                query_string : `str`
                    GraphQL-formatted query string.
        """

        formatted_args = ', '.join(['{}:{}'.format(key, value) for key, value in self.arguments.items()])
        formatted_args = formatted_args.replace("'", '"')
        return '{} ({})'.format(body, formatted_args)


class GraphQLField(GraphQLNode):
    """A GraphQL field node.

        Methods

            add_fields : `void`
                Add fields to node.
            add_arguments : `void`
                Add arguments to node.
            get_field : `moncli.api_v2.graphql.GraphQLField`
                Get a child field of the given GraphQL field.
            format_body : `str`
                Format the GraphQL node into a query string.
            format_children : `str`
                Format child fields into query string.
    """

    def __init__(self, field_name: str, field_map: dict, *args, **kwargs):
        super(GraphQLField, self).__init__(field_name)
        self.__children: dict = {}
        self._field_map = field_map
        
        self.add_fields(*args)
        self.add_arguments(**kwargs)


    def add_fields(self, *args):
        """Add fields to node.

            Parameters

                args : `tuple`
                    The list of child fields to add.
        """

        for field in args:

            if not field or field == '':
                continue
            
            if type(field) is str:
                field_split = field.split('.')
                parent_field = field_split[0]
                child_fields = field_split[1:]
                
                if not child_fields:
                    field_group = [[]]
                # Check for list notation.
                elif child_fields[0].startswith('[') and child_fields[0].endswith(']'):
                    if len(child_fields) > 1:
                        raise GraphQLError('Field list syntax is only available for leaf-level fields.')
                    
                    list_fields = child_fields[0][1:-1]
                    if list_fields == '*':
                        field_group = [[f] for f in self._field_map[parent_field]]
                    else:
                        field_group = [[f.strip()] for f in list_fields.split(',')]
                else:
                    field_group = [child_fields]
                
                for group in field_group:
                    existing_field = self.get_field(parent_field)
                    # Add the new fields to the existing field
                    if existing_field:
                        existing_field.add_fields('.'.join(group))
                        continue
                    
                    new_field = GraphQLField(field_split[0], self._field_map)
                    new_field.add_fields('.'.join(group))
                    self.__children.__setitem__(new_field.name, new_field)

            elif type(field) is GraphQLField:
                self.__children.__setitem__(field.name, field)


    def add_arguments(self, **kwargs):
        """Add arguments to node.

            Parameters

                kwargs : `dict`
                    The field's argument pairs.
        """

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
        """Get a child field of the given GraphQL field.

            Parameters

                path : `str`
                    The string field path of the field.

            Returns

                field : `moncli.api_v2.graphql.GraphQLField`
                    The retrieved graphql field.
        """

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
        """Format the GraphQL node into a query string."""

        body: str = self.name

        if len(self.arguments) > 0:
            body = self.format_arguments(body)

        if len(self.__children) > 0:
            body = self.format_children(body)

        return body

    
    def format_children(self, body: str):
        """Format child fields into query string.
            
            Parameters

                body : `str`
                    The body of the base query to be amended.

            Returns

                query_string : `str`
                    The amended GraphQL query string.

        """

        formatted_children = ', '.join([child.format_body() for child in self.__children.values()])
        return '{} {{ {} }}'.format(body, formatted_children)


class GraphQLOperation(GraphQLField):
    """A GraphQL node for operations.
    
        Properties
        
            action_type : `str`
                The action type of the operation (query / mutation)
            query_name : `str`
                The name of the executed command.
            args : `tuple`
                A collection of added fields.
            kwargs : `dict`
                A collection of argument mappings 

        Methods
        
            add_query_variable : `void`
                Add a query variable to the query.
    """

    def __init__(self, action_type: OperationType, query_name: str, field_map: dict, *args, **kwargs):

        self.action_type = action_type.name.lower()
        super(GraphQLOperation, self).__init__(query_name, field_map, *args, **kwargs)
        self.query_variables: dict = {}


    def add_query_variable(self, key: str, value):
        """Add a query variable to the query.

            Parameters

                key : `str`
                    The query variable key.
                value : `object`
                    The query variable value.
        """

        self.query_variables.__setitem__(key, value)  


    def format_body(self):
        """Format the GraphQL node into a query string."""

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
    """Base GraphQL argument type and format."""
    def __init__(self, value):
        self.value = value

    def format(self):
        return self.value


class StringValue(ArgumentValue):
    """GraphQL string argument type and format."""
    def __init__(self, value):
        super(StringValue, self).__init__(str(value))

    def format(self):
        return '"{}"'.format(self.value)


class IntValue(ArgumentValue):
    """GraphQL integer argument type and format."""
    def __init__(self, value):
        super(IntValue, self).__init__(int(value))

    def format(self):
        return self.value


class BoolValue(ArgumentValue):
    """GraphQL boolean argument type and format."""
    def __init__(self, value):
        super(BoolValue, self).__init__(value)

    def format(self):
        return str(self.value).lower()


class ListValue(ArgumentValue):
    """GraphQL list argument type and format."""
    def __init__(self, value):
        super(ListValue, self).__init__(list(value))

    def format(self):
        return self.value

class EnumValue(ArgumentValue):
    """GraphQL enum argument type and format."""
    def __init__(self, value):
        super(EnumValue, self).__init__(value)

    def format(self):
        enum : Enum = self.value
        return enum.name


class JsonValue(ArgumentValue):
    """GraphQL json argument type and format."""
    def __init__(self, value):
        super(JsonValue, self).__init__(value)

    def format(self):
        return json.dumps(json.dumps(self.value))


class FileValue(ArgumentValue):
    """GraphQL file argument type and format."""
    def __init__(self, value):
        super(FileValue, self).__init__(value)

    def format(self):
        return str(self.value)


class GraphQLError(Exception):
    """GraphQL client error."""
    def __init__(self, message: str):
        self.message = message


def create_field(field_name: str, *args, **kwargs):
    """Create a GraphQL field.

        Parameters

            field_name : `str`
                The name of the parent field to create.
            args : `tuple`
                A collection of child fields to add.
            kwargs : `dict`
                A field argument value map for queried return fields.

        Returns

            field : `moncli.api_v2.graphql.GraphQLField`
                A graphql field node.
    """

    return GraphQLField(field_name, *args, **kwargs)


def create_value(value, value_type: ArgumentValueKind):
    """Transform value into ArgumentValue
    
        Parameters

            value : `object`
                Any data object value.
            value_type : `moncli.api_v2.graphql.ArgumentValueKind`
                The argument value conversion type.

        Results

            value = `moncli.api_v2.graphql.ArgumentValue`
                The GraphQL argument value.
    """

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