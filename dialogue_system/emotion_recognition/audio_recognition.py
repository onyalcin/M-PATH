import os
from keras.models import load_model, model_from_json
import numpy
import cv2
import json

import librosa
from scipy import signal

from .recognizer import AudioRecognizer


# TODO: Testing the functionality
class RavdessAudioRecognizer(AudioRecognizer):
    def __init__(self):
        self.audioSeconds = 3
        self.numberOfAugmentedSamples = 10
        self.framesPerSecond = 30
        self.stride = 25

        self.sr = 16000

        self.categories = ["calm", "angry", "sad", "disgust", "happy", "fearful"]

        model_path = 'dialogue_system\\emotion_recognition\\utils\\audio\\models\\'

        model_location = "fckin_RAVDESS_Audio.h5"
        arch_location = "fckin_arch_RAVDESS.json"
        with open(os.path.join(model_path, arch_location), 'r') as arch_file:
            arch = json.load(arch_file)
        weights_location = "weights_RAVDESS.h5"
        self.model = model_from_json(arch)
        self.model.load_weights(os.path.join(model_path, weights_location))
        #self.model = load_model(os.path.join(model_path, model_location))

    def slice_signal2(self, signal, sliceSize, stride=0.5):
        slice_size = 16000 * sliceSize
        slices = []
        currentFrame = 0
        while currentFrame + slice_size < len(signal):
            currentSlide = signal[currentFrame:int(currentFrame + slice_size)]
            slices.append(currentSlide)
            currentFrame = int(currentFrame + slice_size * stride)
        return numpy.array(slices)

    def preprocess2(self, signals, augment=False):
        signals2 = []
        for wav_data2 in signals:
            mel = librosa.feature.melspectrogram(y=wav_data2, sr=self.sr, n_mels=80)
            mel = numpy.array(cv2.resize(mel, (80, 96)))
            mel = numpy.expand_dims(mel, axis=0)
            signals2.append(mel)
        return numpy.array(signals2)

    def recognize(self, chunk):
        audio_batch = self.preprocess2(chunk) # FIXME! Are we passing audio chunk which is already sliced or slice it
        predictions = []
        for audio in audio_batch:  # TODO: I think it is better to get already sliced data and average over it
            predictions.append(self.model.predict(numpy.array([audio]), batch_size=64, verbose=0))
        return predictions

    def recognize_file(self, dataLocation):
        wav_data, sr = librosa.load(dataLocation, mono=True, sr=self.sr)
        signals = self.slice_signal2(wav_data, 3, 1)  # FIXME! This is weird and not being used
        #signals = [wav_data[0:49152]]
        audio_batch = self.preprocess2(signals)
        predictions = []
        for audio in audio_batch:
            prediction = self.model.predict(numpy.array([audio]), batch_size=64, verbose=0)
            predictions.append([self.categories[numpy.where(prediction == numpy.max(prediction))[0][0]],
                                numpy.max(prediction)])
        print(predictions)
        return predictions


class AudioAVRecognizer(AudioRecognizer):
    def __init__(self):
        self.audioSeconds = 0.3
        self.sr = 16000

        model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                     'emotion_recognition\\utils\\audio\\models\\'

        weights_location = "fckin_weights.h5"
        arch_location = "fckin_arch.json"
        model_location = "fckin_heck_yea.h5"

        with open(os.path.join(model_path, arch_location), 'r') as arch_file:
            arch = json.load(arch_file)

        self.model = model_from_json(arch)
        self.model.load_weights(os.path.join(model_path, weights_location))
        #self.model = load_model(os.path.join(model_path, model_location))

    def slice_signal(self, signal, seconds=1.0, sr=16000):
        """ Return windows of the given signal by sweeping in stride fractions
            of window
        """
        slices = []
        stepSize = int((seconds * sr))
        totalSteps = int(len(signal) / stepSize)
        for i in range(totalSteps):
            slice = signal[int(i * stepSize):int(i * stepSize) + stepSize]
            slices.append(slice)
        return numpy.array(slices)

    def preEmphasis(self, signal, coeff=0.95):
        x = numpy.array(signal)
        x0 = numpy.reshape(x[0], [1, ])
        diff = x[1:] - coeff * x[:-1]
        concat = numpy.concatenate([x0, diff], 0)
        return concat

    def preprocess(self, signals, augment=False):
        signals2 = []
        for wav_data2 in signals:
            mel = librosa.feature.melspectrogram(y=wav_data2, sr=self.sr, n_mels=96)
            if self.audioSeconds == 3:
                mel = numpy.array(cv2.resize(mel, (96, 96)))
            elif self.audioSeconds == 1:
                mel = numpy.array(cv2.resize(mel, (32, 96)))
            elif self.audioSeconds == 0.3:
                mel = numpy.array(cv2.resize(mel, (10, 96)))
            mel = numpy.expand_dims(mel, axis=0)
            signals2.append(mel)
        return numpy.array(signals2)

    def recognize(self, wav_data):
        signals = self.slice_signal(wav_data, seconds=self.audioSeconds, sr=self.sr)
        processed_audio = self.preprocess(signals)
        meanArousal = []
        meanValence = []
        for audio in processed_audio:
            prediction = self.model.predict(numpy.array([audio]), batch_size=64, verbose=0)
            print("Prediciton:", prediction[0])
            print("Prediciton:", prediction[1])
            meanArousal.append(float(prediction[0][0]))
            meanValence.append(float(prediction[1][0]))
        return {"arousal": numpy.mean(meanArousal), "valence": numpy.mean(meanValence)}

    def recognize_file(self, dataLocation):
        fftsize = 1024
        hop_length = 512
        wav_data, sr = librosa.load(dataLocation, mono=True,
                                    sr=self.sr)
        signals = self.slice_signal(wav_data, seconds=self.audioSeconds, sr=self.sr)
        processed_audio = self.preprocess(signals)
        meanArousal = []
        meanValence = []
        for audio in processed_audio:
            prediction = self.model.predict(numpy.array([audio]), batch_size=64, verbose=0)
            print("Prediciton:", prediction[0])
            print("Prediciton:", prediction[1])
            meanArousal.append(float(prediction[0][0]))
            meanValence.append(float(prediction[1][0]))
        return {"arousal": numpy.mean(meanArousal), "valence": numpy.mean(meanValence)}