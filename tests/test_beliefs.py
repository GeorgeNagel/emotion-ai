import sys
print sys.path

from unittest import TestCase

from ai.core.beliefs import Beliefs, Entity, EntityAttrBelief, \
    EntityEntityBelief, BeliefNotFound


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
        belief_1 = EntityAttrBelief(entity, 'alive', 1)
        beliefs.set_belief(belief_1)
        self.assertEqual(beliefs.beliefs_count(), 1)
        # Overwrite the belief
        belief_2 = EntityAttrBelief(entity, 'alive', 0)
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

    def test_get_unknown_entity_attr(self):
        """
        Test that an exception is raised when getting an attr
        of an unknown entity.
        """
        beliefs = Beliefs()
        entity = Entity()
        with self.assertRaises(Exception):
            beliefs.get_entity_attr(entity, 'alive')

    def test_get_entity_attr_belief_not_found(self):
        """Test an exception is raised when no such belief exists."""
        beliefs = Beliefs()
        entity = Entity()
        beliefs.register_entity(entity)
        with self.assertRaises(BeliefNotFound):
            beliefs.get_entity_attr(entity, 'likes_icecream')

    def test_get_entity_attr_belief(self):
        """Test that you can get entity attrs with defaults."""
        beliefs = Beliefs()
        entity = Entity()
        beliefs.register_entity(entity)
        # Set an attr belief
        belief = EntityAttrBelief(entity, 'likes_icecream', 1)
        beliefs.set_belief(belief)
        # Get the attr back
        likes_icecream = beliefs.get_entity_attr(entity, 'likes_icecream')
        self.assertEqual(likes_icecream, 1)
        # Get an unset attr with defaults
        alive = beliefs.get_entity_attr(entity, 'alive', default=1)
        self.assertEqual(alive, 1)

    def test_revise_belief(self):
        """
        agent 1 believes red knight is dead.
        agent 1 believes agent 2 is alive.
        agent 1 then believes red knight is agent 2.
        agent 1 believes agent 2 is not alive.
        """
        pass

    def test_entity_is_entity(self):
        """Test that entity 1 is entity 2 works."""
        pass
