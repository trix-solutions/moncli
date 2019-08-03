from enum import Enum

class OperationType(Enum):
    QUERY = 1
    MUTATION = 2


class MondayApiError(Exception):

    def __init__(self, operation_type: OperationType, entity: str, error_code: int, message: str):

        self.operation_type = operation_type.name.lower()
        self.entity = entity
        self.error_code = error_code
        self.message = message


class GraphQLNode():
    
    def __init__(self):

        self.name: str = None
        self.path: str = None
        self.children: list = []
        self.arguments: dict = {}


    def format_body(self):
        pass


    def format_arguments(self, body: str):

        formatted_args = ', '.join(['{}:{}'.format(key, value) for key, value in self.arguments.items()])
        return '{} ({})'.format(body, formatted_args)


    def format_children(self, body: str):

        formatted_children = ', '.join([child.format_body() for child in self.children])
        return '{} {{ {} }}'.format(body, formatted_children)


class GraphQLField(GraphQLNode):

    def __init__(self, name: str, path: str, nodes: dict, **kwargs):
        super(GraphQLField, self).__init__()

        self.name = name
        self.path = path
        self.__nodes = nodes

        self.__nodes.__setitem__(self.path, self)
        
        for key, value in kwargs.items():
            if type(value) is str:
                self.arguments.__setitem__(key, '"{}"'.format(value))
            elif isinstance(value, Enum):
                self.arguments.__setitem__(key, value.name)
            else:
                self.arguments.__setitem__(key, value)


    def add_fields(self, *argv):

        for name in argv:
            path: str = '.'.join([self.path, name])
            self.children.append(GraphQLField(name, path, self.__nodes))

        return self


    def get_field(self, path: str):

        return self.__nodes.get(path)


    def add_argument_field(self, name: str, **kwargs):

        path: str = '.'.join([self.path, name])
        self.children.append(GraphQLField(name, path, self.__nodes, **kwargs))

        return self


    def format_body(self):

        body: str = self.name

        if len(self.arguments) > 0:
            body = self.format_arguments(body)

        if len(self.children) > 0:
            body = self.format_children(body)

        return body


class GraphQLOperation(GraphQLField):

    def __init__(self, action_type: OperationType, name: str, **kwargs):

        self.action_type = action_type.name.lower()
        nodes = {}
        super(GraphQLOperation, self).__init__(name, name, nodes, **kwargs)
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

