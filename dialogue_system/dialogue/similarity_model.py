import fasttext as ft
import logging

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer  # TODO: Fix the nltk wordnet download!!!
from nltk.corpus import wordnet
import warnings
import numpy as np
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=FutureWarning, module='gensim')

logger = logging.getLogger().getChild(__name__)


class LikertSimilarity(object):
    def __init__(self):
        self.classifier = ft.load_model("dialogue_system\\dialogue\\utils\\likert\\likert.bin")
        self.threshold = 0.8

    def predict(self, answer):
        pred, prob = self.classifier.predict(answer)
        logger.debug('Prediction for likert is %s %s', pred[0], prob[0])
        if prob[0] > self.threshold:
            return pred[0].lstrip('__label__')
        else:
            return None


class TfidfSimilarity(object):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.lemmatizer.lemmatize('start')

        self.vectorizer = TfidfVectorizer(tokenizer=self.lemma_tokenize)

    def lemma_tokenize(self, text):
        tokens = word_tokenize(text)
        tokens = pos_tag(tokens)
        logger.debug('Pos tags %s', tokens)
        stems = []
        for item in tokens:
            logger.debug('Getting lemma for item %s', item)
            stems.append(self.lemmatizer.lemmatize(item[0], self.get_wordnet_pos(item[1])))
        return stems

    def get_wordnet_pos(self, treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v)
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def TFIDF_similarity_lemmatize(self, sentences, sentence):
        logger.debug('Getting similarity values %s %s', sentences, sentence)
        tfidf = self.vectorizer.fit_transform([sentence] + sentences)
        similarity = cosine_similarity(tfidf[0], tfidf[1:])
        maxx = max(similarity[0])
        top = np.argmax(similarity[0])
        logger.debug('Similarity done')
        if maxx >= 0.7:
            return sentences[top], top
        else:
            return None, None
