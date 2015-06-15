from copy import deepcopy

from ai.example.preferences import culture
from ai.example.agent import ExampleAgent


balin = ExampleAgent.create_random_agent()
balin.name = "Balin"
balin.set_preferences(deepcopy(culture))

balan = ExampleAgent.create_random_agent()
balan.name = "Balan"
balan.set_preferences(deepcopy(culture))

# They know that they are brothers

# They like each other, because they know they are brothers
# and brothers generally like each other

# They are both disguised

# They both dislike or are indifferent to the disguised versions of themselves

# They each know they just killed and were killed by the disguised characters

# They both find out that who the disguised people are

# They are sad about killing each other.
