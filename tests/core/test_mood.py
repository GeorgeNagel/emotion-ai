from unittest import TestCase

from ai.core.emotion import Gloating
from ai.core.mood import Mood


class TestMood(TestCase):
    def test_str(self):
        mood = Mood(1, -1, 1)
        mood_string = str(mood)
        self.assertEqual(mood_string, "Relaxed (1.73205080757)")

    def test_type(self):
        mood = Mood(1, -1, 1)
        self.assertEqual(mood.type, "Relaxed")

    def test_update_from_emotions(self):
        mood = Mood(.1, .1, .1)
        self.assertEqual(mood.type, "Exuberant")
        emotion = Gloating(.5)
        mood.update_from_emotions([emotion])
        self.assertEqual(mood.type, "Relaxed")
