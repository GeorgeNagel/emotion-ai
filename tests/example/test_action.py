from unittest import TestCase

from ai.core.agent import Agent
from ai.example.action import apply_action, Kill


class TestAction(TestCase):
    def test_apply_action(self):
        subject_agent = Agent(0, 0, 0, 0, 0)
        object_agent = Agent(0, 0, 0, 0, 0)
        viewer_agent = Agent(0, 0, 0, 0, 0)
        viewer_preferences = viewer_agent.get_preferences()
        viewer_preferences.set_love(subject_agent, 1)
        viewer_preferences.set_love(object_agent, 1)
        viewer_preferences.set_praiseworthiness(Kill, -1)
        viewer_preferences.set_goodness(Kill, -1)
        apply_action(
            action=Kill,
            subject=subject_agent,
            obj=object_agent,
            viewers=[viewer_agent]
        )
        self.assertEqual(len(viewer_agent.emotions), 2)
