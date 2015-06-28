from copy import deepcopy
import random

from ai.core.beliefs import Beliefs
from ai.core.emotion import Love, Hate, Pride, Remorse, Anger, Gratitude, \
    HappyFor, SorryFor, Gloating, Resentment, Joy, Distress, Hope, Fear, \
    Relief, Disappointment
from ai.core.preferences import Preferences
from ai.core.personality import Personality
from ai.core.obj import Object
from ai.name_gen.new_names import generate_names

EMOTION_THRESHOLD = .01


class GENDERS(object):
    MALE = 'male'
    FEMALE = 'female'


class Agent(Object):
    """An object that has a mood."""
    beliefs = None
    children = None
    culture = None
    emotions = None
    mood = None
    parents = None
    personality = None
    _preferences = None

    def __init__(self, o, c, e, a, n):
        self.personality = Personality(o, c, e, a, n)
        self.mood = self.personality.to_mood()
        self.emotions = []
        # Like/dislike relationships with objects
        self.relationships = {}
        self.beliefs = Beliefs()
        self.children = []
        super(Agent, self).__init__()

    def __str__(self):
        return self.name

    @classmethod
    def from_personality(cls, p):
        agent = Agent(p.o, p.c, p.e, p.a, p.n)
        return agent

    def set_preferences(self, preferences):
        agent_preferences = deepcopy(preferences)
        assert(isinstance(agent_preferences, Preferences))
        self._preferences = agent_preferences

    def get_preferences(self):
        if self._preferences is None:
            self._preferences = Preferences()
        return self._preferences

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

    def emotions_for_action(self, action, agent_entity_id,
                            obj_entity_id, prob, prior_prob=None):
        """
        Generate a list of emotions for actions based on
        probability of the action happening.
        """
        assert(isinstance(agent_entity_id, basestring))
        assert(isinstance(obj_entity_id, basestring))
        emotions = []
        # Calculate the expected joy/distress at an event's success
        joy_distress = self._expected_joy_distress(
            action, agent_entity_id, obj_entity_id)
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
                action, agent_entity_id, obj_entity_id
            )
            emotions.extend(confirmed_outcome_emotions)
        return emotions

    def _expected_joy_distress(self, action, agent_entity_id, obj_entity_id):
        """Calculate the expected joy and distress at an actions success."""
        assert(isinstance(agent_entity_id, basestring))
        assert(isinstance(obj_entity_id, basestring))
        emotions = self._emotions_for_observed_action(
            action, agent_entity_id, obj_entity_id)
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

    def _emotions_for_observed_action(self, action, agent_entity_id,
                                      obj_entity_id):
        agent_emotions = self._action_agent_emotions(action, agent_entity_id)
        obj_emotions = self._action_object_emotions(action, obj_entity_id)
        emotions = agent_emotions + obj_emotions
        return emotions

    def _action_agent_emotions(self, action, agent_entity_id):
        assert(isinstance(agent_entity_id, basestring))
        preferences = self.get_preferences()
        if preferences is None:
            raise Exception("Cannot calculate emotions without a culture.")

        p = preferences.get_praiseworthiness(action)
        emotions = []
        related_entities = self.beliefs.get_related_entities(agent_entity_id)
        # Only count emotions for self once
        if self.entity_id in related_entities:
            related_entities = [self.entity_id]
        # Cycle through for emotions felt about related entities (ones who
        # represent the same agent as the one the action happened to.)
        for related_agent_entity_id in related_entities:
            if agent_entity_id == self.entity_id:
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
        return emotions

    def _action_object_emotions(self, action, obj_entity_id):
        assert(isinstance(obj_entity_id, basestring))
        preferences = self.get_preferences()
        if preferences is None:
            raise Exception("Cannot calculate emotions without a culture.")
        g = preferences.get_goodness(action)
        emotions = []
        related_entities = self.beliefs.get_related_entities(obj_entity_id)
        # Only count emotions felt for self once
        if self.entity_id in related_entities:
            related_entities = [self.entity_id]
        # Loop through all entities that are the same concept and return
        # any emotions the action induces. For example, if The Red Knight is
        # terrible but turns out to be the same as Lancelot, when Lancelot is
        # hurt, people will feel bad for him as Lancelot (a good guy) but will
        # gloat over the bad thing happening to the person they knew as The Red
        # Knight.
        for related_obj_entity_id in related_entities:
            l = preferences.get_love(related_obj_entity_id)
            if related_obj_entity_id == self.entity_id:
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

    def set_parents(self, parent_1, parent_2):
        if not isinstance(parent_1, Agent) or not isinstance(parent_2, Agent):
            raise ValueError("Parents must be agents")
        self.parents = [parent_1, parent_2]

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    @classmethod
    def create_random_agent(cls, gender=None):
        """Create a first-generation agent."""
        # Randomize the personality
        o = random.random()*2 - 1
        c = random.random()*2 - 1
        e = random.random()*2 - 1
        a = random.random()*2 - 1
        n = random.random()*2 - 1
        agent = cls(o, c, e, a, n)
        if gender is None:
            gender = random.choice([GENDERS.MALE, GENDERS.FEMALE])
        agent.gender = gender
        agent.name = generate_names(gender, 1)[0]
        return agent
