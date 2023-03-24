
from _datetime import datetime


class Utterance(object):

    utterance_id = 0

    def __init__(self, text, acts=list(), speaker_id=0, timestamp=datetime.now(), domain=None, subdomain=None):
        self.utterance_id = self.next_id()
        self.text = text
        self.speaker_id = speaker_id
        self.timestamp = timestamp
        self.acts = acts
        self.domain = domain
        self.subdomain = subdomain

    def next_id(self):
        Utterance.utterance_id += 1
        return Utterance.utterance_id

    def set_text(self, text):
        self.text = text

    def set_acts(self, acts):
        self.acts = acts

    def set_speaker_id(self, speaker_id):
        self.speaker_id = speaker_id

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def set_domain(self, domain):
        self.domain = domain

    def set_subdomain(self, sd):
        self.subdomain = sd

    def get_id(self):
        return self.utterance_id

    def get_text(self):
        return self.text

    def get_acts(self):
        return self.acts

    def get_speaker_id(self):
        return self.speaker_id

    def get_timestamp(self):
        return self.timestamp

    def get_domain(self):
        return self.domain

    def get_subdomain(self):
        return self.subdomain

    @staticmethod
    def reset():
        Utterance.utterance_id = 0
