from unittest import TestCase

from ai.example.agent import ExampleAgent


class TestExampleAgent(TestCase):
    def test_entity_id(self):
        agent = ExampleAgent(0, 0, 0, 0, 0)
        uuid_plain = agent.entity_id
        agent.disguised = True
        uuid_disguised = agent.entity_id
        self.assertNotEqual(uuid_plain, uuid_disguised)
