from unittest import TestCase

from ai.core.emotion import Gloating
from ai.core.mood import Mood


class TestMood(TestCase):
    def test_str(self):
        mood = Mood(1, -1, 1)
        mood_string = str(mood)
        self.assertEqual(mood_string, "Relaxed")

    def test_update_from_emotions(self):
        mood = Mood(.1, .1, .1)
        self.assertEqual(str(mood), "Exuberant")
        emotion = Gloating(.5)
        mood.update_from_emotions([emotion])
        self.assertEqual(str(mood), "Relaxed")
