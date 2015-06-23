from ai.core.preferences import Preferences
from ai.example.action import Kill, RemoveDisguise


culture = Preferences()
culture.set_praiseworthiness(Kill, -1)
culture.set_goodness(Kill, -1)
culture.set_praiseworthiness(RemoveDisguise, 0)
culture.set_goodness(RemoveDisguise, 0)
