import json
from enum import Enum 


def create_field(name: str, *argv, **kwargs):

    return GraphQLField(name, *argv, **kwargs)


def create_query(name: str, *argv, **kwargs):
    
    return GraphQLOperation(OperationType.QUERY, name, *argv, **kwargs)


def create_mutation(name: str, *argv, **kwargs):
    
    return GraphQLOperation(OperationType.MUTATION, name, *argv, **kwargs)


class OperationType(Enum):
    QUERY = 1
    MUTATION = 2


class GraphQLNode():

    def __init__(self, name: str):

        self.name: str = name
        self.arguments: dict = {}


    def format_body(self):
        pass


    def format_arguments(self, body: str):

        formatted_args = ', '.join(['{}:{}'.format(key, value) for key, value in self.arguments.items()])
        return '{} ({})'.format(body, formatted_args)


class GraphQLField(GraphQLNode):

    def __init__(self, name: str, *argv, **kwargs):
        super(GraphQLField, self).__init__(name)
        self.__children: dict = {}
        
        self.add_fields(*argv)
        self.add_arguments(**kwargs)


    def add_fields(self, *argv):

        for field in argv:

            if field == None or field == '':
                continue
            
            if type(field) is str:

                field_split = field.split('.')
                existing_field = self.get_field(field_split[0])

                # Add the new fields to the existing field
                if existing_field != None:
                    existing_field.add_fields('.'.join(field_split[1:]))
                    continue

                new_field = GraphQLField(field_split[0])
                new_field.add_fields('.'.join(field_split[1:]))
                self.__children.__setitem__(new_field.name, new_field)

            elif type(field) is GraphQLField:
                self.__children.__setitem__(field.name, field)


    def add_arguments(self, **kwargs):

        for key, value in kwargs.items():

            arg_value : ArgumentValue = value
            formatted_value = arg_value.format()

            if formatted_value is not None:
                self.arguments.__setitem__(key, formatted_value)


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

    def __init__(self, action_type: OperationType, name: str, *argv, **kwargs):

        self.action_type = action_type.name.lower()
        super(GraphQLOperation, self).__init__(name, *argv, **kwargs)
        self.query_variables: dict = {}


    def add_query_variable(self, key: str, value):

        self.query_variables.__setitem__(key, value)  


    def format_body(self):

        body: str = self.name

        if len(self.arguments) > 0:
            body = self.format_arguments(body)

        body = self.format_children(body)

        body = '{} {{ {} }}'.format(self.action_type, body)

        return body


class ArgumentValue():

    def __init__(self, value):
        self.value = value

        
    def format(self):
        pass


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


class ArgumentValueKind(Enum):
    String = 1
    Int = 2
    Bool = 3
    Enum = 4
    List = 5
    Json = 6


def create_value(value, value_type: ArgumentValueKind):

    if value_type == ArgumentValueKind.String:
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