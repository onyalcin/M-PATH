import json
import time
import math


class MockVideoRecognizer(object):
    def __init__(self):
        self.data = None

    def load_data(self, data_file):
        with open(data_file, 'r') as f:
            if data_file.endswith('.json'):
                self.data = json.load(f)

    def recognize(self, data=None):
        if data is not None:
            self.data = data
        fps = 60
        types = ["anger", "fear", "contempt", "surprise", "joy", "sadness", "disgust"]
        au_list = ["inner brow raise", "brow raise", "brow furrow", "eye widen", "cheek raise", "lid tighten",
                   "nose wrinkle", "upper lip raise", "dimpler", "lip corner depressor", "chin raise",
                   "lip pucker", "lip stretch", "lip press", "jaw drop", "lip suck", "eye closure", "smile"]
        print("START!!")
        last_time = time.time()
        time_past = 0
        for frame in self.data["frames"]:
            results = {k: frame["faces"]["0"][k] for k in types}
            au = {l: frame["faces"]["0"][l] for l in au_list}
            valence = frame["faces"]["0"]["valence"]
            engagement = frame["faces"]["0"]["engagement"]
            recognition = max(results, key=results.get)
            out = {"emotion": recognition, "value": results[recognition], "valence": valence, "au": au}

            time_past +=0.0167
            if time.time()-(last_time+time_past) < 0:
                time.sleep(0.02)
            '''
            new_time = time.time()
            sleep_time = ((1000.0 / fps) - (new_time - last_time)*1000.0) / 1000.0
            print(sleep_time)
            if sleep_time > 0:
                time.sleep(math.ceil(sleep_time*100)/100.0)
            #time.sleep(0.01)
            last_time = new_time
            '''
            yield out
