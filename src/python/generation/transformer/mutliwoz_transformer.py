import ast

import pandas as pd
import numpy as np
import json
from src.python.param import order, multiwoz as mp, dataset as d, product_feature as pf
from src.python.utils.common import get_key
from src.python.database import manager


dataset_path = "/home/albert/Projects/PycharmProjects/DialogueSystemE2Ebaseline/src/python/" \
               "data/rulebased/generated_dataset.xlsx"
factor_path = "/home/albert/Projects/PycharmProjects/DialogueSystemE2Ebaseline/src/python/data/rulebased/factors.xlsx"
out_path = "/home/albert/Projects/PycharmProjects/DialogueSystemE2Ebaseline/src/python/data/multiwoz/"


def get_file_name(oid):
    fname =  prefix + str(oid) + format_string
    return fname


def generate_names(df):
    names = df[order.ORDER_ID].apply(get_file_name)
    return names


def create_file_list(names):
    with open(out_path + "valListFile" + format_string, 'w') as f:
        f.writelines("\n".join(names))


def get_goal_content(dialogue_id, factor_id):
    goal_content = {}
    return goal_content


def get_dialogue(dialogue_id):
    dialogue = dataset[dataset[d.DIALOGUE_ID]==dialogue_id]
    return dialogue


def get_text(row):
    text = row[d.TEXT]
    return text


def get_domains():
    domains = set(dataset[d.UTTERANCE_DOMAIN])
    return domains


def get_subdomains(domain):
    domain_rows = dataset[dataset[d.UTTERANCE_DOMAIN] == domain]
    subdomains = set(domain_rows[d.UTTERANCE_SUBDOMAIN])
    return subdomains


def get_speaker_id(row):
    speaker_id = row[d.SPEAKER_ID]
    return speaker_id


def get_all_slots(category):
    categories = product_features[product_features[pf.CATEGORY] == category]
    slots = categories[pf.FEATURE]
    return set(slots)


def get_book_content(row, category):
    book_content = {}



def get_category(row):
    cat = row[d.UTTERANCE_SUBDOMAIN]
    return cat


def get_semi_content(row, category):
    semi_content = {}
    acts = get_acts(row)
    product_category = get_category(row)
    all_slots = get_all_slots(category)
    for intent, slots_dict in acts.items():
        #TODO: where is intent?!
        for slot in all_slots:
            if category == product_category:
                try:
                    slot_value = slots_dict[slot]
                    semi_content.update({slot: slot_value})
                except KeyError:
                    semi_content.update({slot: default_semi_notmentioned_slot})
            else:
                semi_content.update({slot: default_semi_slot})
    return semi_content


def get_category_content(row, category):
    category_content = {mp.BOOK: get_book_content(row, category),
                        mp.SEMI: get_semi_content(row, category)}
    return category_content


def get_subdomain_content(row, subdomain):
    # in case of any other subdomain instead of category
    category = subdomain
    subdomain_content = get_category_content(row, category)
    return subdomain_content


def get_domain_content(row, domain):
    domain_content = {}
    subdomains = get_subdomains(domain)
    for subdom in subdomains:
        domain_content.update({subdom: get_subdomain_content(row, subdom)})
    return domain_content


def merge_metas(old_meta, new_meta):
    meta = new_meta
    for domain_name, domain_content in new_meta.items():
        for cat_name, cat_content in domain_content.items():
            for info_name, info_content in cat_content.items():
                if info_name == mp.BOOK:
                    pass
                if info_name == mp.SEMI:
                    for filter_name, filter_value in info_content.items():
                        if filter_value == default_semi_notmentioned_slot or len(filter_value) == 0:
                            meta[domain_name][cat_name][info_name][filter_name] = old_meta[domain_name][cat_name][info_name][filter_name]

    return meta


def get_meta(row):
    meta = {}
    domains = get_domains()
    for dom in domains:
        meta.update({dom: get_domain_content(row, dom)})
    return meta


