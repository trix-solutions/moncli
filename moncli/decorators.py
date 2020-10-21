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