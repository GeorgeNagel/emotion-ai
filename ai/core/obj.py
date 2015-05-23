from functools import wraps
from weakref import WeakValueDictionary
import uuid

# A mapping of object uuids to objects
# This is the representation of all objects that "exist"
# Use a WeakValueDictionary to auto-delete object references
# where this is the last reference
object_registry = WeakValueDictionary()


def clean_obj_registry(f):
    """Decorator for cleaning the object registry in tests."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Bomb the object_registry for tests
        global object_registry
        object_registry = WeakValueDictionary()
        return f(*args, **kwargs)
    return wrapper


class Object(object):
    """A "thing" which can be liked/disliked"""
    def __init__(self):
        """Ensure a uuid for each object."""
        unique_id = str(uuid.uuid1())
        while unique_id in object_registry:
            unique_id = str(uuid.uuid1())
        self.uuid = unique_id
        # Register the object
        object_registry[self.uuid] = self
