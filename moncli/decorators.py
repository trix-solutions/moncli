def default_field_list(field_list: list):
    def wrap(func):
        def inner(instance, *args, **kwargs):
            for arg in args:
                # Execute function as is with input return fields if 
                # arg list contains default or nested field
                if arg in field_list or len(arg.split('.')) > 1:
                    return func(instance, *args, **kwargs)
            # Add field list if no args are present
            return func(instance, *args, *field_list, **kwargs)
        return inner         
    return wrap
