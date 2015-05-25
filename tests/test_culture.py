import sys
print sys.path

from unittest import TestCase

from ai.core.action import Action
from ai.core.culture import Culture
from ai.core.obj import Object


class TestSetPraiseworthiness(TestCase):
    def test_lower_limit(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            c.set_praiseworthiness(a, -20)

    def test_upper_limit(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            c.set_praiseworthiness(a, 20)


class TestGetPraiseworthiness(TestCase):
    def test_get_praiseworthiness(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        c.set_praiseworthiness(a, 1)
        p = c.get_praiseworthiness(a)
        self.assertEqual(p, 1)


class TestSetGoodness(TestCase):
    def test_lower_limit(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            c.set_goodness(a, -20)

    def test_upper_limit(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        with self.assertRaises(ValueError):
            c.set_goodness(a, 20)


class TestGetGoodness(TestCase):
    def test_get_praiseworthiness(self):
        c = Culture()
        a = Action()
        a.name = "punch"
        c.set_goodness(a, 1)
        g = c.get_goodness(a)
        self.assertEqual(g, 1)


class TestSetLove(TestCase):
    def test_lower_limit(self):
        c = Culture()
        o = Object()
        with self.assertRaises(ValueError):
            c.set_love(o, -20)

    def test_upper_limit(self):
        c = Culture()
        o = Object()
        with self.assertRaises(ValueError):
            c.set_love(o, 20)


class TestGetLove(TestCase):
    def test_get_love(self):
        c = Culture()
        o = Object()
        c.set_love(o, 1)
        l = c.get_love(o)
        self.assertEqual(l, 1)
