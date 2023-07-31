import functools


def validate_kwargs_are_int(api, *validate_args):
    def decorator_validate(func):
        @api.response(400, "Validation Error")
        @functools.wraps(func)
        def wrapper_validate(*args, **kwargs):
            for validate_arg in validate_args:
                value = kwargs.get(validate_arg)
                try:
                    int(value)
                except ValueError:
                    api.abort(400, f"Path parameter '{validate_arg}' is not an integer")
            return func(*args, **kwargs)

        return wrapper_validate

    return decorator_validate
