import sys
print sys.path

from unittest import TestCase

from ai.core.beliefs import Beliefs, Entity, \
    EntityAttrBelief, EntityEntityBelief


class TestBeliefs(TestCase):
    def test_register_entity(self):
        beliefs = Beliefs()
        entity = Entity()
        self.assertEqual(beliefs.entities_count(), 0)
        beliefs.register_entity(entity)
        self.assertEqual(beliefs.entities_count(), 1)

    def test_set_belief_unknown_entity(self):
        """
        Test an error is raised when setting a belief
        on an unregistered entity.
        """
        beliefs = Beliefs()
        entity = Entity()
        belief = EntityAttrBelief(entity, 'alive', True)
        with self.assertRaises(Exception):
            beliefs.set_belief(belief)

    def test_set_entity_attr_belief(self):
        """Test that you can set an EntityAttrBelief."""
        # Register an entity
        beliefs = Beliefs()
        entity = Entity()
        beliefs.register_entity(entity)
        # Set a belief
        self.assertEqual(beliefs.beliefs_count(), 0)
        belief_1 = EntityAttrBelief(entity, 'alive', True)
        beliefs.set_belief(belief_1)
        self.assertEqual(beliefs.beliefs_count(), 1)
        # Overwrite the belief
        belief_2 = EntityAttrBelief(entity, 'alive', False)
        beliefs.set_belief(belief_2)
        self.assertEqual(beliefs.beliefs_count(), 1)

    def test_set_entity_entity_belief(self):
        """Test that you can set an EntityEntityBelief."""
        # Register an entity
        beliefs = Beliefs()
        entity_1 = Entity()
        entity_2 = Entity()
        beliefs.register_entity(entity_1)
        beliefs.register_entity(entity_2)
        # Set a belief
        belief_1 = EntityEntityBelief(entity_1, entity_2, 'is', 1)
        beliefs.set_belief(belief_1)
        self.assertEqual(beliefs.beliefs_count(), 1)
        # Overwrite the belief
        belief_2 = EntityEntityBelief(entity_1, entity_2, 'is', 0)
        beliefs.set_belief(belief_2)
        self.assertEqual(beliefs.beliefs_count(), 1)

    def test_revise_belief(self):
        """
        agent 1 kills red knight.
        agent 1 believes agent 2 is alive.
        agent 1 then believes red knight is agent 2.
        agent 1 believes agent 2 is not alive.
        """
        pass

    def test_entity_is_entity(self):
        """Test that entity 1 is entity 2 works."""
        pass
