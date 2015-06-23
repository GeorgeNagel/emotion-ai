import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.beliefs import Beliefs
from ai.core.emotion import Joy, Remorse, Gloating, Anger
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
        action = Action()
        action.name = "test_action"
        p = Preferences()
        p.set_goodness(action, 1)
        agent = Agent(0, 0, 0, 0, 0)
        agent.set_preferences(p)

        p_returned = agent.get_preferences()
        self.assertEqual(p_returned.get_goodness(action), 1)

    def test_emotions_for_observed_action(self):
        agent_1 = Agent(0, 0, 0, 0, 0)
        agent_2 = Agent(-1, -1, 1, -1, 1)
        action = Action()
        action.name = "Hit"

        p = Preferences()
        p.set_goodness(action, -.5)
        p.set_praiseworthiness(action, -1)
        p.set_love(agent_2.entity_id, -.5)

        agent_1.set_preferences(p)
        agent_2.set_preferences(p)

        emotions = agent_1._emotions_for_observed_action(
            action, agent_1.entity_id, agent_2.entity_id
        )
        self.assertEqual(len(emotions), 2)
        emotion_1 = emotions.pop()
        self.assertIsInstance(emotion_1, Gloating)
        self.assertEqual(emotion_1.amount, .25)
        emotion_2 = emotions.pop()
        self.assertIsInstance(emotion_2, Remorse)
        self.assertEqual(emotion_2.amount, 1)

    def test_emotions_for_action(self):
        subject = Agent(0, 0, 0, 0, 0)
        obj = Agent(0, 0, 0, 0, 0)
        observer = Agent(0, 0, 0, 0, 0)

        hit = Action()
        hit.name = "Hit"

        preferences = observer.get_preferences()
        preferences.set_goodness(hit, -1)
        preferences.set_praiseworthiness(hit, -1)
        preferences.set_love(subject.entity_id, 1)
        preferences.set_love(obj.entity_id, -1)

        prob = 1
        emotions = observer.emotions_for_action(hit, subject.entity_id, obj.entity_id, prob)
        self.assertEqual(len(emotions), 2)
        self.assertIsInstance(emotions[0], Anger)
        self.assertIsInstance(emotions[1], Gloating)

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

    def test_create_random_agent(self):
        agent = Agent.create_random_agent()
        self.assertIsInstance(agent.name, basestring)
