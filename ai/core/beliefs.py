class RELATIONSHIPS(object):
    """An enumeration of relationship types."""
    IS = 'is'


class Beliefs(object):
    known_entities = None
    beliefs = None

    def __init__(self):
        self.known_entities = []
        self.beliefs = []

    def register_entity(self, entity_id):
        assert(isinstance(entity_id, basestring))
        if entity_id not in self.known_entities:
            self.known_entities.append(entity_id)

    def set_belief(self, belief):
        found_match = False
        if isinstance(belief, EntityAttrBelief):
            entity_id = belief.entity_id
            attr = belief.attr
            value = belief.value
            timestamp = belief.timestamp
            if entity_id not in self.known_entities:
                raise Exception("Unknown entity: %s" % entity_id)

            for b in self.beliefs:
                if isinstance(b, EntityAttrBelief):
                    if b.entity_id == entity_id and b.attr == attr:
                        found_match = True
                        b.value = value
                        b.timestamp = timestamp

        elif isinstance(belief, EntityEntityBelief):
            entity_1_id = belief.entity_1_id
            entity_2_id = belief.entity_2_id
            relationship = belief.relationship
            timestamp = belief.timestamp
            value = belief.value
            if entity_1_id not in self.known_entities:
                raise Exception("Unknown entity %s" % entity_1_id)
            elif entity_2_id not in self.known_entities:
                raise Exception("Unknown entity %s" % entity_2_id)

            for b in self.beliefs:
                if isinstance(b, EntityEntityBelief):
                    if b.entity_1_id == entity_1_id and b.entity_2_id == entity_2_id and \
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

    def get_entity_attr(self, entity_id, attr, default=None):
        assert(isinstance(entity_id, basestring))
        if entity_id not in self.known_entities:
            raise Exception("Unknown entity: %s" % entity_id)
        related_entities = self.get_related_entities(entity_id)
        greatest_timestamp = -1
        found_matching_belief = False
        value = None
        for b in self.beliefs:
            if isinstance(b, EntityAttrBelief):
                if b.entity_id in related_entities and b.attr == attr:
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

    def get_related_entities(self, entity_id, related=None):
        """Return all entities tied by 'is' relationship including the given entity."""
        assert(isinstance(entity_id, basestring))
        if related is None:
            related = [entity_id]

        # Create the set of elements related to this one not yet searched for.
        neighbors = []
        for b in self.beliefs:
            if isinstance(b, EntityEntityBelief):
                if b.relationship == RELATIONSHIPS.IS and b.entity_1_id == entity_id:
                    if b.entity_2_id not in related and b.entity_2_id not in neighbors:
                        # You have not yet searched through this neighbor's relateds
                        neighbors.append(b.entity_2_id)

        # You now know about all neighbors. Don't search for them again.
        related.extend(neighbors)

        # Get all neighbors of neighbors.
        for neighbor in neighbors:
            related = self.get_related_entities(neighbor, related=related)
        return related

    def set_entity_is_entity(self, timestamp, entity_1_id, entity_2_id, value):
        """Set the bi-directional is relationship."""
        assert(isinstance(entity_1_id, basestring))
        assert(isinstance(entity_2_id, basestring))
        belief_1 = EntityEntityBelief(timestamp, entity_1_id, entity_2_id, RELATIONSHIPS.IS, value)
        belief_2 = EntityEntityBelief(timestamp, entity_2_id, entity_1_id, RELATIONSHIPS.IS, value)
        self.set_belief(belief_1)
        self.set_belief(belief_2)


class BeliefNotFound(Exception):
    pass


class Belief(object):
    causing_belief = None


class EntityAttrBelief(Belief):
    """Belief that an entity has an attribute."""
    def __init__(self, timestamp, entity_id, attr, value):
        assert(isinstance(entity_id, basestring))
        self.timestamp = timestamp
        self.entity_id = entity_id
        self.attr = attr
        self.value = value


class EntityEntityBelief(Belief):
    """Beliefs about two entities."""
    def __init__(self, timestamp, entity_1_id, entity_2_id, relationship, value):
        assert(isinstance(entity_1_id, basestring))
        assert(isinstance(entity_2_id, basestring))
        self.timestamp = timestamp
        self.entity_1_id = entity_1_id
        self.entity_2_id = entity_2_id
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
