"""Default values for a group of agents."""


class Culture(object):
    praiseworthiness_registry = None
    goodness_registry = None
    love_registry = None

    def __init__(self):
        self.praiseworthiness_registry = {}
        self.goodness_registry = {}
        self.love_registry = {}

    def register_action(self, action, p=0, g=0):
        """
        Register an action to a culture.
        action - the action being registered
        p - the praiseworthiness of the subject of action [-1, 1]
        g - the goodness of being the object of an action [-1, 1]
        """
        self._set_praiseworthiness(action, p)
        self._set_goodness(action, g)

    def register_object(self, obj, l=0):
        """
        Register an object to a culture.
        obj - the object being registered
        l - the love/hate of the object. [-1, 1]
        """
        self._set_love(obj, l)

    def set_praiseworthiness(self, action, p):
        """Set the default valence of being the subject of an action."""
        if p < -1 or p > 1:
            raise ValueError()
        self.praiseworthiness_registry[action.name] = p

    def get_praiseworthiness(self, action):
        return self.praiseworthiness_registry[action.name]

    def set_goodness(self, action, g):
        """Set the default valence of being the object of an action."""
        if g < -1 or g > 1:
            raise ValueError()
        self.goodness_registry[action.name] = g

    def get_goodness(self, action):
        return self.goodness_registry[action.name]

    def set_love(self, obj, l):
        """Set the default love/hate value of an object."""
        if l < -1 or l > 1:
            raise ValueError()
        self.love_registry[obj.uuid] = l

    def get_love(self, obj):
        return self.love_registry[obj.uuid]
