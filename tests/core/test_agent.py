import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.beliefs import Beliefs
from ai.core.emotion import Joy, Remorse, Gloating, Anger, SorryFor, Distress
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
        emotions = observer.emotions_for_action(
            hit, subject.entity_id, obj.entity_id, prob)
        self.assertEqual(len(emotions), 2)
        self.assertIsInstance(emotions[0], Anger)
        self.assertIsInstance(emotions[1], Gloating)

    def test_emotions_for_multiple_object_entities(self):
        """Test emotions for an object represented as multiple entities."""
        hit = Action()
        hit.name = "Hit"
        object_entity_id_1 = '123a'
        object_entity_id_2 = '123b'
        subject_entity_id = '456'
        observer = Agent(0, 0, 0, 0, 0)

        preferences = observer.get_preferences()
        preferences.set_goodness(hit, -1)
        preferences.set_praiseworthiness(hit, -1)
        preferences.set_love(object_entity_id_1, 1)
        preferences.set_love(object_entity_id_2, -1)
        preferences.set_love(subject_entity_id, 1)

        timestamp = 0
        truth_value = 1
        observer.beliefs.register_entity(object_entity_id_1)
        observer.beliefs.register_entity(object_entity_id_2)
        observer.beliefs.set_entity_is_entity(
            timestamp, object_entity_id_1, object_entity_id_2, truth_value
        )

        prob = 1
        emotions = observer.emotions_for_action(
            hit,
            subject_entity_id,
            object_entity_id_1,
            prob)

        self.assertEqual(len(emotions), 3)
        # Anger towards the person who hit (a bad thing to do)
        self.assertIsInstance(emotions[0], Anger)
        # Sorry for the loved person being hit
        self.assertIsInstance(emotions[1], SorryFor)
        # Gloating over the hated person being hit
        self.assertIsInstance(emotions[2], Gloating)

    def test_emotions_self_action(self):
        """Test emotions for an action by an agent with multiple entities."""
        hit = Action()
        hit.name = "Hit"
        agent = Agent(0, 0, 0, 0, 0)
        agent_entity_id_1 = agent.entity_id
        agent_entity_id_2 = 'test_123'

        preferences = agent.get_preferences()
        preferences.set_goodness(hit, -1)
        preferences.set_praiseworthiness(hit, -1)
        preferences.set_love(agent_entity_id_1, 1)
        preferences.set_love(agent_entity_id_2, 1)

        timestamp = 0
        truth_value = 1
        agent.beliefs.register_entity(agent_entity_id_1)
        agent.beliefs.register_entity(agent_entity_id_2)
        agent.beliefs.set_entity_is_entity(
            timestamp, agent_entity_id_1, agent_entity_id_2, truth_value
        )

        prob = 1
        emotions = agent.emotions_for_action(
            hit,
            agent_entity_id_1,
            agent_entity_id_2,
            prob)

        self.assertEqual(len(emotions), 2)
        # Feeling bad for hitting someone agent loves (agent)
        self.assertIsInstance(emotions[0], Remorse)
        # Feeling bad for being hit (by agent)
        self.assertIsInstance(emotions[1], Distress)

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
