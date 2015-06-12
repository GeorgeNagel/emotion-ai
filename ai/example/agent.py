from ai.core.agent import Agent


class ExampleAgent(Agent):
    disguised = False

    @property
    def entity_id(self):
        if not self.disguised:
            return self.uuid
        else:
            return "%s_disguised" % self.uuid
