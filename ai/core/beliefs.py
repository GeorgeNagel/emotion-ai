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
            if entity not in self.known_entities:
                raise Exception("Unknown entity: %s" % entity)

            for b in self.beliefs:
                if isinstance(b, EntityAttrBelief):
                    if b.entity == entity and b.attr == attr:
                        found_match = True
                        b.value = value

        elif isinstance(belief, EntityEntityBelief):
            entity_1 = belief.entity_1
            entity_2 = belief.entity_2
            relationship = belief.relationship
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

        if not found_match:
            self.beliefs.append(belief)

    def entities_count(self):
        return(len(self.known_entities))

    def beliefs_count(self):
        return(len(self.beliefs))

    def get_entity_attr(self, entity, attr, default=None):
        if entity not in self.known_entities:
            raise Exception("Unknown entity: %s" % entity)
        for b in self.beliefs:
            if isinstance(b, EntityAttrBelief):
                if b.entity == entity and b.attr == attr:
                    return b.value

        # Exhausted the search but no match found
        if default is None:
            raise BeliefNotFound
        else:
            return default


class BeliefNotFound(Exception):
    pass


class Belief(object):
    causing_belief = None


class EntityAttrBelief(Belief):
    """Belief that an entity has an attribute."""
    def __init__(self, entity, attr, value):
        self.entity = entity
        self.attr = attr
        self.value = value


class EntityEntityBelief(Belief):
    """Beliefs about two entities."""
    def __init__(self, entity_1, entity_2, relationship, value):
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
