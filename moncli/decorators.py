import copy

def default_field_list(field_list: list):
    def wrap(func):
        def inner(instance, *args, **kwargs):
            # This loop prevents duplicate args and kwargs from messing up the decorator.
            for key in [key for key in kwargs.keys()]:
                if key in args or key in field_list:
                    args = (*args, kwargs.pop(key))
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
