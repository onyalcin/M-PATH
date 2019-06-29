import os
import json
import text_normalization as t
from .db_utils import save_dbs
import argparse
from shutil import copyfile

# For [context, intent, next_intent, [q1;q2;q3], [r1;r2;r3], gesture, emotion, bml]


def ensure_dir(chatbot_name):
    directory = os.path.join('..', '..', 'data', chatbot_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
        return directory
    else:
        raise Exception('Directory with the bot name already exists!')


def create_db(source_path, chatbot_name):
    if chatbot_name is None:
        chatbot_name = input('Give your bot a name:')
    try:
        dir = ensure_dir(chatbot_name)
    except:
        print('There is already a bot with the same name, try another name.')
        chatbot_name = input('Give your bot another name >')
        dir = ensure_dir(chatbot_name)

    if source_path is None:
        source_path = input('Need a filename to load the database:')
    copyfile(source_path, os.path.join(dir, 'corpus.txt'))

    db_search = {}
    db_learn = {}
    op = open(source_path, 'r')

    for line in op:
        lst = json.loads(line)
        int1 = t.clean_whitespace(lst[1])
        context = t.clean_whitespace(lst[0])
        Qs = lst[3][1:-1].split(';')
        As = lst[4][1:-1].split(';')
        if lst[2] == "":
            Cs = []
        else:
            Cs = [t.clean_whitespace(lst[2])]  # WARNING considering this is not a list

        # add intent to db_learn
        responses = []
        for x in As:
            responses.append(x)

        if int1 not in db_learn:
            db_learn[int1]= {"patterns": Qs, "responses": responses, "context_set": Cs, "context": context}
        else:
            n_patterns = list(set(db_learn[int1]['patterns']) | set(Qs))
            n_responses = list(set(db_learn[int1]['responses']) | set(responses))
            n_context_set = list(set(db_learn[int1]['context_set']) | set(Cs))
            db_learn[int1] = {"patterns": n_patterns, "responses": n_responses, "context_set": n_context_set, "context": context} # assuming there can be only one context for an intent

        #construct db_search
        for Q in Qs:
            q = t.clean(Q)
            if q not in db_search:
                db_search[q] = {"intents": [t.clean_whitespace(int1)],"context_set": Cs}
            else:
                n_intents = list(set(db_search[q]['intents']) | set([int1]))
                n_context_set = list(set(db_search[q]['context_set']) | set(Cs))
                db_search[q] = {"intents": n_intents, "context_set": n_context_set}

    # add global fallback
    db_learn["fallback_global"] = {"context_set": [""], "responses": ["I am sorry, I don't know much about that"], "patterns": []}
    # save the files
    save_dbs(chatbot_name, db_search, db_learn)
    op.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source_path", help="sourcepath for the txt file/n ex. bot.txt", type=str, default=None)
    parser.add_argument("-b", "--bot_name", help= "give the bot a name", type=str, default=None)
    args = parser.parse_args()
    create_db(args.source_path, args.bot_name)
    print("Done!")
