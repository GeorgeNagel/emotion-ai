from functools import wraps

from agent.obj import clean_objects_registry


def clean_obj_registry(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Bomb the object_registry for tests
        clean_objects_registry()
        return f(*args, **kwargs)
    return wrapper
