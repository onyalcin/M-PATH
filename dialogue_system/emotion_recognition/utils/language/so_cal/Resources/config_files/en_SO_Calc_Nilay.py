# Configuration file for SO_Calc.py
# Note that deleting entries from this configuration file will cause SO-CAL to stop working

# Dictionaries

init_dict = {}

init_dict['dic_dir'] = '../Resources/dictionaries/English/'
init_dict['adj_dict'] = 'adj_dictionary1.11.txt'
init_dict['adv_dict'] = 'adv_dictionary1.11.txt'
init_dict['noun_dict'] = 'noun_dictionary1.11.txt'
init_dict['verb_dict'] = 'verb_dictionary1.11.txt'
init_dict['int_dict'] = 'int_dictionary1.11.txt'
init_dict['extra_dict'] = ''
# the extra dictionary allows for additional (genre-specific) words that supplement
# or override the the definitions in the four main dictionaries. Each type should be under
# an appropriate heading, i.e. "verbs", "nouns", "adjectives", "adverbs", and "intensifiers"


# Flags

init_dict['language'] = 'English' # English or Spanish
init_dict['use_adjectives'] = True
init_dict['use_nouns'] = True
init_dict['use_verbs'] = True
init_dict['use_adverbs'] = True
init_dict['use_intensifiers'] = True
init_dict['use_negation'] = True
init_dict['use_comparatives'] = True
init_dict['use_superlatives'] = True
init_dict['use_multiword_dictionaries'] = True
init_dict['use_extra_dict'] = False
init_dict['use_XML_weighing'] = True
init_dict['use_weight_by_location'] = False
init_dict['use_irrealis'] = True # irrealis markers (e.g. modals) nullify the SO value of words
init_dict['use_imperative'] = False # nullify words that appear in imperatives
init_dict['use_subjunctive'] = False # nullify words that appear in subjunctives, only relevant to Spanish
init_dict['use_conditional'] = False # nullify words that appear in conditionals, only relevant to Spanish
init_dict['use_highlighters'] = True # highlighers amplify (or deamplify) the SO value of words
init_dict['use_cap_int'] = True # intensify words in all caps
init_dict['fix_cap_tags'] = True # try to fix mistagged capitalized words
init_dict['use_exclam_int'] = True # intensify words in sentences with exclamation marks
init_dict['use_quest_mod']= True # don't use words that appear in questions
init_dict['use_quote_mod'] = True # don't use words that appear in quotes
init_dict['use_definite_assertion'] = True # Presence of definites indicates assertion, ignore irrealis 
init_dict['use_clause_final_int'] = True # look for verb intensifiers at the edge of VPs
init_dict['use_heavy_negation'] = True # multiply all negative words by a fixed amount
init_dict['use_word_counts_lower'] = True # lower SO_value of words that appear often in text
init_dict['use_word_counts_block'] = False # do not assign SO value to repeated words
init_dict['use_blocking'] = True # a strong modifier will block items of opposite polarity
init_dict['adv_learning'] = True # add to the adverb dictionary by using the adjective dictionary
init_dict['limit_shift'] = False #limit negation shifting, no shifting beyond switched value
init_dict['neg_negation_nullification'] = True # the negation of negative terms simply nullifies them.
init_dict['polarity_switch_neg'] = False # switch polarity on negated items instead of shift
init_dict['simple_SO'] = False # Treat the SO of words as binary rather than as a continuous value
                 # Also simplifies intensification to +1 -1
init_dict['restricted_neg'] = {'JJ' : True, 'RB' : True, 'NN' : True, 'VB' : True}
init_dict['use_boundary_words'] = True # disable only if preprocessor already segments into clauses
init_dict['use_boundary_punctuation'] = True # disable only if preprocessor already segments into clauses

# Modifiers

init_dict['adj_multiplier'] = 1 #multiply all adjectives by this amount
init_dict['adv_multiplier'] = 1 #mulitply all adverbs by this amount
init_dict['verb_multiplier'] = 1 #multiply all verbs by this amount
init_dict['noun_multiplier'] = 1 #multiply all nouns by this amount
init_dict['int_multiplier'] = 1 # multiply all intensified word groups by this amount
init_dict['neg_multiplier'] = 1.5 # multiply all negative word groups by this amount
init_dict['capital_modifier'] = 2 # multiply all fully capitalized words by this amount
init_dict['exclam_modifier'] = 2 # multiply words appearing in exclamations by this amount
init_dict['verb_neg_shift'] = 4 # shift negated verbs by this amount
init_dict['noun_neg_shift'] = 4 # shift negated nouns by this amount
init_dict['adj_neg_shift'] = 4 # shift negated adjectives by this amount
init_dict['adv_neg_shift'] = 4 # shift negated adverbs by this amount
init_dict['blocker_cutoff'] = 3 # lowest (absolute) SO value that will block opposite polarity


# Ouput

init_dict['output_calculations'] = True # output the calculation of SO to richout
init_dict['output_sentences'] = True # output the SO_Value for each sentence (clause) in text to richout
init_dict['output_unknown'] = True # unknown closed-class words will be outputed to search
init_dict['output_used'] = False # used closed-class words will be outputed to search
init_dict['output_used_lemma'] = False # for used words, output the lower-case lemma
init_dict['search'] = ['expected', 'expecting', 'expect', 'hoped', 'hope,hoping', 'wanted', 'want', 'wanting,thought', 'supposed', 'figured', 'guessed', 'imagined', 'could', 'should', 'would', 'might', 'must', 'ought', 'may', 'anything', 'any', 'used'] # search can be used to optionally output sentences with certain words
init_dict['contain_all_words'] = True # only sentences that contain all search words are outputed

# Lists

init_dict['highlighters'] = {'but' : 2, 'although':.5} # these words increase or decrease the SO weight of words later in a sentence
init_dict['irrealis'] = ['expected', 'expecting', 'expect', 'hoped', 'hope,hoping', 'wanted', 'want', 'wanting', 'doubt', 'doubted', 'doubting', 'thought,supposed', 'figured', 'guessed', 'imagined', 'could', 'should', 'would', 'might', 'must', 'ought', 'may', 'anything', 'any', 'used'] #irrealis blockers
init_dict['boundary_words'] = ['but', 'and', 'or', 'since', 'because', 'while', 'after', 'before', 'when', 'though', 'although', 'if', 'which', 'despite', 'so', 'then', 'thus', 'where', 'whereas', 'until', 'unless'] #these words stop a backward search for negators, highlighters, modifier blockers, and irrealis blockers
init_dict['weight_tags'] = {'COMMENT': 1, 'DESCRIBE': 0, 'FORMAL': 0, 'DESCRIBE+COMMENT': .1, 'BACKGROUND': 0, 'INTERPRETATION': 0} 
# words contained within XML tags with these names will be weighed 
init_dict['weights_by_location'] = {'0-1/5':.3, '4/5-1': .3} # words within fraction range will be weighed, default is 1