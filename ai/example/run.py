from copy import deepcopy

from ai.example.preferences import culture
from ai.example.agent import ExampleAgent


balin = ExampleAgent.create_random_agent()
balin.name = "Balin"
balin.set_preferences(deepcopy(culture))

balan = ExampleAgent.create_random_agent()
balan.name = "Balan"
balan.set_preferences(deepcopy(culture))

# They both think killing is shameful
balin.set_preferences(culture)
balan.set_preferences(culture)

# They like each other as brothers
# Create Balin's concepts of self and Balan
balin.beliefs.register_entity(balin.entity_id)
balin.beliefs.register_entity(balan.entity_id)
# Create Balan's concepts of self and Balin
balan.beliefs.register_entity(balan.entity_id)
balan.beliefs.register_entity(balin.entity_id)
# They both love themselves and each other
balin.preferences.set_love(balan, 1)
balin.preferences.set_love(balin, 1)
balan.preferences.set_love(balin, 1)
balan.preferences.set_love(balan, 1)

# They are both disguised
balan.disguised = True
balin.disguised = True

# They both dislike or are indifferent to the disguised versions of themselves
balin.beliefs.register_entity(balan.entity_id)
balan.beliefs.register_entity(balin.entity_id)

# They each know they just killed and were killed by the disguised characters


# They both find out that who the disguised people are

# They are sad about killing each other.
