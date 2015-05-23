import sys
print sys.path

from unittest import TestCase

from agent.agent import Agent
from agent.mood import Mood
from agent.obj import Object
from agent.personality import Personality


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


class TestFromPersonality(TestCase):
    """Create an agent given a personality."""
    def test_from_personality(self):
        personality = Personality(-1, -1, 1, -1, 1)
        agent = Agent.from_personality(personality)
        self.assertEqual(str(agent.mood), "Disdainful")


class TestSetLike(TestCase):
    def test_lower_limit(self):
        """set_like() should raise an error on values less than -1."""
        disliked_object = Object()
        agent = agent_factory()
        self.assertRaises(ValueError, agent.set_like(disliked_object, -20))

        # No error should be raised
        agent.set_like(disliked_object, -1)

    def test_upper_limit(self):
        """set_like() should raise an error on values greater than 1."""
        liked_object = Object()
        agent = agent_factory()
        self.assertRaises(ValueError, agent.set_like(liked_object, 20))

        # No error should be raised
        agent.set_like(liked_object, 1)


class TestGetLike(TestCase):
    def test_get_like(self):
        obj = Object()
        agent = agent_factory()
        agent.set_like(obj, 0.5)

        like_value = agent.get_like(obj)
        self.assertEqual(like_value, 0.5)
