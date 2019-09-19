import pandas as pd
import queue


class Emotion_Fusion:
    def __init__(self, video_recognition, speech_recognition):
        self.video_recongition = video_recognition
        self.speech_recognition = speech_recognition

        self.video_thread = None
        self.speech_thread = None

        self.user_emotion = queue.Queue()
        self.user_mood = queue.Queue()
        self.user_personality = queue.Queue()

    def valence_analysis(self):
        for result in self.video_recongition.recognize():
            self.user_emotion.put(result["valence"])
            if len(self.user_emotion) > 3:
                #self.user_emotion(self.user_personality
                pass