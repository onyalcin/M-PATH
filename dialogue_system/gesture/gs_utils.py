import os
import json

gesture_dbs = {
    "smartbody": ['gesture_db.json', 'gesture_categories.json', 'emotion_categories', 'au_categories'],
    "unity": ['unity_gestures']
}  # TODO: add missing unity files to standardize things


def load_gesture_dbs(body_type):
    gesture_db = load_db(os.path.join('.', 'dialogue_system', 'gesture', 'data', body_type, 'gesture_db.json'))
    gesture_categories = load_db(os.path.join('.', 'dialogue_system', 'gesture', 'data', body_type,
                                              'gesture_categories.json'))
    emotion_categories = load_db(os.path.join('.', 'dialogue_system', 'gesture', 'data',  body_type,
                                              'emotion_categories.json'))
    au_categories = load_db(os.path.join('.', 'dialogue_system', 'gesture', 'data',  body_type,
                                         'au_categories.json'))

    return gesture_db, gesture_categories, emotion_categories, au_categories


def load_db(filename):
    with open(filename, 'r') as outfile:
        return json.load(outfile)
