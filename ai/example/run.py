from ai.example.preferences import culture
from ai.example.agent import ExampleAgent
from ai.example.action import apply_action, Kill, RemoveDisguise


balin = ExampleAgent.create_random_agent()
balin.name = "Balin"
balin.set_preferences(culture)

balan = ExampleAgent.create_random_agent()
balan.name = "Balan"
balan.set_preferences(culture)

# They like each other as brothers
# Create Balin's concepts of self and Balan
balin.beliefs.register_entity(balin.entity_id)
balin.beliefs.register_entity(balan.entity_id)
# Create Balan's concepts of self and Balin
balan.beliefs.register_entity(balan.entity_id)
balan.beliefs.register_entity(balin.entity_id)
# They both love themselves and each other
balin.get_preferences().set_love(balan.entity_id, 1)
balin.get_preferences().set_love(balin.entity_id, 1)
balan.get_preferences().set_love(balin.entity_id, 1)
balan.get_preferences().set_love(balan.entity_id, 1)

# They are both disguised
balan.disguised = True
balin.disguised = True

# They both dislike or are indifferent to the disguised versions of themselves
# Balin's concept of disguised self and disguised brother
balin.beliefs.register_entity(balan.entity_id)
balin.beliefs.register_entity(balin.entity_id)
# Balan's concept of disguised self and disguised brother
balan.beliefs.register_entity(balin.entity_id)
balan.beliefs.register_entity(balan.entity_id)
# They both are indifferent to their disguised brother,
# but love their disguised selves (?)
balin.get_preferences().set_love(balan.entity_id, -.1)
balin.get_preferences().set_love(balin.entity_id, 1)
balan.get_preferences().set_love(balin.entity_id, -.1)
balan.get_preferences().set_love(balan.entity_id, 1)

# They each know they just killed and were killed by the disguised characters
viewers = [balan, balin]
apply_action(action=RemoveDisguise, subject=balan, obj=balan, viewers=viewers)
apply_action(action=RemoveDisguise, subject=balin, obj=balin, viewers=viewers)
apply_action(action=Kill, subject=balan, obj=balin, viewers=viewers)
apply_action(action=Kill, subject=balin, obj=balan, viewers=viewers)

# They are sad about killing each other.
print "Balan emotions: %s" % balan.emotions
print "Balan mood: %s" % balan.mood
print "Balin emotions: %s" % balin.emotions
print "Balin mood: %s" % balin.mood

# TODO: Anger about an action should probably be weighted by how beneficial
# the outcome is and how liked the object of an action is to the observer
