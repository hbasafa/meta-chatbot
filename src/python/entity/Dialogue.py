
from src.python.entity.Utterance import Utterance
from src.python.param import dataset
import pandas as pd
import numpy as np


class Dialogue(object):
    dialogue_id = 0

    def __init__(self, is_multidomain=False, utterances=None):
        self.dialogue_id = self.next_id()
        self.is_multidomain = is_multidomain
        if utterances:
            self.utterances = utterances
        else:
            self.utterances = list()
        Utterance.reset()

    def next_id(self):
        Dialogue.dialogue_id +=1
        return Dialogue.dialogue_id

    def set_is_multidomain(self, value):
        self.is_multidomain = value

    def set_utterances(self, utterances):
        self.utterances = utterances

    def add_utterance(self, utterance):
        self.utterances.append(utterance)

    def add_utterances(self, utterances):
        self.utterances.extend(utterances)

    def get_is_multidomain(self):
        return self.is_multidomain

    def get_utterances(self):
        return self.utterances

    def get_id(self):
        return self.dialogue_id

    def get_dataframe_headers(self):
        headers = [dataset.DIALOGUE_ID, dataset.UTTERANCE_ID, dataset.SPEAKER_ID, dataset.TIMESTAMP,
                    dataset.UTTERANCE_DOMAIN, dataset.UTTERANCE_SUBDOMAIN, dataset.TEXT, dataset.ACT]
        return headers

    def to_dataframe(self):
        headers = self.get_dataframe_headers()
        dialog_id = self.get_id()
        rows = []
        for utter in self.get_utterances():
            utter_id = utter.get_id()
            text = utter.get_text()
            speaker_id = utter.get_speaker_id()
            domain = utter.get_domain()
            subdomain = utter.get_subdomain()
            timestamp = utter.get_timestamp()
            act = str(utter.get_acts()[0])
            row = [dialog_id, utter_id, speaker_id, timestamp, domain, subdomain, text, act]
            rows.append(row)
        df = {}
        rows = np.array(rows).T
        for h, r in zip(headers, rows):
            df.update({h: r})
        df = pd.DataFrame(df)
        return df
