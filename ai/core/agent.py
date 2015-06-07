from ai.core.beliefs import Beliefs
from ai.core.emotion import Love, Hate, Pride, Remorse, Anger, Gratitude, \
    HappyFor, SorryFor, Gloating, Resentment, Joy, Distress, Hope, Fear, \
    Relief, Disappointment
from ai.core.preferences import Preferences
from ai.core.personality import Personality
from ai.core.obj import Object

EMOTION_THRESHOLD = .01


class Agent(Object):
    """An object that has a mood."""
    culture = None
    beliefs = None

    def __init__(self, o, c, e, a, n):
        self.personality = Personality(o, c, e, a, n)
        self.mood = self.personality.to_mood()
        self.emotions = []
        # Like/dislike relationships with objects
        self.relationships = {}
        self.beliefs = Beliefs()
        super(Agent, self).__init__()

    def set_preferences(self, preferences):
        assert(isinstance(preferences, Preferences))
        self.preferences = preferences

    def get_preferences(self):
        return self.preferences

    def emotions_for_object(self, obj):
        emotions = []
        c = self.get_culture()
        l = c.get_love(obj)
        if l > 0:
            e = Love(l)
            emotions.append(e)
        if l < 0:
            e = Hate(l)
            emotions.append(e)
        return emotions

    def emotions_for_action(self, action, agent, obj, prob, prior_prob=None):
        """
        Generate a list of emotions for actions based on
        probability of the action happening.
        """
        emotions = []
        # Calculate the expected joy/distress at an event's success
        joy_distress = self._expected_joy_distress(action, agent, obj)
        if prob > 0 and prob < 1:
            if 'joy' in joy_distress:
                # Possible joyful event
                j = joy_distress['joy']
                e = Hope(j*prob)
                emotions.append(e)
            if 'distress' in joy_distress:
                # Possible distressing event
                d = joy_distress['distress']
                e = Fear(d*prob)
                emotions.append(e)

        if prob == 0 and prior_prob is not None:
            if prior_prob > 0:
                # Disconfirmed hope/fear
                if 'joy' in joy_distress:
                    # Disconfirmed hoped-for outcome
                    j = joy_distress['joy']
                    e = Disappointment(j*prior_prob)
                    emotions.append(e)
                if 'distress' in joy_distress:
                    # Disconfirmed feared outcome
                    d = joy_distress['distress']
                    e = Relief(j*prior_prob)
                    emotions.append(e)

        if prob == 1:
            confirmed_outcome_emotions = self._emotions_for_observed_action(
                action, agent, obj
            )
            emotions.extend(confirmed_outcome_emotions)

    def _expected_joy_distress(self, action, agent, obj):
        """Calculate the expected joy and distress at an actions success."""
        emotions = self.emotions_for_observed_action(action, agent, obj)
        j = None
        d = None
        for e in emotions:
            if isinstance(e, Joy):
                j = e.amount
            if isinstance(e, Distress):
                d = e.amount
        hope_fear = {}
        if j:
            hope_fear['joy'] = j
        if d:
            hope_fear['distress'] = d
        return hope_fear

    def _emotions_for_observed_action(self, action, agent, obj):
        emotions = []
        preferences = self.get_preferences()
        if preferences is None:
            raise Exception("Cannot calculate emotions without a culture.")

        p = preferences.get_praiseworthiness(action)
        g = preferences.get_goodness(action)
        l = preferences.get_love(obj)

        if agent == self:
            # Self-initiated
            if p > 0:
                # Praiseworthy
                e = Pride(p)
                emotions.append(e)
            if p < 0:
                # Shameworthy
                e = Remorse(-1*p)
                emotions.append(e)
        else:
            # Other-initiaed
            if p > 0:
                # Praiseworthy
                e = Gratitude(p)
                emotions.append(e)
            if p < 0:
                # Shameworthy
                e = Anger(-1*p)
                emotions.append(e)

        if isinstance(obj, Agent):
            if obj == self:
                if g > 0:
                    # Good thing happened
                    e = Joy(g)
                    emotions.append(e)
                if g < 0:
                    # Bad thing happened
                    e = Distress(-1*g)
                    emotions.append(e)
            else:
                if l > 0:
                    # Something happened to a liked agent
                    if g > 0:
                        # Good thing happened
                        e = HappyFor(l*g)
                        emotions.append(e)
                    if g < 0:
                        # Bad thing happened
                        e = SorryFor(l*g*-1)
                        emotions.append(e)
                if l < 0:
                    # Something happened to a disliked agent
                    if g > 0:
                        # Good thing happened
                        e = Resentment(-1*l*g)
                        emotions.append(e)
                    if g < 0:
                        # Bad thing happened
                        e = Gloating(l*g)
                        emotions.append(e)
        return emotions

    def tick_mood(self):
        """Update mood state."""
        # Decay emotion amounts
        decayed_emotions = []
        for emotion in self.emotions:
            emotion.amount /= 2
            # Remove any emotions below the perceptible threshold
            if emotion.amount > EMOTION_THRESHOLD:
                decayed_emotions.append(emotion)
        self.emotions = decayed_emotions

        # Set a new mood based on decayed emotions
        mood = self.personality.to_mood()
        mood.update_from_emotions(decayed_emotions)
        self.mood = mood
