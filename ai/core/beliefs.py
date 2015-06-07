class RELATIONSHIPS(object):
    """An enumeration of relationship types."""
    IS = 'is'


class Beliefs(object):
    known_entities = None
    beliefs = None

    def __init__(self):
        self.known_entities = []
        self.beliefs = []

    def register_entity(self, entity):
        if entity not in self.known_entities:
            self.known_entities.append(entity)

    def set_belief(self, belief):
        found_match = False
        if isinstance(belief, EntityAttrBelief):
            entity = belief.entity
            attr = belief.attr
            value = belief.value
            timestamp = belief.timestamp
            if entity not in self.known_entities:
                raise Exception("Unknown entity: %s" % entity)

            for b in self.beliefs:
                if isinstance(b, EntityAttrBelief):
                    if b.entity == entity and b.attr == attr:
                        found_match = True
                        b.value = value
                        b.timestamp = timestamp

        elif isinstance(belief, EntityEntityBelief):
            entity_1 = belief.entity_1
            entity_2 = belief.entity_2
            relationship = belief.relationship
            timestamp = belief.timestamp
            value = belief.value
            if entity_1 not in self.known_entities or \
                    entity_2 not in self.known_entities:
                raise Exception("Unknown entity (one of %s and %s)" % (
                    entity_1, entity_2)
                )

            for b in self.beliefs:
                if isinstance(b, EntityEntityBelief):
                    if b.entity_1 == entity_1 and b.entity_2 == entity_2 and \
                            b.relationship == relationship:
                        found_match = True
                        b.value = value
                        b.timestamp = timestamp

        if not found_match:
            self.beliefs.append(belief)

    def entities_count(self):
        return(len(self.known_entities))

    def beliefs_count(self):
        return(len(self.beliefs))

    def get_entity_attr(self, entity, attr, default=None):
        if entity not in self.known_entities:
            raise Exception("Unknown entity: %s" % entity)
        related_entities = self.get_related_entities(entity)
        greatest_timestamp = -1
        found_matching_belief = False
        value = None
        for b in self.beliefs:
            if isinstance(b, EntityAttrBelief):
                if b.entity in related_entities and b.attr == attr:
                    if b.timestamp > greatest_timestamp:
                        found_matching_belief = True
                        value = b.value
                        greatest_timestamp = b.timestamp
        if found_matching_belief:
            return value

        # Exhausted the search but no match found
        if default is None:
            raise BeliefNotFound
        else:
            return default

    def get_related_entities(self, entity, related=None):
        """Return all entities tied by 'is' relationship including the given entity."""
        if related is None:
            related = [entity]

        # Create the set of elements related to this one not yet searched for.
        neighbors = []
        for b in self.beliefs:
            if isinstance(b, EntityEntityBelief):
                if b.relationship == RELATIONSHIPS.IS and b.entity_1 == entity:
                    if b.entity_2 not in related and b.entity_2 not in neighbors:
                        # You have not yet searched through this neighbor's relateds
                        neighbors.append(b.entity_2)

        # You now know about all neighbors. Don't search for them again.
        related.extend(neighbors)

        # Get all neighbors of neighbors.
        for neighbor in neighbors:
            related = self.get_related_entities(neighbor, related=related)
        return related

    def set_entity_is_entity(self, timestamp, entity_1, entity_2, value):
        """Set the bi-directional is relationship."""
        belief_1 = EntityEntityBelief(timestamp, entity_1, entity_2, RELATIONSHIPS.IS, value)
        belief_2 = EntityEntityBelief(timestamp, entity_2, entity_1, RELATIONSHIPS.IS, value)
        self.set_belief(belief_1)
        self.set_belief(belief_2)


class BeliefNotFound(Exception):
    pass


class Belief(object):
    causing_belief = None


class EntityAttrBelief(Belief):
    """Belief that an entity has an attribute."""
    def __init__(self, timestamp, entity, attr, value):
        self.timestamp = timestamp
        self.entity = entity
        self.attr = attr
        self.value = value


class EntityEntityBelief(Belief):
    """Beliefs about two entities."""
    def __init__(self, timestamp, entity_1, entity_2, relationship, value):
        self.timestamp = timestamp
        self.entity_1 = entity_1
        self.entity_2 = entity_2
        self.relationship = relationship
        self.value = value


class Entity(object):
    """
    The concept of an object.

    Two entities may be, in fact, the same object.
    For example, a masquerading knight may be known to
    an agent as both the entities Masked Knight and Lancelot.
    """
    pass
