from mood import Mood


class Personality(object):
    """
    OCEAN long-term mental state.
    o - Openness
    c - Conscientiousness
    e - Extraversion
    a - Agreeableness
    n - Neuroticism
    """
    def __init__(self, o, c, e, a, n):
        self.o = o
        self.c = c
        self.e = e
        self.a = a
        self.n = n

    def _to_pad(self):
        """
        Convert the OCEAN mood to PAD space.

        http://infoscience.epfl.ch/record/199429/files/510.pdf
        pg. 24
        """
        p = .21*self.e + .59*self.a + .19*self.n
        a = .15*self.o + .30*self.a - .57*self.n
        d = .25*self.o + .17*self.c + .6*self.e - .32*self.a
        return (p, a, d)

    def to_mood(self):
        p, a, d = self._to_pad()
        mood = Mood(p, a, d)
        return mood
