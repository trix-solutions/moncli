import copy

def default_field_list(field_list: list):
    def wrap(func):
        def inner(instance, *args, **kwargs):
            for arg in args:
                # Input arg list contains a default field
                if arg in field_list:
                    return func(instance, *args, **kwargs)
                # Input arg list contains a nested field
                if type(arg) is str and len(arg.split('.')) > 1:
                    return func(instance, *args, **kwargs)
            # Add field list if no args are present
            args = (*args, *field_list)
            return func(instance, *args, **kwargs)
        return inner         
    return wrap

def optional_arguments(arguments: dict):
    def wrap(func):
        def inner(instance, *args, **kwargs):
            # This loop prevents decorator from breaking when required params are used as kwargs.
            for key in [key for key in kwargs.keys()]:
                if key not in arguments.keys():
                    args = (*args, kwargs.pop(key))
            return func(instance, *args, **kwargs)
        return inner
    return wrap