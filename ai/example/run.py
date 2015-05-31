from copy import deepcopy

from ai.example.preferences import culture
from ai.core.agent import Agent

frank = Agent(0, -.1, 0, 0, 0)
frank.name = "Frank"
frank.set_preferences(deepcopy(culture))

al = Agent(0, 1, 1, 0, -1)
al.name = "Al"
al.set_preferences(deepcopy(culture))

# Al likes Frank
al.get_preferences().set_love(frank, .25)

# Frank hates Al
frank.get_preferences().set_love(al, -1)

print "Al's initial mood: %s" % al.mood
print "Frank's initial mood: %s" % frank.mood
