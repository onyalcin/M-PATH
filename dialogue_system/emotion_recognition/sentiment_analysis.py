from pycorenlp import StanfordCoreNLP

from .utils.language.so_cal.sentiment_calculator.SO_Calc_Nilay import SO_Calculator
from .utils.language.vader_sentiment.vaderSentiment.vaderSentiment_nilay import SentimentIntensityAnalyzer


# Returning sentiment between -1 to 1, neg, pos
class VaderSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, sentence):
        vs = self.analyzer.polarity_scores(sentence)
        # Vader returns sentiments in  {'neg': 0.778, 'neu': 0.222, 'pos': 0.0, 'compound': -0.5423} format
        # We will only take the compound paremeter
        print("{:-<65} {}".format(sentence, str(vs))) # TODO: How to return the sentiments
        return vs['compound']


class SOCALSentimentAnalyzer:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')
        self.standford_annotators = 'tokenize,ssplit,pos'

    def str_process(self, row_string):
        processed_json = self.nlp.annotate(row_string, properties={
            'annotators': self.standford_annotators,
            'outputFormat': 'json'
        })
        return processed_json

    @staticmethod
    def output_preprocessed_data(json_input):
        rows = []
        for sent in json_input['sentences']:
            parsed_sent = " ".join([t['originalText'] + "/" + t['pos'] for t in sent['tokens']])
            rows.append(parsed_sent)
        return rows

    def analyze(self, sentence):
        parsed_json = self.str_process(sentence)
        rows = self.output_preprocessed_data(parsed_json)
        for row in rows:
            print("Start calculating SO of :", row)
            calculator = SO_Calculator()
            sent = calculator.get_output(rows)
            # TODO: check if this is really between -5 and 5
            return sent/5.0 # normalizing the sentiment value