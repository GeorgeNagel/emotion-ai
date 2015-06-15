from ai.core.preferences import Preferences
from ai.example.action import Kill


culture = Preferences()
culture.set_praiseworthiness(Kill, 1)
culture.set_goodness(Kill, 1)
