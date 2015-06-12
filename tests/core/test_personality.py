from unittest import TestCase

from ai.core.personality import Personality, combine_personalities


class TestPersonality(TestCase):
    def test_combine_personalities(self):
        p1 = Personality(0, 0, 0, 0, 0)
        p2 = Personality(1, 1, 1, 1, 1)
        variation = 0
        p3 = combine_personalities(p1, p2, variation)

        assert(p1.o <= p3.o <= p2.o)
        assert(p1.c <= p3.c <= p2.c)
        assert(p1.e <= p3.e <= p2.e)
        assert(p1.a <= p3.a <= p2.a)
        assert(p1.n <= p3.n <= p2.n)
