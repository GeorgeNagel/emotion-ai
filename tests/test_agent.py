import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.preferences import Preferences
from ai.core.emotion import Remorse, Gloating


class TestInit(TestCase):
    def test_init(self):
        """New agents should have a uuid."""
        agent = Agent.from_OCEAN(0, 0, 0, 0, 0)
        uuid = getattr(agent, "uuid")
        self.assertIsInstance(uuid, basestring)


class TestFromOCEAN(TestCase):
    """Create an agent given a personality."""
    def test_from_OCEAN(self):
        agent = Agent.from_OCEAN(-1, -1, 1, -1, 1)
        self.assertEqual(str(agent.mood), "Disdainful")


class TestPreferences(TestCase):
    def test_set_get(self):
        p = Preferences()
        agent = Agent.from_OCEAN(0, 0, 0, 0, 0)
        agent.set_preferences(p)
        p_returned = agent.get_preferences()
        self.assertEqual(p, p_returned)


class TestEmotionsForObservedAction(TestCase):
    def test_emotions_for_observed_action(self):
        p = Preferences()
        agent_1 = Agent.from_OCEAN(0, 0, 0, 0, 0)
        agent_1.set_preferences(p)
        agent_2 = Agent.from_OCEAN(-1, -1, 1, -1, 1)
        agent_2.set_preferences(p)
        action = Action()
        action.name = "Hit"
        p.set_goodness(action, -.5)
        p.set_praiseworthiness(action, -1)
        p.set_love(agent_2, -.5)

        emotions = agent_1._emotions_for_observed_action(
            action, agent_1, agent_2
        )
        emotion_1 = emotions.pop()
        self.assertIsInstance(emotion_1, Gloating)
        self.assertEqual(emotion_1.amount, .25)
        emotion_2 = emotions.pop()
        self.assertIsInstance(emotion_2, Remorse)
        self.assertEqual(emotion_2.amount, 1)
