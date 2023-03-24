import pandas as pd
import json

from src.python.Features import *

path = "/home/albert/Documents/DS1/"
file_name = "restaurant.tsv"


def standard_data(file_path, new_file_path):
    with open(file_path, 'r', newline="") as fo, open(new_file_path, 'w') as fi:
        is_header = True
        for line in iter(lambda: fo.readline(), ''):
            cols = line.split("\t")
            last_col = cols[DIALOGUE_ACTS_NUM:]

            if is_header:
                header = '\t'.join(cols[:DIALOGUE_ACTS_NUM + 1]) + '\n'
                fi.write(header)
                is_header = False
                continue

            act_dict = dict()
            for act in last_col:
                if act == '' or act == '\n':
                    continue
                i = act.find('(')
                j = act.rfind(')')
                action = act[:i]
                slot_string = act[i + 1:j]
                slots = slot_string.split(';')
                slot_values = []
                if i + 1 == j:  # no slot
                    act_dict.update({action: {}})

                for s in slots:
                    vs = s.split('=')
                    if len(vs) == 1:
                        slot_values.append((vs[0], vs[0]))
                    else:
                        slot_values.append((vs[0], vs[1]))

                for s, sv in slot_values:
                    act_dict.update({action: {s: sv}})

            rest = cols[:DIALOGUE_ACTS_NUM]
            new_row = '\t'.join(c for c in rest) + '\t' + json.dumps(act_dict) + '\n'
            fi.write(new_row)


if __name__ == '__main__':
    file_path = path + file_name
    new_file_path = path + "sample.tsv"

    # standard_data --> Done.

    # reading data
    data = pd.read_csv(new_file_path, sep='\t')

    # preparing data for nlu comp
    utterances = data[MESSAGE_TEXT]
    labels_text = data[DIALOGUE_ACTS]

    #TODO: token-number for words
    #TODO(opt): embedding for words
    #TODO: IOB-tagging + intent = labels


    # preparing data for dm comp

    # preparing data for nlg comp

    # train end-to-end




