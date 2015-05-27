from unittest import TestCase

from ai.core.emotion import Joy


class TestEmotion(TestCase):
    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            # Instantiate an emotion with an invalid amount
            Joy(-1)
