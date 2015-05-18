from mood import Mood


class Emotion(object):
    def __init__(self, amount):
        """amount - how acute is the emotional reaction."""
        self.amount = amount

    def _to_pad(self):
        raise NotImplementedError

    def to_mood(self):
        p, a, d = self._to_pad()
        mood = Mood(p, a, d)
        return mood


class Joy(Emotion):
    def _to_pad(self):
        return (.4, .2, .1)


class Hope(Emotion):
    def _to_pad(self):
        return (.2, .2, -.1)


class Relief(Emotion):
    def _to_pad(self):
        return (.2, -.3, .4)


class Pride(Emotion):
    def _to_pad(self):
        return (.4, .3, .3)


class Gratitude(Emotion):
    def _to_pad(self):
        return (.4, .2, -.3)


class Love(Emotion):
    def _to_pad(self):
        return (.3, .1, .2)


class HappyFor(Emotion):
    def _to_pad(self):
        return (.4, .2, .2)


class Gloating(Emotion):
    def _to_pad(self):
        return (.3, -.3, -.1)


class Distress(Emotion):
    def _to_pad(self):
        return (-.4, -.2, -.5)


class Fear(Emotion):
    def _to_pad(self):
        return (-.64, .6, -.43)


class Disappointment(Emotion):
    def _to_pad(self):
        return (-.3, .1, -.4)


class Remorse(Emotion):
    def _to_pad(self):
        return (-.3, .1, -.6)


class Anger(Emotion):
    def _to_pad(self):
        return (-.51, .59, .25)


class Hate(Emotion):
    def _to_pad(self):
        return (-.6, .6, .3)


class SorryFor(Emotion):
    def _to_pad(self):
        return (-.4, -.2, -.5)


class Resentment(Emotion):
    def _to_pad(self):
        return (-.2, -.3, -.2)
