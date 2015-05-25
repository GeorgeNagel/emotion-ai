import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.culture import Culture


class TestSetPraiseworthiness(TestCase):
    def test_lower_limit(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            c.set_praiseworthiness(a, -20)