def get_utterances(dialogue):
    pass


def get_log_content(dialogue_id, factor_id):
    dialogue = get_dialogue(dialogue_id)
    log_content = []
    is_second_row = True
    old_meta = old_row = None
    for i, row in dialogue.iterrows():
        text = get_text(row)
        speaker_id = get_speaker_id(row)
        if speaker_id == 0:
            meta = get_meta(old_row)
            if is_second_row:
                old_meta = meta
                is_second_row = False
            meta = merge_metas(old_meta, meta)
            old_meta = meta
        else:
            meta = {}
        old_row = row
        log_content.append({mp.TEXT: text, mp.METADATA: meta})
    return log_content


def prepare_content(dialogue_id, factor_id):
    content = {
        mp.GOAL: get_goal_content(dialogue_id, factor_id),
        mp.LOG: get_log_content(dialogue_id, factor_id),
    }
    return content


def get_information():
    info = {}
    for _, (dialogue_id, factor_id) in factors.iterrows():
        content = prepare_content(dialogue_id, factor_id)
        filename = get_file_name(factor_id)
        info.update({filename:content})
    return info


def get_act_id(row):
    utter_id = row[d.UTTERANCE_ID]
    act_id = str(int(np.ceil(utter_id / 2)))
    return act_id


def get_domain(row):
    domain = row[d.UTTERANCE_DOMAIN]
    return domain


def get_subdomain(row):
    subdom = row[d.UTTERANCE_SUBDOMAIN]
    return subdom


def get_intent(act):
    intent = get_key(act)
    return intent


def get_act_prefix(row):
    domain = get_domain(row)
    subdomain = get_subdomain(row)
    key = "-".join([domain, subdomain])
    return key


def get_slots(slots_dict):
    slots = []
    if len(slots_dict) == 0:
        slots.append([default_slot, default_slot])
    else:
        for slot_name, slot_value in slots_dict.items():
            slots.append([slot_name, slot_value])
    return slots


def get_acts(row):
    acts = ast.literal_eval(row[d.ACT])
    return acts


def get_dialogue_acts(row):
    dialogue_acts = []
    acts = get_acts(row)
    prefix = get_act_prefix(row)
    for intent, slots_dict in acts.items():
        act_key = "-".join([prefix, intent])
        slots_list = get_slots(slots_dict)
        dialogue_acts.append({act_key: slots_list})
    return dialogue_acts


def prepare_acts(dialogue_id, factor_id):
    dialogue_rows = get_dialogue(dialogue_id)
    acts = {}
    act_id = 0
    for i , row in dialogue_rows.iterrows():
        speaker_id = get_speaker_id(row)
        if speaker_id != 0:
            act_id = get_act_id(row)
        dialogue_acts = get_dialogue_acts(row)
        for act in dialogue_acts:
            acts.update({act_id: act})
    return acts


def get_labels():
    labels = {}
    for _, (dialogue_id, factor_id) in factors.iterrows():
        acts = prepare_acts(dialogue_id, factor_id)
        filename = get_file_name(factor_id)
        labels.update({filename:acts})
    return labels


def create_data_file(dt, name):
        f = open(out_path + name + format_string, 'w')
        json.dump(dt, f)


def get_database():
    pass


if __name__ == '__main__':
    dataset = pd.read_excel(dataset_path)
    factors = pd.read_excel(factor_path)
    product_features = manager.get_products_features()
    prefix = "factor-"
    format_string = ".json"
    default_slot = "none"
    default_semi_slot = ""
    default_semi_notmentioned_slot = "not mentioned"

    # file list
    conversation_names = generate_names(factors)
    create_file_list(conversation_names)

    # data file
    data = get_information()
    create_data_file(data, "data")

    # act file
    act_data = get_labels()
    create_data_file(act_data, "dialogue_acts")

    # db file
    db_data = get_database()
    create_data_file(db_data, "shop_db")
