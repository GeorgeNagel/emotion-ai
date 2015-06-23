import sys
print sys.path

from unittest import TestCase

from ai.core.agent import Agent
from ai.core.beliefs import Beliefs, EntityAttrBelief, \
    EntityEntityBelief, BeliefNotFound, RELATIONSHIPS
from ai.core.obj import Object


class TestBeliefs(TestCase):
    def test_register_entity(self):
        beliefs = Beliefs()
        entity = Object()
        self.assertEqual(beliefs.entities_count(), 0)
        beliefs.register_entity(entity.entity_id)
        self.assertEqual(beliefs.entities_count(), 1)

    def test_set_belief_unknown_entity(self):
        """
        Test an error is raised when setting a belief
        on an unregistered entity.
        """
        beliefs = Beliefs()
        entity = Object()
        belief = EntityAttrBelief(0, entity.entity_id, 'alive', True)
        with self.assertRaises(Exception):
            beliefs.set_belief(belief)

    def test_set_entity_attr_belief(self):
        """Test that you can set an EntityAttrBelief."""
        # Register an entity
        beliefs = Beliefs()
        entity = Object()
        beliefs.register_entity(entity.entity_id)
        # Set a belief
        self.assertEqual(beliefs.beliefs_count(), 0)
        belief_1 = EntityAttrBelief(0, entity.entity_id, 'alive', 1)
        beliefs.set_belief(belief_1)
        self.assertEqual(beliefs.beliefs_count(), 1)
        # Overwrite the belief
        belief_2 = EntityAttrBelief(1, entity.entity_id, 'alive', 0)
        beliefs.set_belief(belief_2)
        self.assertEqual(beliefs.beliefs_count(), 1)

    def test_set_entity_entity_belief(self):
        """Test that you can set an EntityEntityBelief."""
        # Register an entity
        beliefs = Beliefs()
        entity_1 = Object()
        entity_2 = Object()
        beliefs.register_entity(entity_1.entity_id)
        beliefs.register_entity(entity_2.entity_id)
        # Set a belief
        belief_1 = EntityEntityBelief(
            0, entity_1.entity_id, entity_2.entity_id, RELATIONSHIPS.IS, 1)
        beliefs.set_belief(belief_1)
        self.assertEqual(beliefs.beliefs_count(), 1)
        # Overwrite the belief
        belief_2 = EntityEntityBelief(
            1, entity_1.entity_id, entity_2.entity_id, RELATIONSHIPS.IS, 0)
        beliefs.set_belief(belief_2)
        self.assertEqual(beliefs.beliefs_count(), 1)

    def test_get_unknown_entity_attr(self):
        """
        Test that an exception is raised when getting an attr
        of an unknown entity.
        """
        beliefs = Beliefs()
        entity = Object()
        with self.assertRaises(Exception):
            beliefs.get_entity_attr(entity.entity_id, 'alive')

    def test_get_entity_attr_belief_not_found(self):
        """Test an exception is raised when no such belief exists."""
        beliefs = Beliefs()
        entity = Object()
        beliefs.register_entity(entity.entity_id)
        with self.assertRaises(BeliefNotFound):
            beliefs.get_entity_attr(entity.entity_id, 'likes_icecream')

    def test_get_entity_attr_belief(self):
        """Test that you can get entity attrs with defaults."""
        beliefs = Beliefs()
        entity = Object()
        beliefs.register_entity(entity.entity_id)
        # Set an attr belief
        belief = EntityAttrBelief(0, entity.entity_id, 'likes_icecream', 1)
        beliefs.set_belief(belief)
        # Get the attr back
        likes_icecream = beliefs.get_entity_attr(entity.entity_id, 'likes_icecream')
        self.assertEqual(likes_icecream, 1)
        # Get an unset attr with defaults
        alive = beliefs.get_entity_attr(entity.entity_id, 'alive', default=1)
        self.assertEqual(alive, 1)

    def test_revise_belief(self):
        """
        agent 1 believes red knight is dead.
        agent 1 believes agent 2 is alive.
        agent 1 then believes red knight is agent 2.
        agent 1 believes agent 2 is not alive.
        """
        agent_1 = Agent(0, 0, 0, 0, 0)
        red_knight_entity = Object()
        agent_2_entity = Object()
        agent_1.beliefs.register_entity(red_knight_entity.entity_id)
        agent_1.beliefs.register_entity(agent_2_entity.entity_id)
        # agent_1 beliefs agent_2 is alive
        agent_2_alive = EntityAttrBelief(0, agent_2_entity.entity_id, 'alive', 1)
        agent_1.beliefs.set_belief(agent_2_alive)

        # agent_1 believes red knight is not alive
        red_knight_dead = EntityAttrBelief(1, red_knight_entity.entity_id, 'alive', 0)
        agent_1.beliefs.set_belief(red_knight_dead)

        # agent_1 believes red knight is agent_2
        agent_1.beliefs.set_entity_is_entity(
            2, red_knight_entity.entity_id, agent_2_entity.entity_id, 1)

        # Check that agent 1 believes that agent 2 is not alive
        agent_2_alive = agent_1.beliefs.get_entity_attr(
            agent_2_entity.entity_id, 'alive')
        self.assertEqual(agent_2_alive, 0)

    def test_all_related_entities(self):
        """Test that all related entities are returned using 'is'."""
        beliefs = Beliefs()
        entity_1 = Object()
        beliefs.register_entity(entity_1.entity_id)
        entity_2 = Object()
        beliefs.register_entity(entity_2.entity_id)
        entity_3 = Object()
        beliefs.register_entity(entity_3.entity_id)

        beliefs.set_entity_is_entity(0, entity_1.entity_id, entity_2.entity_id, 1)
        beliefs.set_entity_is_entity(0, entity_2.entity_id, entity_3.entity_id, 1)

        related_entities = beliefs.get_related_entities(entity_1.entity_id)
        self.assertEqual(len(related_entities), 3)
        self.assertIn(entity_1.entity_id, related_entities)
        self.assertIn(entity_2.entity_id, related_entities)
        self.assertIn(entity_3.entity_id, related_entities)
