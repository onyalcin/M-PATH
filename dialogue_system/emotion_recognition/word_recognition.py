import csv
import logging

logger = logging.getLogger().getChild(__name__)


class NRC_AffectIntensity:
    def __init__(self):
        self.lexicon = {}
        with open('dialogue_system/emotion_recognition/utils/language/nrc/NRC-AffectIntensity-Lexicon.txt') as file:
            reader = csv.DictReader(file, delimiter='\t')
            header = reader.fieldnames
            for row in reader:
                self.add_lexicon(row)
            logger.debug('Done reading affect lexicon!')

    def add_lexicon(self, affect_dict):
        if affect_dict['term'] not in self.lexicon:
            self.lexicon[affect_dict['term']] = {'value': float(affect_dict['score']),
                                                 'emotion': affect_dict['AffectDimension']}
        elif self.lexicon[affect_dict['term']]['value'] < float(affect_dict['score']):
            self.lexicon[affect_dict['term']] = {'value': float(affect_dict['score']),
                                                 'emotion': affect_dict['AffectDimension']}

    def get_affect(self, word):
        try:
            affect_data = self.lexicon[word]
            logger.debug('\nAffect data for word %s, %s: ', word, affect_data)
            return affect_data
        except KeyError:
            #logger.debug('\nNo affect data for word %s: ', word)
            return None


class NRC_VAD:
    def __init__(self):
        self.lexicon = {}
        with open('dialogue_system/emotion_recognition/utils/language/nrc/NRC-VAD-Lexicon.txt', 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for term in reader:
                self.add_lexicon(term)
            logger.debug('Done reading VAD lexicon!')

    def add_lexicon(self, affect_dict):
        d = {affect_dict['Word']: {'valence': float(affect_dict['Valence']), 'arousal': float(affect_dict['Arousal']),
                                   'dominance': float(affect_dict['Dominance'])}}
        self.lexicon.update(d)

    def get_affect(self, word):
        try:
            affect_data = self.lexicon[word]
            return affect_data
        except KeyError:
            logger.debug('\nNo VAD data for word : ', word)
            return None


class NRC_all:
    def __init__(self):
        vad = NRC_VAD()
        emo = NRC_AffectIntensity()

        self.lexicon = vad.lexicon
        self.add_lexicon(emo.lexicon)

        logger.debug('Finished adding both lexicons!')

    def add_lexicon(self, affect_dict):
        for key, value in affect_dict.items():
            if key not in self.lexicon.keys():
                self.lexicon.update({key: value})
            else:
                for k, v in value.items():
                    if k not in self.lexicon[key].keys():
                        self.lexicon[key].update({k:v})
                    else:
                        logger.debug('Already have values for :', key, value)
                        pass

    def get_affect(self, word):
        try:
            affect_data = self.lexicon[word]
            return affect_data
        except KeyError:
            logger.debug('\nNo data for word : ', word)
            return None
