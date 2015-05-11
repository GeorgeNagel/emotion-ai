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

    def to_pad(self):
        """
        Convert the OCEAN mood to PAD space.

        http://infoscience.epfl.ch/record/199429/files/510.pdf
        pg. 24
        """
        p = .21*self.e + .59*self.a + .19*self.n
        a = .15*self.o + .30*self.a - .57*self.n
        d = .25*self.o + .17*self.c + .6*self.e - .32*self.a
        return (p, a, d)


class Mood(object):
    """
    PAD mid-term mental state.
    p - Pleasure
    a - Arousal
    d - Dominance
    """
    def __init__(self, p, a, d):
        self.p = p
        self.a = a
        self.d = d

    def __str__(self):
        """
        Value to return when cast to a string.

        http://infoscience.epfl.ch/record/199429/files/510.pdf
        pg. 24.
        """
        if self.p >= 0:
            if self.a >= 0:
                if self.d >= 0:
                    return "Exuberant"
                else:
                    return "Dependent"
            else:
                if self.d >= 0:
                    return "Relaxed"
                else:
                    return "Docile"
        else:
            if self.a >= 0:
                if self.d >= 0:
                    return "Hostile"
                else:
                    return "Anxious"
            else:
                if self.d >= 0:
                    return "Disdainful"
                else:
                    return "Bored"


class Agent(object):
    def __init__(self, Mood):
        self.Mood = Mood
