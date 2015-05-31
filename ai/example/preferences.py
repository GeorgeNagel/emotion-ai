from ai.core.preferences import Preferences
from ai.example.action import Hug, Slap


culture = Preferences()
culture.set_praiseworthiness(Hug, 1)
culture.set_goodness(Hug, 1)
culture.set_praiseworthiness(Slap, -1)
culture.set_goodness(Slap, -1)
