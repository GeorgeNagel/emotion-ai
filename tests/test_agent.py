import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.beliefs import Beliefs
from ai.core.emotion import Joy, Remorse, Gloating
from ai.core.preferences import Preferences


class TestAgent(TestCase):
    def test_uuid(self):
        """New agents should have a uuid."""
        agent = Agent(0, 0, 0, 0, 0)
        uuid = getattr(agent, "uuid")
        self.assertIsInstance(uuid, basestring)

    def test_beliefs(self):
        """New agents should have beliefs."""
        agent = Agent(0, 0, 0, 0, 0)
        self.assertIsInstance(agent.beliefs, Beliefs)

    def test_from_OCEAN(self):
        """Create an agent given a personality."""
        agent = Agent(-1, -1, 1, -1, 1)
        self.assertEqual(str(agent.mood), "Disdainful")

    def test_set_get_preferences(self):
        p = Preferences()
        agent = Agent(0, 0, 0, 0, 0)
        agent.set_preferences(p)
        p_returned = agent.get_preferences()
        self.assertEqual(p, p_returned)

    def test_emotions_for_observed_action(self):
        p = Preferences()
        agent_1 = Agent(0, 0, 0, 0, 0)
        agent_1.set_preferences(p)
        agent_2 = Agent(-1, -1, 1, -1, 1)
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

    def test_tick_mood(self):
        agent = Agent(.01, -.01, .01, -.01, .01)
        self.assertEqual(str(agent.mood), "Disdainful")
        agent.emotions = [Joy(.05)]

        agent.tick_mood()
        self.assertEqual(len(agent.emotions), 1)
        self.assertEqual(agent.emotions[0].amount, .025)
        self.assertEqual(str(agent.mood), "Relaxed")

        # After enough ticks, the emotion should be removed from memory
        agent.tick_mood()
        agent.tick_mood()
        self.assertEqual(len(agent.emotions), 0)
        self.assertEqual(str(agent.mood), "Disdainful")
