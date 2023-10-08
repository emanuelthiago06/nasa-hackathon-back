def authenticate(instance, value):
    try:
        new_val = instance(value)
    except TypeError:
        return None
    return new_val