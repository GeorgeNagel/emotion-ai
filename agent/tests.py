from unittest import TestCase

from mood import Mood


class TestMood(TestCase):
    def test_str(self):
        mood = Mood(1, -1, 1)
        mood_string = str(mood)
        self.assertEqual(mood_string, "Relaxed")
