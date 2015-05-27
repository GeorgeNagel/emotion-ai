import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.culture import Culture
from ai.core.emotion import Remorse, Gloating
from ai.core.mood import Mood


def agent_factory():
    mood = Mood(0, 0, 0)
    agent = Agent(mood)
    return agent


class TestInit(TestCase):
    def test_init(self):
        """New agents should have a uuid."""
        a = agent_factory()
        uuid = getattr(a, "uuid")
        self.assertIsInstance(uuid, basestring)


class TestFromOCEAN(TestCase):
    """Create an agent given a personality."""
    def test_from_OCEAN(self):
        agent = Agent.from_OCEAN(-1, -1, 1, -1, 1)
        self.assertEqual(str(agent.mood), "Disdainful")


class TestCulture(TestCase):
    def test_set_get(self):
        c = Culture()
        a = agent_factory()
        a.set_culture(c)
        c_returned = a.get_culture()
        self.assertEqual(c, c_returned)


class TestEmotionsForObservedAction(TestCase):
    def test_emotions_for_observed_action(self):
        c = Culture()
        agent_1 = agent_factory()
        agent_1.set_culture(c)
        agent_2 = agent_factory()
        agent_2.set_culture(c)
        action = Action()
        action.name = "Hit"
        c.set_goodness(action, -.5)
        c.set_praiseworthiness(action, -1)
        c.set_love(agent_2, -.5)

        emotions = agent_1._emotions_for_observed_action(
            action, agent_1, agent_2
        )
        emotion_1 = emotions.pop()
        self.assertIsInstance(emotion_1, Gloating)
        self.assertEqual(emotion_1.amount, .25)
        emotion_2 = emotions.pop()
        self.assertIsInstance(emotion_2, Remorse)
        self.assertEqual(emotion_2.amount, 1)
