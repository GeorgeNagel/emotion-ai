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
