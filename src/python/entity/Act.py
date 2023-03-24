

# TODO: is it better than usual dictionary?!


class Act(object):

    def __init__(self, intent=None, slots=None):
        self.intent = intent
        if slots:
            self.slots = slots
        else:
            self.slots = dict()

    def set_act(self, act):
        self.intent = act.get_intent()
        self.slots = act.get_slots()

    def set_act_as_dict(self, act):
        key = list(act.keys())[0]
        self.intent = key
        self.slots = act[key]

    def set_intents(self, intents):
        self.intent = intents

    def set_slots(self, slots):
        self.slots = slots

    def get_intent(self):
        return self.intent

    def get_slots(self):
        return self.slots

    def to_dict(self):
        return {self.get_intent(): self.get_slots()}

    def items(self):
        return self.to_dict().items()

    def __str__(self):
        return self.to_dict().__str__()

    def to_string(self):
        return self.__str__()
