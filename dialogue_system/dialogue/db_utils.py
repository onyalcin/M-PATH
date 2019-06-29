import os
import json

from dialogue_system.dialogue import text_normalization as t


# LOAD BOTS
def load_dbs_old(path):
    learn_db = load_learn_db(os.path.join(path, 'learn.json'))
    search_db = load_search_db(os.path.join(path, 'search.json'))
    return search_db, learn_db


def load_dbs(path):
    learn_db = load_learn_db(os.path.join(path, 'learn.json'))
    search_db = load_search_from_learn(learn_db)
    return search_db, learn_db


def load_search_from_learn(learn_db):
    search_db = {}
    for item in learn_db.keys():
        for q in learn_db[item]["patterns"]:
            qc = t.clean_db(q)
            if qc not in search_db.keys():
                search_db[qc] = {"intents": [item], "context_set": learn_db[item]["context_set"]}
            else:
                n_intents = list(set(search_db[qc]['intents']) | set([item]))
                n_context_set = list(set(search_db[qc]['context_set']) | set(learn_db[item]["context_set"]))
                search_db[qc] = {"intents": n_intents, "context_set": n_context_set}
    return search_db


def load_learn_db(filename):
    with open(filename, 'r') as outfile:
        learn_db = json.load(outfile)
    return learn_db


def load_search_db(filename):
    with open(filename, 'r') as outfile:
        search_db = json.load(outfile)
    return search_db


# SAVE BOTS

def save_dbs(path, search_db, learn_db):
    save_search_db(os.path.join(path, 'search.json'), search_db)
    save_learn_db(os.path.join(path, 'learn.json'), learn_db)


def save_learn_db(filename, learn_db):
    with open(filename, 'w') as outfile:
        json.dump(learn_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def save_search_db(filename, search_db):
    with open(filename, 'w') as outfile:
        json.dump(search_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))
