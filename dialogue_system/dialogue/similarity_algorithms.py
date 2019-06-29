from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer # TODO: Fix the nltk wordnet download!!!
from nltk.corpus import wordnet
from .text_normalization import clean_list
from fuzzywuzzy import process, fuzz
import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=FutureWarning, module='gensim')
import gensim
import logging

logger = logging.getLogger().getChild(__name__)


def fuzzy_similarity(choices, sentence):
    choices = clean_list(choices)
    match = process.extractOne(sentence, choices, scorer=fuzz.token_set_ratio)
    if match[1] > 0.9:
        return choices.index(match[0])  # FIXME: does not return the top result number
    else:
        return None


'''barebones Tfidf'''
def TFIDF_similarity(sentences, sentence):
    #sentences = clean_list(sentences)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([sentence]+sentences)
    similarity = cosine_similarity(tfidf[0], tfidf[1:])
    maxx = max(similarity[0])
    top = np.argmax(similarity[0])
    if maxx >= 0.7:
        return sentences[top], top
    else:
        return None, None


'''without stopwords'''
def TFIDF_similarity_stopwords(sentences, sentence):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([sentence]+sentences)
    similarity = cosine_similarity(tfidf[0], tfidf[1:])
    maxx = max(similarity[0])
    top = np.argmax(similarity[0])
    if maxx >= 0.7:
        return sentences[top], top
    else:
        return None, None


''' with Lemmatize'''
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize('start')
def lemma_tokenize(text):
    tokens = word_tokenize(text)
    tokens = pos_tag(tokens)
    logger.debug('Pos tags %s', tokens)
    stems = []
    for item in tokens:
        logger.debug('Getting lemma for item %s', item) # FIXME!!! Soooooo sloooow!!
        #lemma_item = wordnet.lemmas(item[0], get_wordnet_pos(item[1]))[0]
        #stems.append(WordNetLemmatizer().lemmatize(item[0], get_wordnet_pos(item[1])))
        stems.append(lemmatizer.lemmatize(item[0], get_wordnet_pos(item[1])))
        #stems.append(lemma_item.pertainyms()[0].name())
    return stems


def get_wordnet_pos(treebank_tag):
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

def pre_processer(s): #FIXME: lemma preprocessing
    s = s.lower()
    pass

def spacy(): # FIXME
    import en_core_web_sm
    nlp = en_core_web_sm.load()
    pass

vectorizer = TfidfVectorizer(tokenizer=lemma_tokenize) # TODO!! Initiate this as a class
def TFIDF_similarity_lemmatize(sentences, sentence):
    logger.debug('Getting similarity values %s %s', sentences, sentence)
    #vectorizer = TfidfVectorizer(tokenizer=lemma_tokenize)  # FIXME: remove this to a class if its what we are using
    tfidf = vectorizer.fit_transform([sentence]+sentences)
    similarity = cosine_similarity(tfidf[0], tfidf[1:])
    maxx = max(similarity[0])
    top = np.argmax(similarity[0])
    logger.debug('Similarity done')
    if maxx >= 0.7:
        return sentences[top], top
    else:
        return None, None


def TFIDF_search_lemmatize(sentences, sentence):
    #vectorizer = TfidfVectorizer(tokenizer=lemma_tokenize)
    tfidf = vectorizer.fit_transform([sentence]+sentences)
    similarity = cosine_similarity(tfidf[0], tfidf[1:])
    maxx = max(similarity[0])
    top = np.argmax(similarity[0])
    if maxx >= 0.7:
        return sentences[top], top
    else:
        return None, None


"""comparing positive vs negative groups"""
def TFIDF_twogroups(sentences, sentence):
    l = len(sentences)
    negatives = [sentences[i] for i in range(l) if i <= l/2]
    positives = list(set(sentences) - set(negatives))

    result = TFIDF_similarity_lemmatize([' '.join(negatives), ' '.join(positives)], sentence)
    if result is not None:
        if result == 1:
            return len(sentences)-1  # FIXME: does not return the top result
    return result

'''
path = os.path.join('.','dialogue_system','dialogue', 'lee_size50_min2_iter55')
model =gensim.models.doc2vec.Doc2Vec.load(path)


def doc2vec_similarity(sentence, sentences):  # sentences list
    similarity = []
    target_vector = gensim.utils.simple_preprocess(sentence)
    i = 0
    for s in sentences:
        similarity.append(model.docvecs.similarity_unseen_docs(model, target_vector, gensim.utils.simple_preprocess(s)))
    top = np.argmax(similarity)
    if max(similarity) > 0.7:
        return sentences[top]
    else:
        return None
'''
