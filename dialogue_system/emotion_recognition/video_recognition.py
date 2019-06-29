from statistics import mode

import cv2
import logging
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np

from .utils.face_classification.datasets import get_labels
from .utils.face_classification.inference import detect_faces
from .utils.face_classification.inference import draw_text
from .utils.face_classification.inference import draw_bounding_box
from .utils.face_classification.inference import apply_offsets
from .utils.face_classification.inference import load_detection_model
from .utils.face_classification.preprocessor import preprocess_input

from .recognizer import VideoRecognizer, VideoRecResult


logger = logging.getLogger().getChild(__name__)

# From face_classification: https://github.com/oarriaga/face_classification


class FaceVideoRecognizer(VideoRecognizer):
    def __init__(self):
        # parameters for loading data and images
        detection_model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                               'emotion_recognition\\utils\\face_classification\\trained_models\\detection_models\\' \
                               'haarcascade_frontalface_default.xml'
        emotion_model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                             'emotion_recognition\\utils\\face_classification\\trained_models\\' \
                             'emotion_models\\fer2013_mini_XCEPTION.102-0.66.hdf5'
        self.emotion_labels = get_labels('fer2013')  # 0: Angry, 1: Disgust, 2: Fear, 3: Happy,
        #  4: Sad, 5:Surprise, 6:Neutral

        # hyper-parameters for bounding boxes shape
        self.frame_window = 10
        self.emotion_offsets = (20, 40)

        # loading models
        self.face_detection = load_detection_model(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)

        # getting input model shapes for inference
        self.emotion_target_size = self.emotion_classifier.input_shape[1:3]

        # starting lists for calculating modes
        self.emotion_window = []

        # starting video streaming
        cv2.namedWindow('window_frame')
        self.video_capture = cv2.VideoCapture(0)

    def recognize(self, video_stream=None):
        if video_stream is not None:
            self.video_capture = video_stream
        while True:
            ret, frame = self.video_capture.read()
            if ret & self.video_capture.isOpened():
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faces = detect_faces(self.face_detection, gray_image)

                for face_coordinates in faces:

                    x1, x2, y1, y2 = apply_offsets(face_coordinates, self.emotion_offsets)
                    gray_face = gray_image[y1:y2, x1:x2]
                    try:
                        gray_face = cv2.resize(gray_face, self.emotion_target_size)
                    except Exception:
                        continue

                    gray_face = preprocess_input(gray_face, True)
                    gray_face = np.expand_dims(gray_face, 0)
                    gray_face = np.expand_dims(gray_face, -1)
                    emotion_prediction = self.emotion_classifier.predict(gray_face)
                    emotion_probability = np.max(emotion_prediction)
                    emotion_label_arg = np.argmax(emotion_prediction)
                    emotion_text = self.emotion_labels[emotion_label_arg]
                    self.emotion_window.append(emotion_text)

                    if len(self.emotion_window) > self.frame_window:
                        self.emotion_window.pop(0)
                    try:
                        emotion_mode = mode(self.emotion_window)
                    except Exception:
                        continue

                    if emotion_text == 'angry':
                        color = emotion_probability * np.asarray((255, 0, 0))
                    elif emotion_text == 'sad':
                        color = emotion_probability * np.asarray((0, 0, 255))
                    elif emotion_text == 'happy':
                        color = emotion_probability * np.asarray((255, 255, 0))
                    elif emotion_text == 'surprise':
                        color = emotion_probability * np.asarray((0, 255, 255))
                    else:
                        color = emotion_probability * np.asarray((0, 255, 0))

                    color = color.astype(int)
                    color = color.tolist()

                    draw_bounding_box(face_coordinates, rgb_image, color)
                    draw_text(face_coordinates, rgb_image, emotion_mode,
                              color, 0, -45, 1, 1)

                bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                cv2.imshow('window_frame', bgr_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                '''
                types = ["anger", "fear", "neutral", "surprise", "joy", "sadness", "disgust"]
                au_list = ["inner brow raise", "brow raise", "brow furrow", "eye widen", "cheek raise", "lid tighten",
                           "nose wrinkle", "upper lip raise", "dimpler", "lip corner depressor", "chin raise",
                           "lip pucker", "lip stretch", "lip press", "jaw drop", "lip suck", "eye closure", "smile"]
                print("START!!")
                for frame in self.data["frames"]:
                    results = {k: frame["faces"]["0"][k] for k in types}
                    au = {l: frame["faces"]["0"][l] for l in au_list}
                    valence = frame["faces"]["0"]["valence"]
                    engagement = frame["faces"]["0"]["engagement"]
                    recognition = max(results, key=results.get)
                    out = {"emotion": recognition, "value": results[recognition], "valence": valence, "au": au}

                    yield VideoRecResult(**out)
                '''

# from https://github.com/omar178/Emotion-recognition

class EmotionVideoRecognizer(VideoRecognizer):
    def __init__(self):
        # parameters for loading data and images
        detection_model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                               'emotion_recognition\\utils\\face_classification\\trained_models\\detection_models\\' \
                               'haarcascade_frontalface_default.xml'
        emotion_model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                             'emotion_recognition\\utils\\face_classification\\trained_models\\' \
                             'emotion_models\\fer2013_mini_XCEPTION.102-0.66.hdf5'
        # loading models
        self.face_detection = load_detection_model(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)

        # starting video streaming
        self.video_capture = cv2.VideoCapture(0)

        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

    def recognize(self, video_stream=None):
        if video_stream is not None:
            self.video_capture = video_stream
        while True:
            ret, frame = self.video_capture.read()
            if ret & self.video_capture.isOpened():
                # reading the frame
                frame = cv2.resize(frame, (300, 200))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                             flags=cv2.CASCADE_SCALE_IMAGE)

                canvas = np.zeros((250, 300, 3), dtype="uint8")
                clone = frame.copy()
                if len(faces) > 0:
                    faces = sorted(faces, reverse=True,
                                   key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
                    (fX, fY, fW, fH) = faces
                    # Extract the ROI of the face from the grayscale image,
                    # resize it to a fixed 28x28 pixels, and then prepare
                    # the ROI for classification via the CNN
                    roi = gray[fY:fY + fH, fX:fX + fW]
                    roi = cv2.resize(roi, (64, 64))
                    roi = roi.astype("float") / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    predictions = self.emotion_classifier.predict(roi)[0]
                    emotion_probability = np.max(predictions)
                    label = self.EMOTIONS[predictions.argmax()]
                else:
                    continue

                for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS, predictions)):
                    # construct the label text
                    text = "{}: {:.2f}%".format(emotion, prob * 100)

                    w = int(prob * 300)
                    cv2.rectangle(canvas, (7, (i * 35) + 5),
                                  (w, (i * 35) + 35), (0, 0, 255), -1)
                    cv2.putText(canvas, text, (10, (i * 35) + 23),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (255, 255, 255), 2)
                    cv2.putText(clone, label, (fX, fY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    cv2.rectangle(clone, (fX, fY), (fX + fW, fY + fH),
                                  (0, 0, 255), 2)

                cv2.imshow('your_face', clone)
                cv2.imshow("Probabilities", canvas)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


# my version

class Emo_VideoRecognizer(VideoRecognizer):
    def __init__(self):
        # parameters for loading data and images
        detection_model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                               'emotion_recognition\\utils\\face_classification\\trained_models\\detection_models\\' \
                               'haarcascade_frontalface_default.xml'
        emotion_model_path = 'C:\\Users\\steve\\Documents\\MyChatterBot\\BOT\\dialogue_system\\dialogue_system\\' \
                             'emotion_recognition\\utils\\face_classification\\trained_models\\' \
                             'emotion_models\\fer2013_mini_XCEPTION.102-0.66.hdf5'
        # loading models
        self.face_detection = load_detection_model(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        self.emotion_classifier._make_predict_function()

        # Empty run of classifier to fully initialize it
        self.emotion_classifier.predict(np.empty(shape=(1, 64, 64, 1)))

        # no contempt bu extra neutral
        self.EMOTIONS = ["anger", "disgust", "fear", "joy", "sad", "surprise", "neutral"]
        self._show_output = False

    def recognize(self, frame):
        frame = cv2.resize(frame, (300, 200))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detection.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) == 0:
            return {}

        faces = sorted(faces, reverse=True,
                       key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        # Extract ROI from the grayscale image,
        # resize, and then prepare it for classification via the CNN
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        predictions = self.emotion_classifier.predict(roi)[0]
        #emotion_probability = np.max(predictions)

        # dict containing emotions and probabilities in 0.0f
        emotions = dict(zip(self.EMOTIONS, predictions))
        # returning emotions as a separate dict
        '''
        if self._show_output:
            label = self.EMOTIONS[predictions.argmax()]
            canvas = np.zeros((250, 300, 3), dtype="uint8")
            clone = frame.copy()

            for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS, predictions)):
                # construct the label text
                text = "{}: {:.2f}%".format(emotion, prob * 100)

                w = int(prob * 300)
                cv2.rectangle(canvas, (7, (i * 35) + 5),
                              (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(canvas, text, (10, (i * 35) + 23),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 2)
                cv2.putText(clone, label, (fX, fY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(clone, (fX, fY), (fX + fW, fY + fH),
                              (0, 0, 255), 2)

            cv2.imshow('your_face', clone)
            cv2.imshow("Probabilities", canvas)
        '''
        return {"emotions": emotions}
