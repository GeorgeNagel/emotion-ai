from obj import Object


class Agent(Object):
    """An object that has a mood."""

    def __init__(self, Mood):
        self.mood = Mood
        # Like/dislike relationships with objects
        self.relationships = {}
        super(Agent, self).__init__()

    @classmethod
    def from_personality(self, personality):
        mood = personality.to_mood()
        return Agent(mood)

    def set_like(self, obj, value):
        """
        Set the like/dislike value for an object.
        Must be -1 <= x <= 1
        """
        if value < -1 or value > 1:
            raise ValueError()
        self.relationships[obj.uuid] = value

    def get_like(self, obj):
        """
        Get the like/dislike value for an object.
        -1 <= x <= 1
        """
        return self.relationships[obj.uuid]
