import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.preferences import Preferences
from ai.core.obj import Object


class TestSetPraiseworthiness(TestCase):
    def test_lower_limit(self):
        p = Preferences()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            p.set_praiseworthiness(a, -20)

    def test_upper_limit(self):
        p = Preferences()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            p.set_praiseworthiness(a, 20)


class TestGetPraiseworthiness(TestCase):
    def test_get_praiseworthiness(self):
        p = Preferences()
        a = Action()
        a.name = "punch"
        p.set_praiseworthiness(a, 1)
        p = p.get_praiseworthiness(a)
        self.assertEqual(p, 1)


class TestSetGoodness(TestCase):
    def test_lower_limit(self):
        p = Preferences()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            p.set_goodness(a, -20)

    def test_upper_limit(self):
        p = Preferences()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            p.set_goodness(a, 20)


class TestGetGoodness(TestCase):
    def test_get_praiseworthiness(self):
        p = Preferences()
        a = Action()
        a.name = "punch"
        p.set_goodness(a, 1)
        g = p.get_goodness(a)
        self.assertEqual(g, 1)


class TestSetLove(TestCase):
    def test_lower_limit(self):
        p = Preferences()
        o = Object()
        with self.assertRaises(ValueError):
            p.set_love(o, -20)

    def test_upper_limit(self):
        p = Preferences()
        o = Object()
        with self.assertRaises(ValueError):
            p.set_love(o, 20)


class TestGetLove(TestCase):
    def test_get_love(self):
        p = Preferences()
        o = Object()
        p.set_love(o, 1)
        l = p.get_love(o)
        self.assertEqual(l, 1)
