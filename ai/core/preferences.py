"""Default values for a group of agents."""


class Preferences(object):
    praiseworthiness_registry = None
    goodness_registry = None
    love_registry = None

    def __init__(self):
        self.praiseworthiness_registry = {}
        self.goodness_registry = {}
        self.love_registry = {}

    def register_action(self, action, p=0, g=0):
        """
        Register an action to a Preferences.
        action - the action being registered
        p - the praiseworthiness of the subject of action [-1, 1]
        g - the goodness of being the object of an action [-1, 1]
        """
        self._set_praiseworthiness(action, p)
        self._set_goodness(action, g)

    def register_entity(self, entity_id, l=0):
        """
        Register an entity to a Preferences.
        entity_id - the entity id being registered
        l - the love/hate of the entity. [-1, 1]
        """
        assert(isinstance(entity_id, basestring))
        self.set_love(entity_id, l)

    def set_praiseworthiness(self, action, p):
        """Set the default valence of being the subject of an action."""
        if p < -1 or p > 1:
            raise ValueError()
        self.praiseworthiness_registry[action.name] = p

    def get_praiseworthiness(self, action):
        if action.name in self.praiseworthiness_registry:
            return self.praiseworthiness_registry[action.name]
        else:
            raise KeyError(
                "%s not found. Use the set_praiseworthiness() method"
                " to associate a praiseworthiness with this action."
                % action.name
            )

    def set_goodness(self, action, g):
        """Set the default valence of being the object of an action."""
        if g < -1 or g > 1:
            raise ValueError()
        self.goodness_registry[action.name] = g

    def get_goodness(self, action):
        if action.name in self.goodness_registry:
            return self.goodness_registry[action.name]
        else:
            raise KeyError(
                "%s not found. Use the set_goodness() method"
                " to associate a goodness with this action."
                % action.name
            )

    def set_love(self, entity_id, l):
        """Set the default love/hate value of an entity id."""
        assert(isinstance(entity_id, basestring))
        if l < -1 or l > 1:
            raise ValueError()
        self.love_registry[entity_id] = l

    def get_love(self, entity_id):
        assert(isinstance(entity_id, basestring))
        if entity_id in self.love_registry:
            return self.love_registry[entity_id]
        else:
            raise KeyError(
                "%s not found. Use the set_love() method"
                " to associate a love level with this entity id."
                % entity_id
            )
