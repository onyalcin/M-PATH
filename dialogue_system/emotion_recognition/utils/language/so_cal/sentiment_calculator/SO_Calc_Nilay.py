# coding: utf-8
######## Semantic Orientation Calculator (SO-CAL) #######
# The code is is majorly from Julian Brooke's code written in 2008
# Changes are made to allow the code running in Python3.5
# The Semantic Orientation Calculator take a properly formated self.textfile and
# (optionally) a file of span self.weights and calculates a semantic orietation (SO)
# for the file based on the appearance of words carrying positive or negative
# sentiment, multiplied by weight according to their location in the self.text
#
# SO-CAL v1.0 (written in perl) supported adjectives, nouns, verbs, adjectives,
# intensification, modals, and negation.
#
# Major Changes since 1.0
# added support for multi-word dictionaries
# added extra weighing of negative phrases
# added lowered weight on (or nullification of) repeated items
# added intensification and nullification based on punctuation
# added intensification based on captialization
# added intensification based on other "highlighting" words
# added clause final intensification for verbs
# added modifier blocking of opposite polarity SO values
# added part-of-speech-specific restricted negation, by word or tag
# added clause boundary words that block backward searches
# added negation-external intensification
# added optional negation shifting limits
# added tag fixing for all_caps words
# added external weighing by use of XML tags
# added weighing based on part of speech
# added external ini file
# added flexible weighing by location in self.text
# added to the list of self.irrealis markers (modals)
# added definite determiner overriding of self.irrealis nullification
# improved handling of "too"
# improved rich output to show calculation
# fixed some small stemming problems
# intensification and negation are now totally separate
#
#
# Changes since V1.11
# merged Spanish and English calculators
# expanded dictionaries
# various minor bug fixes
# XML weighting with real number tags
# added negative negation nullification
# some lists moved to config file
# now uses boundares as indicated by newlines in the input as search
# and sentence self.boundaries

import operator
import argparse
import os
import json


class SO_Calculator:
    def __init__(self, language="English"):
        self.config_dir = 'dialogue_system/emotion_recognition/utils/language/so_cal/Resources/config_files/'
        self.language = language

        ### Initialize self.language Specs ###
        if self.language == "English":
            self.json_to_attr('init_ENG.json')
            self.json_to_attr('word_list_ENG.json')
        elif self.language == "Spanish":
            self.json_to_attr('word_list_SPA.json')
            self.json_to_attr('init_SPA.json')  # TODO: didnt make this yet

        ### Dictionaries ###
        self.adj_dict_path = self.dic_dir + self.adj_dict
        self.adv_dict_path = self.dic_dir + self.adv_dict
        self.noun_dict_path = self.dic_dir + self.noun_dict
        self.verb_dict_path = self.dic_dir + self.verb_dict
        self.int_dict_path = self.dic_dir + self.int_dict
        if self.use_extra_dict and self.extra_dict:
            self.extra_dict_path = self.dic_dir + self.extra_dict
        else:
            self.extra_dict_path = False
        self.adj_dict = {}  # simple (single-word) dictionaries
        self.adv_dict = {}
        self.noun_dict = {}
        self.verb_dict = {}
        self.int_dict = {}
        self.c_adj_dict = {}  # complex (multi-word) dictionaries
        self.c_adv_dict = {}
        self.c_noun_dict = {}
        self.c_verb_dict = {}
        self.c_int_dict = {}
        self.new_adv_dict = {}

        self.load_dictionaries()

        ### self.text ###

        self.text = []  # the self.text is a list of word, tag lists
        self.weights = []  # self.weights should be the same length as the self.text, one for each token
        self.word_counts = [{}, {}, {}, {}]  # keeps track of number of times each word lemma appears in the self.text
        self.text_SO = 0  # a sum of the SO value of all the words in the self.text
        self.SO_counter = 0  # a count of the number of SO carrying terms
        self.boundaries = []  # the location of newline self.boundaries from the input

    def json_to_attr(self, json_file):
        file_path = os.path.join(self.config_dir, json_file)
        with open(file_path, 'r') as file:
            config = json.load(file)
            for k, v in config.items():
                setattr(self, k, v)

    def same_lists(self, list1, list2):
        """
        Check if 2 lists exactly the same (same elements, same order)
        :param lst1: list 1
        :param lst2: list 2
        :return: if they are exactly the same, return True, otherwise False
        """
        return list1 == list2

    def get_multiword_entries(self, string):
        ### Coverts the multiword dictionary entry in a file to something that can
        ### be accessed by the calculator
        ### In the dictionary, each word of a multi-word definition is separated by
        ### an underscore. The primary word (the one whose part of speech is the same
        ### as the phrase as a whole, except for intensifiers) should be in parentheses;
        ### it becomes the key (if there are multiple keys, multiple entries are created)
        ### The value of an c_dict is a list of all multi-word phrases a key word
        ### appears in (as a key) and each of these contains a 2-ple: the list all the
        ### words in the phrase, with the key word removed and replaced with a #,
        ### and the SO value for the phrase. If a word or words is modified by an
        ### operator (such as ?,*,+,|, or a number), the operator should be placed in
        ### []--all operators but | appear outside the right bracket
        ### ? = optional, + = one or more, * = zero or more, 2 (3, etc.) = two of these
        ### | = or. INT refers to a word or words in the intensifier dictionary.
        ### with that key (minus the last word), together with the modifier value
        ### ex.: self.c_int_dict["little"] = [[["a", "#"], -0.5]]
        if "#" in string:  # if there is a macro, replace
            for item in self.macro_replace:
                string = string.replace(item, self.macro_replace[item])
        words = string.split("_")
        entry = []
        keyindex = len(words) - 1  # if no parens, default to last word
        for index in range(len(words)):
            word = words[index]
            slot = []
            if word[0] == "(":
                slot.append(1)
                slot.append(word[1:-1].split("|"))
                keyindex = index  # found the key
            elif word[0] == "[":
                ordinality = False
                if word[-1] != "]":
                    ordinality = True
                if ordinality:
                    slot.append(word[-1])
                    word = word[:-1]
                else:
                    slot.append(1)
                slot.append(word[1:-1].split("|"))
            else:
                slot = word
            entry.append(slot)
        final_entries = []
        if not isinstance(entry[keyindex], list):
            key = entry[keyindex]
            entry[keyindex] = "#"
            final_entries = [[key, entry]]
        else:
            for key in entry[keyindex][1]:
                final_entry = []
                for index in range(len(entry)):
                    if index == keyindex:
                        final_entry.append("#")
                    else:
                        final_entry.append(entry[index])
                final_entries.append([key, final_entry])
        return final_entries

    def has_accent(self, word):
        for accent in self.accents:
            if accent in word:
                return True
        return False

    def remove_accents(self, word):
        for accent in self.accents:
            word = word.replace(accent, self.accents[accent])
        return word

    def load_dictionary(self, filepointer, s_dict, c_dict):
        ### General function for loading dictionaries from files and putting them
        ### either in the simple or complex dictionary, as appropriate
        for line in filepointer.readlines():
            pair = line.strip().split()
            if len(pair) == 2:
                if "_" not in pair[0]:  # if single word
                    if self.language == "Spanish" and self.has_accent(pair[0]):
                        s_dict[self.remove_accents(pair[0])] = float(pair[1])
                    s_dict[pair[0]] = float(pair[1])  # put in simple dictionary
                elif self.use_multiword_dictionaries:
                    entries = self.get_multiword_entries(pair[0])
                    for entry in entries:
                        if entry[0] not in c_dict:
                            c_dict[entry[0]] = [[entry[1], float(pair[1])]]
                        else:
                            c_dict[entry[0]].append([entry[1], float(pair[1])])
        filepointer.close()

    def load_extra_dict(self, filepointer):
        ### loads the optional dictionary, which contains entries from all the
        ### various types of words
        s_dict = False
        c_dict = False
        for line in filepointer.readlines():
            line = line.strip()
            if line:
                if line == "adjectives":
                    s_dict = self.adj_dict
                    c_dict = self.c_adj_dict
                elif line == "nouns":
                    s_dict = self.noun_dict
                    c_dict = self.c_noun_dict
                elif line == "verbs":
                    s_dict = self.verb_dict
                    c_dict = self.c_verb_dict
                elif line == "adverbs":
                    s_dict = self.adv_dict
                    c_dict = self.c_adv_dict
                elif line == "intensifiers":
                    s_dict = self.int_dict
                    c_dict = self.c_adv_dict
                elif s_dict:
                    pair = line.split()
                    if "_" not in pair[0]:  # if single word
                        s_dict[pair[0]] = float(pair[1])  # put in simple dictionary
                    elif self.use_multiword_dictionaries:
                        entries = self.get_multiword_entries(pair[0])
                        for entry in entries:
                            if entry[0] not in c_dict:
                                c_dict[entry[0]] = [[entry[1], float(pair[1])]]
                            else:
                                for old_entry in c_dict[entry[0]]:  # duplicate entry
                                    if self.same_lists(old_entry[0], entry[1]):
                                        c_dict[entry[0]].remove(old_entry)
                                c_dict[entry[0]].append([entry[1], float(pair[1])])
        filepointer.close()

    def load_dictionaries(self):
        ### load the five kinds of dictionaries
        self.load_dictionary(open(self.adj_dict_path, encoding="ISO-8859-1"), self.adj_dict, self.c_adj_dict)
        self.load_dictionary(open(self.adv_dict_path, encoding="ISO-8859-1"), self.adv_dict, self.c_adv_dict)
        self.load_dictionary(open(self.verb_dict_path, encoding="ISO-8859-1"), self.verb_dict, self.c_verb_dict)
        self.load_dictionary(open(self.noun_dict_path, encoding="ISO-8859-1"), self.noun_dict, self.c_noun_dict)
        self.load_dictionary(open(self.int_dict_path, encoding="ISO-8859-1"), self.int_dict, self.c_int_dict)
        if self.extra_dict_path:
            self.load_extra_dict(open(self.extra_dict_path, encoding="ISO-8859-1"))
        if self.simple_SO:
            for s_dict in [self.adj_dict, self.adv_dict, self.verb_dict, self.noun_dict]:
                for entry in s_dict:
                    if s_dict[entry] > 0:
                        s_dict[entry] = 2
                    elif s_dict[entry] < 0:
                        s_dict[entry] = -2
            for entry in self.int_dict:
                if self.int_dict[entry] > 0:
                    self.int_dict[entry] = .5
                elif self.int_dict[entry] < 0 and self.int_dict[entry] > -1:
                    self.int_dict[entry] = -.5
                elif self.int_dict[entry] < -1:
                    self.int_dict[entry] = -2
            for c_dict in [self.c_adj_dict, self.c_adv_dict, self.c_verb_dict, self.c_noun_dict]:
                for entry in c_dict:
                    for i in range(len(c_dict[entry])):
                        if c_dict[entry][i][1] > 0:
                            c_dict[entry][i] = [c_dict[entry][i][0], 2]
                        elif c_dict[entry][i][1] < 0:
                            c_dict[entry][i] = [c_dict[entry][i][0], -2]
            for entry in self.c_int_dict:
                for i in range(len(self.c_int_dict[entry])):
                    if self.c_int_dict[entry][i][1] > 0:
                        self.c_int_dict[entry][i] = [self.c_int_dict[entry][i][0], .5]
                    elif self.c_int_dict[entry][i][1] < 0 and self.c_int_dict[entry][i][1] > -1:
                        self.c_int_dict[entry][i] = [self.c_int_dict[entry][i][0], -.5]
                    elif self.c_int_dict[entry][i][1] < -1:
                        self.c_int_dict[entry][i] = [self.c_int_dict[entry][i][0], -2]

    def convert_fraction(self, fraction):
        ### coverts a fraction string into a float
        if "/" not in fraction:
            return float(fraction)
        else:
            fraction = fraction.split("/")
            if len(fraction) == 2:
                return float(fraction[0]) / float(fraction[1])
        return -1

    def is_decimal(self, string):
        decimal_yet = False
        if len(string) == 0:
            return False
        if string[0] == "-":
            string = string[1:]
            if len(string) == 0:
                return False
        for letter in string:
            if not letter.isdigit():
                if not letter == "." or decimal_yet:
                    return False
                else:
                    decimal_yet = True
        return True

    def convert_ranges(self):
        ### converts a list of string ranges in faction form (e.g. ["1/4-1/2", 2]) into a
        ### a list of numerical ranges plus weight (e.g. [0.25, .5, 2]
        new_ranges = []
        for range in self.weights_by_location:
            pair = range.split("-")
            if len(pair) == 2:
                start = self.convert_fraction(pair[0].strip())
                end = self.convert_fraction(pair[1].strip())
                if start >= 0 and start <= 1 and end >= 0 and end <= 1 and start < end:
                    new_ranges.append([start, end, self.weights_by_location[range]])
        return new_ranges

    def fill_text_and_weights(self, input):
        ### Read in the self.textfile. The file is assumed to be properly spaced and tagged,
        ### i.e. there should be a space between every word/tag pair or XML tag
        ### if there are XML tags and those tags have been assigned weight, the weight
        ### will be applied after the opening tag and will be removed at the closing
        ### tag. All XML tags are removed for the SO calculation
        weight = 1.0  # start with weight 1
        temp_weight = 1.0  # keep track of weight before a zero
        for line in input:
            # TODO: deal with weight tags
            line = line.replace("<", " <").replace(">", "> ")
            for word in line.strip().split(" "):
                if word:
                    if word[0] == "<" and word[-1] == ">":  # XML tag
                        XML_tag = word.strip("<>/")
                        if self.use_XML_weighing:
                            if XML_tag in self.weight_tags:
                                weight_modifier = self.weight_tags[XML_tag]
                            elif self.is_decimal(XML_tag):
                                weight_modifier = float(XML_tag)
                            else:
                                weight_modifier = 1
                            if word[1] == "/":
                                if weight_modifier != 0:
                                    weight /= weight_modifier  # remove weight
                                else:
                                    weight = temp_weight  # use pre-zero weight
                            else:
                                if weight_modifier != 0:
                                    weight *= weight_modifier  # add weight
                                else:
                                    temp_weight = weight  # save weight
                                    weight = 0
                    elif "/" in word:
                        self.text.append(word.split("/"))
                        self.weights.append(weight)
            self.boundaries.append(len(self.text))
        if self.use_weight_by_location:  # add location self.weights
            range_dict = self.convert_ranges()
            for i in range(len(self.weights)):
                for interval in range_dict:  # if the current index in range
                    if interval[0] <= float(i) / len(self.weights) and interval[1] > float(i) / len(self.weights):
                        self.weights[i] *= interval[2]  # add the weight
        print("Weights and text:", self.weights, self.text)

    ### English steming functions ###

    def stem_NN(self, NN):
        if NN not in self.noun_dict and NN not in self.c_noun_dict and len(NN) > 2 and NN[-1] == "s":  # boys -> boy
            NN = NN[:-1]
            if NN not in self.noun_dict and NN not in self.c_noun_dict and NN[-1] == "e":  # watches -> watch
                NN = NN[:-1]
                if NN not in self.noun_dict and NN not in self.c_noun_dict and NN[-1] == "i":  # flies -> fly
                    NN = NN[:-1] + "y"
        return NN

    def stem_VB(self, VB, type):
        if type == "" or type == "P" or len(VB) < 4 or VB in self.verb_dict or VB in self.c_verb_dict:
            return VB
        elif type == "D" or type == "N":
            if VB[-1] == "d":
                VB = VB[:-1]  # loved -> love
                if not VB in self.verb_dict and not VB in self.c_verb_dict:
                    if VB[-1] == "e":
                        VB = VB[:-1]  # enjoyed -> enjoy
                    if not VB in self.verb_dict and not VB in self.c_verb_dict:
                        if VB[-1] == "i":
                            VB = VB[:-1] + "y"  # tried -> try
                        elif len(VB) > 1 and VB[-1] == VB[-2]:
                            VB = VB[:-1]  # compelled -> compel
            return VB
        elif type == "G":
            VB = VB[:-3]  # obeying -> obey
            if not VB in self.verb_dict and not VB in self.c_verb_dict:
                if len(VB) > 1 and VB[-1] == VB[-2]:
                    VB = VB[:-1]  # stopping -> stop
                else:
                    VB = VB + "e"  # amusing -> amuse
            return VB
        elif type == "Z" and len(VB) > 3:
            if VB[-1] == "s":
                VB = VB[:-1]  # likes -> like
                if VB not in self.verb_dict and not VB in self.c_verb_dict and VB[-1] == "e":
                    VB = VB[:-1]  # watches -> watch
                    if VB not in self.verb_dict and not VB in self.c_verb_dict and VB[-1] == "i":
                        VB = VB[:-1] + "y"  # flies -> fly
            return VB

    def stem_RB_to_JJ(self, RB):
        ### used to find the adjective that is the stem of an adverb so that the adverb
        ### can be added automatically to the dictionary
        JJ = RB
        if len(JJ) > 3 and JJ[-2:] == "ly":
            JJ = JJ[:-2]  # sharply -> sharp
            if not JJ in self.adj_dict:
                if JJ + "l" in self.adj_dict:
                    JJ += "l"  # full -> fully
                elif JJ + "le" in self.adj_dict:
                    JJ += "le"  # simply -> simple
                elif JJ[-1] == "i" and JJ[:-1] + "y" in self.adj_dict:
                    JJ = JJ[:-1] + "y"  # merrily -> merry
                elif len(JJ) > 5 and JJ[-2:] == "al" and JJ[:-2] in self.adj_dict:
                    JJ = JJ[:-2]  # angelic -> angelically
        return JJ

    def stem_ative_adj(self, JJ):
        # this function does stemming for both comparative and superlative adjectives
        # after the suffix "er" or "est" has been removed
        if JJ not in self.adj_dict:
            if JJ + "e" in self.adj_dict:
                JJ += "e"  # abler/ablest -> able
            elif JJ[:-1] in self.adj_dict:
                JJ = JJ[:-1]  # bigger/biggest -> big
            elif JJ[-1] == "i" and JJ[:-1] + "y" in self.adj_dict:
                JJ = JJ[:-1] + "y"  # easier/easiest -> easy
        return JJ

    def stem_comp_JJ(self, JJ):
        if JJ[-2:] == "er":
            JJ = self.stem_ative_adj(JJ[:-2])  # fairer -> fair
        return JJ

    def stem_super_JJ(self, JJ):
        if JJ[-3:] == "est":
            JJ = self.stem_ative_adj(JJ[:-3])  # fairest -> fair
        return JJ

    ### Spanish Stemming Fuctions

    def stem_NC(self, NC):
        if NC not in self.noun_dict and len(NC) > 2 and NC[-1] == "s":  # diplomas -> diploma
            NC = NC[:-1]
        if NC not in self.noun_dict and NC not in self.c_noun_dict and len(NC) > 1:
            if NC[-1] == "a":
                NC = NC[:-1] + "o"  # hermanas -> hermano
            elif NC[-1] == "e":  # actor -> actores
                NC = NC[:-1]
        return NC

    def stem_AQ(self, AQ):
        if AQ not in self.adj_dict and len(AQ) > 2 and AQ[-1] == "s":  # buenos -> bueno
            AQ = AQ[:-1]
        if AQ not in self.adj_dict and AQ not in self.c_adj_dict and len(AQ) > 1:
            if AQ[-1] == "a":  # buena -> bueno
                AQ = AQ[:-1] + "o"
            elif AQ[-1] == "e":  # -> watch
                AQ = AQ[:-1]
        return AQ

    def stem_RG_to_AQ(self, RG):
        ### used to find the adjective that is the stem of an adverb so that the adverb
        ### can be added automatically to the dictionary
        AQ = RG
        if len(AQ) > 6 and AQ[-5:] == "mente":
            AQ = AQ[:-5]  # felizmente -> feliz
            if not AQ in self.adj_dict:
                if AQ[-1] == "a":
                    AQ = AQ[:-1] + "o"  # nuevamente -> nuevo
        return AQ

    def stem_super_AQ(self, AQ):
        # this function removes "isima" or "isimo" from the word
        if AQ not in self.adj_dict:
            if len(AQ) > 6 and AQ[-5:] in [chr(237) + "sima", chr(237) + "simo", "isima", "isimo"]:
                AQ = AQ[:-5]
                if AQ not in self.adj_dict:
                    if AQ[-2:] == "qu":
                        AQ = AQ[:-2] + "co"
                    elif AQ[-2] == "gu":
                        AQ = AQ[:-1] = "o"
                    else:
                        AQ += "o"
        return AQ

    ### self.language general stemming functions ###

    def stem_noun(self, noun):
        if self.language == "English":
            return self.stem_NN(noun)
        elif self.language == "Spanish":
            return self.stem_NC(noun)

    def stem_adv_to_adj(self, adverb):
        if self.language == "English":
            return self.stem_RB_to_JJ(adverb)
        elif self.language == "Spanish":
            return self.stem_RG_to_AQ(adverb)

    def stem_super_adj(self, adj):
        if self.language == "English":
            return self.stem_super_JJ(adj)
        elif self.language == "Spanish":
            return self.stem_super_AQ(adj)

    ### General functions ###

    def get_word(self, pair):
        return pair[0]  # get word from (word, tag) pair

    def get_tag(self, pair):
        return pair[1]  # get tag from (word, tag) pair

    def sum_word_counts(self, word_count_dict):
        ### gives the total count in a word count dictionary
        count = 0
        for word in word_count_dict:
            count += word_count_dict[word]
        return count

    def find_intensifier(self, index):
        ### this function determines whether the given index is the last word (or,
        ### trivially, the only word) in an intensifier. If so, it returns a list
        ### containing, as its first element, the length of the intensifier and,
        ### as its second element, the modifier from the relevant intensifier dictionary
        if index < 0 or index >= len(self.text) or self.get_tag(
                self.text[index]) == "MOD":  # already modifying something
            return False
        if self.get_word(self.text[index]).lower() in self.c_int_dict:  # might be complex
            for word_mod_pair in self.c_int_dict[self.get_word(self.text[index]).lower()]:
                if self.same_lists(word_mod_pair[0][:-1], map(str.lower, map(self.get_word, self.text[index - len(
                        word_mod_pair[0]) + 1:index]))):
                    return [len(word_mod_pair[0]), word_mod_pair[1]]
        if self.get_word(self.text[index]).lower() in self.int_dict:  # simple intensifier
            modifier = self.int_dict[self.get_word(self.text[index]).lower()]
            if self.get_word(self.text[index]).isupper() and self.use_cap_int:  # if capitalized
                modifier *= self.capital_modifier  # increase intensification
            return [1, modifier]
        return False

    def match_multiword_f(self, index, words):
        ### this function recursively matches the (partial) multi-word dictionary entry
        ### (words) with the corresponding part of the self.text (from index)
        ### the function returns a list containing the number of words matched (or -1
        ### if the match failed) and the value of any intensifier found
        if len(words) == 0:
            return [0, 0]  # done
        else:
            current = words[0]
            if not isinstance(current, list):
                current = [1, [current]]  # unmodified words should be appear once
            if current[0] == "0":
                return self.match_multiword_f(index, words[1:])  # this word done
            if current[0] == "*" or current[0] == "?":  # word optional - try
                temp = self.match_multiword_f(index, words[1:])  # without first
                if temp[0] != -1:
                    return temp
            if index == len(self.text):
                return [-1, 0]  # reached the end of the self.text
            match = False
            for word_or_tag in current[1]:
                if word_or_tag.islower():  # match by word
                    match = match or self.get_word(self.text[index]).lower() == word_or_tag
                elif word_or_tag.isupper():  # match by tag
                    if word_or_tag == "INT":  # if looking for a intensifiers
                        i = 1
                        while index + i < len(self.text) and self.text[index + i][0] not in self.sent_punct:
                            intensifier = self.find_intensifier(index + i - 1)
                            if intensifier and intensifier[0] == i:
                                result = self.match_multiword_f(index + i, words[1:])
                                if result[0] != -1:
                                    return [result[0] + i, intensifier[1]]
                            i += 1
                    else:
                        match = match or self.get_tag(self.text[index]) == word_or_tag
            if not match:
                return [-1, 0]
            else:
                if current[0] == "*":
                    temp = self.match_multiword_f(index + 1, words)
                elif current[0] == "+":
                    temp = self.match_multiword_f(index + 1, [["*", current[1]]] + words[1:])
                elif current[0] == "?":
                    temp = self.match_multiword_f(index + 1, words[1:])
                else:
                    temp = self.match_multiword_f(index + 1, [[str(int(current[0]) - 1), current[1]]] + words[1:])
                if temp[0] == -1:
                    return temp  # failed
                else:
                    return [temp[0] + 1, temp[1]]  # success

    def match_multiword_b(self, index, words):
        ### same as self.match_multiword_f, except it looks in the other direction
        if len(words) == 0:
            return [0, 0]
        else:
            current = words[-1]
            if not isinstance(current, list):
                current = [1, [current]]
            if current[0] == "0":
                return self.match_multiword_b(index, words[:-1])
            if current[0] == "*" or current[0] == "?":
                temp = self.match_multiword_b(index, words[:-1])
                if temp[0] != -1:
                    return temp
            if index == -1:
                return [-1, 0]
            match = False
            for word_or_tag in current[1]:
                if word_or_tag.islower():
                    match = match or self.get_word(self.text[index]).lower() == word_or_tag
                elif word_or_tag.isupper():
                    if word_or_tag == "INT":
                        intensifier = self.find_intensifier(index)
                        if intensifier:
                            i = intensifier[0]
                            result = self.match_multiword_b(index - i, words[:-1])
                            if result[0] != -1:
                                return [result[0] + i, intensifier[1]]
                    else:
                        match = match or self.get_tag(self.text[index]) == word_or_tag
            if not match:
                return [-1, 0]
            else:
                if current[0] == "*":
                    temp = self.match_multiword_b(index - 1, words)
                elif current[0] == "+":
                    temp = self.match_multiword_b(index - 1, words[:-1] + [["*", current[1]]])
                elif current[0] == "?":
                    temp = self.match_multiword_b(index - 1, words[:-1])
                else:
                    temp = self.match_multiword_b(index - 1, words[:-1] + [[str(int(current[0]) - 1), current[1]]])
                if temp[0] == -1:
                    return temp
                else:
                    return [temp[0] + 1, temp[1]]

    def find_multiword(self, index, dict_entry_list):
        ### this function determines whether the words surrounding the key word at
        ### index match one of the dictionary definitions in dict_entry_list. If so,
        ### it returns a list containing the SO value, the number of words in the phrase,
        ### that are to the left of index, the number of words to the right, and the
        ### value of any intensifier. Any word specifically designated in the defintion
        ### will have its tag changed to "MOD" so that it will not be counted twice
        for dict_entry in dict_entry_list:
            words = dict_entry[0]
            SO = dict_entry[1]
            start = words.index("#")
            intensifier = 0
            if start < len(words) - 1:
                countforward, int_temp = self.match_multiword_f(index + 1, words[start + 1:])
                if int_temp != 0:
                    intensifier = int_temp
            else:
                countforward = 0
            if start > 0:
                (countback, int_temp) = self.match_multiword_b(index - 1, words[:start])
                if int_temp != 0:
                    intensifier = int_temp
            else:
                countback = 0
            if countforward != -1 and countback != -1:
                for i in range(index - countback, index + countforward + 1):
                    if self.get_word(self.text[i]) in dict_entry[0]:
                        self.text[i][1] = "MOD"
                return [SO, countback, countforward, intensifier]
        return False

    def words_within_num(self, index, words_tags, num):
        ### check to see if something in words_tags is within num of index (including
        ### index), returns true if so
        while num > 0:
            if self.get_word(self.text[index]) in words_tags or self.get_tag(self.text[index]) in words_tags:
                return True
            num -= 1
            index -= 1
        return False

    def get_sentence(self, index):
        ### extracts the sentence (a string) that contains the given index, for searching
        sent_start = index
        sent_end = index + 1
        while sent_start > 0 and sent_start not in self.boundaries:
            sent_start -= 1
        while sent_end < len(self.text) and sent_end not in self.boundaries:
            sent_end += 1
        return " ".join(map(self.get_word, self.text[sent_start: sent_end]))

    def get_sentence_no(self, index):
        ### returns the sentence number, based on the orignal self.text newlines
        while index not in self.boundaries:
            index += 1
        return self.boundaries.index(index)

    def get_sent_punct(self, index):
        ### get the next sentence punctuation (e.g. ?, !, or .) after the given index
        while self.text[index][0] not in self.sent_punct:
            if index == len(self.text) - 1:  # if the end of the self.text is reached
                return "EOF"
            index += 1
        return self.get_word(self.text[index])

    def at_boundary(self, index):
        if index + 1 in self.boundaries:
            return True
        elif self.use_boundary_punctuation and self.get_word(self.text[index]) in self.punct:
            return True
        elif self.use_boundary_words and self.get_word(self.text[index]) in self.boundary_words:
            return True
        else:
            return False

    def has_sent_irrealis(self, index):
        ### Returns true if there is a self.irrealis marker in the sentence and no
        ### punctuation or boundary word intervenes between the marker and the index
        if not (self.use_definite_assertion and self.words_within_num(index, self.definites, 1)):
            while index != -1 and not self.at_boundary(index):
                if self.get_word(self.text[index]).lower() in self.irrealis:
                    return True
                if self.language == "Spanish":
                    tag = self.get_tag(self.text[index])
                    if len(tag) == 4 and tag[0] == "V" and (
                                    (tag[2] == "M" and self.use_imperative) or (tag[2] == "S" and self.use_subjunctive) or (
                                            tag[3] == "C" and self.use_conditional)):
                        return True
                index -= 1
        return False

    def get_sent_highlighter(self, index):
        ### If there is a word in the sentence prior to the index but before a boundary
        ### marker (including a boundary marker) in the highlighter list, return it
        while index != -1 and not self.at_boundary(index):
            if self.get_word(self.text[index]).lower() in self.highlighters:
                return self.get_word(self.text[index]).lower()
            else:
                index -= 1
        return False

    def find_negation(self, index, word_type):
        ### looks backwards for a negator and returns its index if one is found and
        ### there is no intervening puctuation or boundary word. If restricted negation
        ### is used (for the given word type), the search will only continue if each
        ### word or its tag is in the skipped list for its type
        search = True
        found = -1
        while search and not self.at_boundary(index) and index != -1:
            current = self.get_word(self.text[index]).lower()
            if current in self.negators:
                search = False
                found = index
            if self.restricted_neg[word_type] and current not in self.skipped[word_type] and self.get_tag(
                    self.text[index]) not in self.skipped[word_type]:
                search = False
            index -= 1
        return found

    def is_blocker(self, SO, index):
        if index > -1 and index < len(self.text) and len(self.text[index]) == 2:
            (modifier, tag) = self.text[index]
            if tag == self.adv_tag and modifier in self.adv_dict and abs(
                    self.adv_dict[modifier]) >= self.blocker_cutoff:
                if abs(SO + self.adv_dict[modifier]) < abs(SO) + abs(self.adv_dict[modifier]):
                    return True
            elif tag == self.adj_tag and modifier in self.adj_dict and abs(
                    self.adj_dict[modifier]) >= self.blocker_cutoff:
                if abs(SO + self.adj_dict[modifier]) < abs(SO) + abs(self.adj_dict[modifier]):
                    return True
            elif tag[:2] == self.verb_tag and modifier in self.verb_dict and abs(
                    self.verb_dict[modifier]) >= self.blocker_cutoff:
                if abs(SO + self.verb_dict[modifier]) < abs(SO) + abs(self.verb_dict[modifier]):
                    return True

    def find_blocker(self, SO, index, POS):
        ### this function tests if the item at index is of the correct type, orientation
        ### and strength (as determined by self.blocker_cutoff) to nullify a word having the
        ### given SO value
        stop = False
        while index > 0 and not stop and not self.at_boundary(index):
            if len(self.text[index - 1]) == 2:
                (modifier, tag) = self.text[index - 1]
                if self.is_blocker(SO, index - 1):
                    return True
                if not modifier in self.skipped[POS] and not tag[:2] in self.skipped[POS]:
                    stop = True
            index -= 1
        return False

    def find_VP_boundary(self, index):
        ### forward search for the index immediately preceding punctuation or a boundary
        ### word or punctuation. Used to find intensifiers remote from the verb
        while not self.at_boundary(index) and index < len(self.text) - 1:
            index += 1
        return index

    def is_in_predicate(self, index):
        ### backwards search for a verb of any kind. Used to determine if a comparative
        ### or superlative adjective is in the predicate
        while not self.at_boundary(index) and index > 0:
            index -= 1
            tag = self.get_tag(self.text[index])
            if (self.language == "English" and tag[:2] == "VB" or tag in ["AUX", "AUXG"]) or (
                            self.language == "Spanish" and tag[0] == "V"):
                return True
        return False

    def is_in_imperative(self, index):
        ### Tries to determine if the word at index is in an imperative based on whether
        ### first word in the clause is a VBP (and not a question or within the
        ### scope of a definite determiner)
        if self.get_sent_punct(index) != "?" and not (self.words_within_num(index, self.definites, 1)):
            i = index
            while i > -1 and self.get_word(self.text[i]) not in self.sent_punct:
                if self.at_boundary(index):
                    return False
                i -= 1
            (word, tag) = self.text[i + 1]
            if (tag == "VBP" or tag == "VB") and word.lower() not in ["were", "was", "am"]:
                return True
        return False

    def is_in_quotes(self, index):
        ### check to see if a particular word is contained within quotation marks.
        ### looks to a sentence boundary on the left, and one past the sentence
        ### boundary on the right; an item in quotes should have an odd number of
        ### quotation marks in the sentence on either sides
        quotes_left = 0
        quotes_right = 0
        found = False
        current = ""
        i = index
        while current not in self.sent_punct and i > -1:
            current = self.get_word(self.text[i])
            if current == '"' or current == "'":
                quotes_left += 1
            i -= 1
        if operator.mod(quotes_left, 2) == 1:
            current = ""
            i = index
            while not found and current not in self.sent_punct and i < len(self.text):
                current = self.get_word(self.text[i])
                if current == '"' or current == "'":
                    quotes_right += 1
                i += 1
            if (quotes_left - quotes_right == 1) and i < len(self.text) - 1 and self.get_word(self.text[i + 1]) == '"':
                quotes_right += 1
            if operator.mod(quotes_right, 2) == 1:
                found = True
        return found

    def apply_other_modifiers(self, SO, index, leftedge):
        ### several modifiers that apply equally to all parts of speech based on
        ### their context. Words in all caps, in a sentences ending with an
        ### exclamation mark, or with some other highlighter are intensified,
        ### while words appearing in a question or quotes or with some other
        ### self.irrealis marker are nullified
        output = []
        if self.use_cap_int and self.get_word(self.text[index]).isupper():
            output.append("X " + str(self.capital_modifier) + " (CAPITALIZED)")
            SO *= self.capital_modifier
        if self.use_exclam_int and self.get_sent_punct(index) == "!":
            output.append("X " + str(self.exclam_modifier) + " (EXCLAMATION)")
            SO *= self.exclam_modifier
        if self.use_highlighters:
            highlighter = self.get_sent_highlighter(leftedge)
            if highlighter:
                output.append("X " + str(self.highlighters[highlighter]) + " (HIGHLIGHTED)")
                SO *= self.highlighters[highlighter]
        if self.use_quest_mod and self.get_sent_punct(index) == "?" and not (
                    self.use_definite_assertion and self.words_within_num(leftedge, self.definites, 1)):
            output.append("X 0 (QUESTION)")
            SO = 0
        if self.language == "English" and self.use_imperative and self.is_in_imperative(leftedge):
            output.append("X 0 (IMPERATIVE)")
            SO = 0
        if self.use_quote_mod and self.is_in_quotes(index):
            output.append("X 0 (QUOTES)")
            SO = 0
        if self.use_irrealis and self.has_sent_irrealis(leftedge):
            output.append("X 0 (IRREALIS)")
            SO = 0
        return [SO, output]

    def fix_all_caps_English(self):  # TODO: Fix this thing
        ### tagger tags most all uppercase words as NNP, this function tries to see if
        ### they belong in another dictionary (if so, it changes the tag)
        for i in range(0, len(self.text)):
            if len(self.text[i]) == 2:
                (word, tag) = self.text[i]
                if len(word) > 2 and word.isupper() and tag == "NNP":
                    word = word.lower()
                    if word in self.adj_dict or word in self.c_adj_dict:
                        self.text[i][1] = "JJ"
                    elif word in self.adv_dict or word in self.c_adv_dict:
                        self.text[i][1] == "RB"

                    else:
                        ex_tag = ""  # verbs need to be stemmed
                        if word[-1] == "s":
                            word = self.stem_VB(word, "Z")
                            ex_tag = "Z"
                        elif word[-3:] == "ing":
                            word = self.stem_VB(word, "G")
                            ex_tag = "G"
                        elif word[-2:] == "ed":
                            word = self.stem_VB(word, "D")
                            ex_tag = "D"
                        if word in self.verb_dict or word in self.c_verb_dict:
                            self.text[i][1] = "VB" + ex_tag
        print("fixed upper, :", self.text)

    def fix_all_caps_Spanish(self):
        ### tagger tags most all uppercase words as NP, this function tries to see if
        ### they belong in another dictionary (if so, it changes the tag)
        for i in range(0, len(self.text)):
            if len(self.text[i]) == 2:
                (word, tag) = self.text[i]
                if len(word) > 2 and word.isupper() and tag == "NP":
                    word = word.lower()
                    alt_word = self.stem_AQ(word)
                    if alt_word in self.adj_dict or word in self.c_adj_dict:
                        self.text[i][1] = "AQ"
                    else:
                        alt_word = self.stem_adv_to_adj(word)
                        if alt_word in self.adj_dict:
                            self.text[i][1] == "RG"

    def fix_all_caps(self):
        if self.language == "English":
            self.fix_all_caps_English()
        elif self.language == "Spanish":
            self.fix_all_caps_Spanish()

    def apply_weights(self, word_SO, index):
        ### this is the last step in the calculation, external self.weights and negation
        ### self.weights are applied
        if self.use_heavy_negation and word_SO < 0:  # weighing of negative SO
            word_SO *= self.neg_multiplier  # items
            print(" X " + str(self.neg_multiplier) + " (NEGATIVE)")
        word_SO *= self.weights[index]  # apply self.weights
        if self.weights[index] != 1:
            print(" X " + str(self.weights[index]) + " (WEIGHTED)")
        print(" = " + str(word_SO) + "\n")
        return word_SO

    def apply_weights_adv(self, word_SO, index, output):
        ### this is the last step in the calculation, external self.weights and negation
        ### self.weights are applied
        if self.use_heavy_negation and word_SO < 0:  # weighing of negative SO
            word_SO *= self.neg_multiplier  # items
            output += " X " + str(self.neg_multiplier) + " (NEGATIVE)"
        word_SO *= self.weights[index]  # apply self.weights
        if self.weights[index] != 1:
            output += " X " + str(self.weights[index]) + " (WEIGHTED)"
        output += (" = " + str(word_SO) + "\n")
        return [word_SO, output]

    ### SO calculators by part of speech
    ### All of these sub-calculators do more or less the same thing:
    ### Stem the word (if necessary)
    ### look for intensifiers
    ### look for negation
    ### look for negation external intensifiers (e.g. I really didn't like it)
    ### apply intensification and negation, if necessary
    ### apply other types of modifiers, including those relevant to capitalization,
    ### punctuation, blocking, repitition, etc.
    ### print the output
    ###
    ### differences that are particular to certain parts of speech are noted below

    def get_noun_SO(self, index):
        NN = self.get_word(self.text[index])
        original_NN = NN
        if NN.isupper():
            NN = NN.lower()  # if all upper case, change to lower case
        if self.get_word(self.text[index - 1]) in self.sent_punct:
            NN = NN.lower()  # change the word to lower case if sentence initial
        ntype = self.get_tag(self.text[index])[2:]
        NN = self.stem_noun(NN)
        if NN in self.c_noun_dict:
            multiword_result = self.find_multiword(index, self.c_noun_dict[NN])
        else:
            multiword_result = False
        if NN not in self.noun_dict and not multiword_result:
            return 0
        else:
            if multiword_result:
                noun_SO, backcount, forwardcount, int_modifier = multiword_result
                output = list(map(self.get_word, self.text[index - backcount:index + forwardcount + 1]))
                i = index - backcount - 1
            else:
                int_modifier = 0
                output = [original_NN]
                noun_SO = self.noun_dict[NN]
                i = index - 1
            if self.use_intensifiers:
                if self.language == "Spanish":  # look for post-nominal adj
                    intensifier = self.find_intensifier(index + 1)  # look for post-nominal adj
                    if intensifier:
                        int_modifier += intensifier[1]
                        self.text[index + 1][1] = "MOD"
                        output += [self.get_word(self.text[index + 1])]
                intensifier = self.find_intensifier(i)
                if intensifier:
                    int_modifier = intensifier[1]
                    for j in range(0, intensifier[0]):
                        self.text[i][1] = "MOD"  # block modifier being used twice
                        i -= 1
                    output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            negation = self.find_negation(i, self.noun_tag)
            if negation != -1:
                output = list(map(self.get_word, self.text[negation:i + 1])) + output
                if self.use_intensifiers:
                    int_modifier_negex = 0
                    i = negation - 1
                    if self.language == "English":
                        while self.text[i][0] in self.skipped[self.adj_tag]:
                            i -= 1
                    intensifier = self.find_intensifier(i)
                    if intensifier:
                        int_modifier_negex = intensifier[1]
                        for j in range(0, intensifier[0]):
                            self.text[i][1] = "MOD"  # block modifier being used twice
                            i -= 1
                        output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            output.append(str(noun_SO))
            if int_modifier != 0:
                noun_SO = noun_SO * (1 + int_modifier)
                output.append("X " + str(1 + int_modifier) + " (INTENSIFIED)")
            elif self.use_blocking and self.find_blocker(noun_SO, index, self.noun_tag):
                output.append("X 0 (BLOCKED)")
                noun_SO = 0
            if self.use_negation and negation != -1:
                if self.neg_negation_nullification and noun_SO < 0:
                    neg_shift = abs(noun_SO)
                elif self.self.polarity_switch_neg or (self.limit_shift and abs(noun_SO) * 2 < self.noun_neg_shift):
                    neg_shift = abs(noun_SO) * 2
                else:
                    neg_shift = self.noun_neg_shift
                if noun_SO > 0:
                    noun_SO -= neg_shift
                    output.append("- " + str(neg_shift))
                elif noun_SO < 0:
                    noun_SO += neg_shift
                    output.append("+ " + str(neg_shift))
                output.append("(NEGATED)")
                if self.use_intensifiers and int_modifier_negex != 0:
                    noun_SO *= (1 + int_modifier_negex)
                    output.append("X " + str(1 + int_modifier_negex) + " (INTENSIFIED)")
            (noun_SO, new_out) = self.apply_other_modifiers(noun_SO, index, i)
            output += new_out
            if noun_SO != 0:
                if int_modifier != 0 and self.int_multiplier != 1:
                    noun_SO *= self.int_multiplier
                    output.append("X " + str(self.int_multiplier) + " (INT_WEIGHT)")
                if NN not in self.word_counts[0]:
                    self.word_counts[0][NN] = 1
                else:
                    self.word_counts[0][NN] += 1
                    if negation == -1:
                        if self.use_word_counts_lower:
                            noun_SO /= self.word_counts[0][NN]
                            output.append("X 1/" + str(self.word_counts[0][NN]) + " (REPEATED)")
                        if self.use_word_counts_block:
                            noun_SO = 0
                            output.append("X 0 (REPEATED)")
            if self.noun_multiplier != 1:
                noun_SO *= self.noun_multiplier
                output.append("X " + str(self.noun_multiplier) + " (NOUN)")
            for word in output:
                print(word + " ")
            if noun_SO == 0:
                print("= 0\n")
            return noun_SO

    def get_verb_SO(self, index):
        ### Verbs are special because their adverbal modifiers are not necessarily
        ### adjecent to the verb; a special search is done for clause
        ### final modifiers
        VB = self.get_word(self.text[index])
        original_VB = VB
        if VB.isupper():
            VB = VB.lower()  # if all upper case, change to lower case
        if self.get_word(self.text[index - 1]) in self.sent_punct:
            VB = VB.lower()  # change the word to lower case if sentence initial
        if self.language == "English":
            vtype = self.get_tag(self.text[index])[2:]
            VB = self.stem_VB(VB, vtype)
        if VB in self.c_verb_dict:
            multiword_result = self.find_multiword(index, self.c_verb_dict[VB])
        else:
            multiword_result = False
        if VB in self.not_wanted_verb:
            return 0
        elif VB not in self.verb_dict and not multiword_result:
            return 0
        else:
            if multiword_result:
                (verb_SO, backcount, forwardcount, int_modifier) = multiword_result
                output = list(map(self.get_word, self.text[index - backcount:index + forwardcount + 1]))
                i = index - backcount - 1
            else:
                int_modifier = 0
                output = [original_VB]
                verb_SO = self.verb_dict[VB]
                i = index - 1
            if self.use_intensifiers:
                intensifier = self.find_intensifier(i)
                if intensifier:
                    int_modifier += intensifier[1]
                    for j in range(0, intensifier[0]):
                        self.text[i][1] = "MOD"  # block modifier being used twice
                        i -= 1
                    output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
                if self.use_clause_final_int:  # look for clause-final modifier
                    edge = self.find_VP_boundary(index)
                    intensifier = self.find_intensifier(edge - 1)
                    if intensifier:
                        int_modifier = intensifier[1]
                        for j in range(0, intensifier[0]):
                            self.text[edge - 1 - j][1] = "MOD"
                        output = output + list(map(self.get_word, self.text[index + 1: edge]))
            negation = self.find_negation(i, self.verb_tag)
            if negation != -1:
                output = list(map(self.get_word, self.text[negation:i + 1])) + output
                if self.use_intensifiers:
                    int_modifier_negex = 0
                    i = negation - 1
                    if self.language == "English":
                        while self.text[i][0] in self.skipped["JJ"]:
                            i -= 1
                    intensifier = self.find_intensifier(i)
                    if intensifier:
                        int_modifier_negex = intensifier[1]
                        for j in range(0, intensifier[0]):
                            self.text[i][1] = "MOD"  # block modifier being used twice
                            i -= 1
                        output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            output.append(str(verb_SO))
            if int_modifier != 0:
                verb_SO = verb_SO * (1 + int_modifier)
                output.append("X " + str(1 + int_modifier) + " (INTENSIFIED)")
            elif self.use_blocking and self.find_blocker(verb_SO, index, self.verb_tag):
                output.append("X 0 (BLOCKED)")
                verb_SO = 0
            if self.use_negation and negation != -1:
                if self.neg_negation_nullification and verb_SO < 0:
                    neg_shift = abs(verb_SO)
                elif self.polarity_switch_neg or (self.limit_shift and abs(verb_SO) * 2 < self.verb_neg_shift):
                    neg_shift = abs(verb_SO) * 2
                else:
                    neg_shift = self.verb_neg_shift
                if verb_SO > 0:
                    verb_SO -= neg_shift
                    output.append("- " + str(neg_shift))
                elif verb_SO < 0:
                    verb_SO += neg_shift
                    output.append("+ " + str(neg_shift))
                output.append("(NEGATED)")
                if self.use_intensifiers and int_modifier_negex != 0:
                    verb_SO *= (1 + int_modifier_negex)
                    output.append("X " + str(1 + int_modifier_negex) + " (INTENSIFIED)")
            (verb_SO, new_out) = self.apply_other_modifiers(verb_SO, index, i)
            output += new_out
            if verb_SO != 0:
                if int_modifier != 0 and self.int_multiplier != 1:
                    verb_SO *= self.int_multiplier
                    output.append("X " + str(self.int_multiplier) + " (INT_WEIGHT)")
                if VB not in self.word_counts[1]:
                    self.word_counts[1][VB] = 1
                else:
                    self.word_counts[1][VB] += 1
                    if negation == -1:
                        if self.use_word_counts_lower:
                            verb_SO /= self.word_counts[1][VB]
                            output.append("X 1/" + str(self.word_counts[1][VB]) + " (REPEATED)")
                        if self.use_word_counts_block:
                            verb_SO = 0
                            output.append("X 0 (REPEATED)")
            if self.verb_multiplier != 1:
                verb_SO *= self.verb_multiplier
                output.append("X " + str(self.verb_multiplier) + " (VERB)")
            for word in output:
                print(word + " ")
            if verb_SO == 0:
                print("= 0\n")  # calculation is over
            return verb_SO

    def get_adj_SO(self, index):
        ### Comparative and superlative adjectives require special stemming, and are
        ### treated as if they have been intensified with "more" or "most". Non-
        ### predicative uses of this kind of adjective are often not intended to
        ### express sentiment, and are therefore ignored. Adjectives often have
        ### more than one intensifier (e.g. really very good) so the search for
        ### intensifiers is iterative.
        JJ = self.get_word(self.text[index])
        original_JJ = JJ
        int_modifier = 0
        if JJ.isupper():
            JJ = JJ.lower()  # if all upper case, change to lower case
        if self.get_word(self.text[index - 1]) in self.sent_punct:
            JJ = JJ.lower()  # change the word to lower case if sentence initial
        if self.language == "English":
            adjtype = self.get_tag(self.text[index])[2:]
            if not self.use_comparatives and (
                            adjtype == "R" or self.get_word(self.text[index - 1]) in self.comparatives):
                return 0
            if not self.use_superlatives and (
                                adjtype == "S" or self.get_word(self.text[index - 1]) in self.superlatives or JJ in [
                        "best",
                        "worst"]):
                return 0
            if adjtype == "R" and JJ not in self.adj_dict and JJ not in self.not_wanted_adj:
                JJ = self.stem_comp_JJ(JJ)
                if self.use_intensifiers:
                    int_modifier += self.int_dict["more"]
            elif adjtype == "S" and JJ not in self.adj_dict and JJ not in self.not_wanted_adj:
                JJ = self.stem_super_adj(JJ)
                if self.use_intensifiers:
                    int_modifier += 1
        elif self.language == "Spanish":
            JJ = self.stem_AQ(JJ)
            if not self.use_comparatives and (self.get_word(self.text[index - 1]) in self.comparatives):
                return 0
            if not self.use_superlatives and ((self.get_word(
                    self.text[index - 1]) in self.comparatives and self.get_tag(self.text[index - 2]) == "DA") or (
                            AQ in ["mejor", "p" + chr(233) + "simo"] and self.get_tag(self.text[index - 2]) == "DA")):
                return 0
            if JJ not in self.adj_dict and JJ not in self.not_wanted_adj:
                new_JJ = self.stem_super_adj(JJ)
                if self.use_intensifiers and self.use_superlatives and new_JJ != JJ:
                    JJ = new_JJ
                    int_modifier += 1
        if JJ in self.c_adj_dict:
            multiword_result = self.find_multiword(index, self.c_adj_dict[JJ])
        else:
            multiword_result = False
        if JJ in self.not_wanted_adj:
            return 0
        elif self.language == "English" and (
                        (adjtype == "S" or self.get_word(self.text[index - 1]) in self.superlatives) and (
                                not self.words_within_num(index, self.definites, 2) or not self.is_in_predicate(
                                index)) or (
                            (adjtype == "R" or self.get_word(
                                self.text[index - 1]) in self.comparatives) and not self.is_in_predicate(
                            index))):
            return 0  # superlatives must be preceded by a definite and be in the predicate         # self.comparatives must be in the predicate
        elif JJ not in self.adj_dict and not multiword_result:
            return 0
        else:
            if multiword_result:
                (adj_SO, backcount, forwardcount, int_modifier) = multiword_result
                output = list(map(self.get_word, self.text[index - backcount:index + forwardcount + 1]))
                i = index - backcount - 1
            else:
                output = [original_JJ]
                adj_SO = self.adj_dict[JJ]
                i = index - 1
            if (self.language == "English" and self.get_tag(self.text[i]) == "DET" or self.get_word(
                    self.text[i]) == "as") or (
                                    self.language == "Spanish" and self.get_tag(self.text[i]) == "DA" or self.get_tag(
                            self.text[i]) == "DI" or self.get_word(
                        self.text[i]) == "tan"):  # look past determiners and "as" for intensification
                i -= 1
            if self.use_intensifiers:
                intensifier = 1
                while intensifier:  # keep looking for instensifiers until no more
                    intensifier = self.find_intensifier(i)  # are found
                    if intensifier:
                        int_modifier += intensifier[1]
                        for j in range(0, intensifier[0]):
                            self.text[i][1] = "MOD"  # block modifier being used twice
                            i -= 1
                        output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            negation = self.find_negation(i, self.adj_tag)
            if negation != -1:
                output = list(map(self.get_word, self.text[negation:i + 1])) + output
                if self.use_intensifiers:
                    int_modifier_negex = 0
                    i = negation - 1
                    if self.language == "English":
                        while self.text[i][0] in self.skipped["JJ"]:
                            i -= 1
                    intensifier = self.find_intensifier(i)
                    if intensifier:
                        int_modifier_negex = intensifier[1]
                        for j in range(0, intensifier[0]):
                            self.text[i][1] = "MOD"  # block modifier being used twice
                            i -= 1
                        output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            output.append(str(adj_SO))
            if int_modifier != 0:
                adj_SO = adj_SO * (1 + int_modifier)
                output.append("X " + str(1 + int_modifier) + " (INTENSIFIED)")
                if ((self.language == "English" and adjtype == "R") or self.get_word(
                        self.text[index - 1]) in self.comparatives):
                    output.append("(COMPARATIVE)")
                if (self.language == "English" and (
                                adjtype == "S" or self.get_word(self.text[index - 1]) in self.superlatives)):
                    output.append("(SUPERLATIVE)")
                elif (self.language == "Spanish" and (
                                self.get_word(self.text[index - 1]) in self.comparatives and self.get_tag(
                            self.text[index - 2]) == "DA") or (
                                JJ in ["mejor", "p" + chr(233) + "simo"] and self.get_tag(
                            self.text[index - 2]) == "DA")):
                    output.append("(SUPERLATIVE)")
            elif self.use_blocking and self.find_blocker(adj_SO, index, self.adj_tag):
                output.append("X 0 (BLOCKED)")
                adj_SO = 0
            if self.use_negation and negation != -1:
                if self.neg_negation_nullification and adj_SO < 0:
                    neg_shift = abs(adj_SO)
                elif self.polarity_switch_neg or (self.limit_shift and abs(adj_SO) * 2 < self.adj_neg_shift):
                    neg_shift = abs(adj_SO) * 2
                else:
                    neg_shift = self.adj_neg_shift
                if adj_SO > 0:
                    adj_SO -= neg_shift
                    output.append("- " + str(neg_shift))
                elif adj_SO < 0:
                    adj_SO += neg_shift
                    output.append("+ " + str(neg_shift))
                output.append("(NEGATED)")
                if self.use_intensifiers and int_modifier_negex != 0:
                    adj_SO *= (1 + int_modifier_negex)
                    output.append("X " + str(1 + int_modifier_negex) + " (INTENSIFIED)")
            (adj_SO, new_out) = self.apply_other_modifiers(adj_SO, index, i)
            output += new_out
            if int_modifier != 0 and self.int_multiplier != 1:
                adj_SO *= self.int_multiplier
                output.append("X " + str(self.int_multiplier) + " (INT_WEIGHT)")
            if JJ not in self.word_counts[2]:
                self.word_counts[2][JJ] = 1
            else:
                self.word_counts[2][JJ] += 1
                if negation == -1:
                    if self.use_word_counts_lower:
                        adj_SO /= self.word_counts[2][JJ]
                        output.append("X 1/" + str(self.word_counts[2][JJ]) + " (REPEATED)")
                    if self.use_word_counts_block:
                        adj_SO = 0
                        output.append("X 0 (REPEATED)")
            if self.adj_multiplier != 1:
                adj_SO *= self.adj_multiplier
                output.append("X " + str(self.adj_multiplier) + " (ADJECTIVE)")
            for word in output:
                print(word + " ")
            if adj_SO == 0:
                print("= 0\n")  # calculation is over
            return adj_SO

    def get_adv_SO(self, index):
        ### There are two special things to note about dealing with adverbs: one is that
        ### their SO value can be derived automatically from the lemma in the
        ### adjective dictionary. The other is the special handling of "too", which
        ### is counted only when it does not appear next to punctuation (which rules out
        ### most cases of "too" in the sense of "also")
        RB = self.get_word(self.text[index])
        original_RB = RB
        if RB.isupper():
            RB = RB.lower()  # if all upper case, change to lower case
        if self.get_word(self.text[index - 1]) in self.sent_punct:
            RB = RB.lower()  # change the word to lower case if sentence initial
        if self.adv_learning and RB not in self.adv_dict and RB not in self.not_wanted_adv:
            JJ = self.stem_adv_to_adj(RB)  # stem the adverb to its corresponding adj
            if JJ in self.adj_dict:
                self.adv_dict[RB] = self.adj_dict[JJ]  # take its SO value
                self.new_adv_dict[RB] = self.adj_dict[JJ]
        if RB in self.c_adv_dict:
            multiword_result = self.find_multiword(index, self.c_adv_dict[RB])
        else:
            multiword_result = False
        if RB in self.not_wanted_adv or (self.language == "English" and (
                            RB == "too" and index < len(self.text) - 1 and self.get_word(
                    self.text[index + 1]) in self.punct) or (
                            RB == "well" and index < len(self.text) - 1 and self.get_word(
                    self.text[index + 1]) == ",")):
            return [0, ""]  # do not count too next to punctuation
        elif RB not in self.adv_dict and not multiword_result:
            return [0, ""]
        else:
            if multiword_result:
                (adv_SO, backcount, forwardcount, int_modifier) = multiword_result
                output = list(map(self.get_word, self.text[index - backcount:index + forwardcount + 1]))
                i = index - backcount - 1
            else:
                int_modifier = 0
                output = [original_RB]
                adv_SO = self.adv_dict[RB]
                i = index - 1
            if (self.language == "English" and self.get_word(self.text[i]) == "as") or (
                            self.language == "Spanish" and self.get_word(
                        self.text[i]) == "tan"):  # look past "as" for intensification
                i -= 1
            if self.use_intensifiers:
                intensifier = self.find_intensifier(i)
                if intensifier:
                    int_modifier += intensifier[1]
                    for j in range(0, intensifier[0]):
                        self.text[i][1] = "MOD"  # block modifier being used twice
                        i -= 1
                    output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            negation = self.find_negation(i, self.adv_tag)
            if negation != -1:
                output = list(map(self.get_word, self.text[negation:i + 1])) + output
                if self.use_intensifiers:
                    int_modifier_negex = 0
                    i = negation - 1
                    if self.language == "English":
                        while self.text[i][0] in self.skipped["JJ"]:
                            i -= 1
                    intensifier = self.find_intensifier(i)
                    if intensifier:
                        int_modifier_negex = intensifier[1]
                        for j in range(0, intensifier[0]):
                            self.text[i][1] = "MOD"  # block modifier being used twice
                            i -= 1
                        output = list(map(self.get_word, self.text[i + 1:i + intensifier[0] + 1])) + output
            output.append(str(adv_SO))
            if int_modifier != 0:
                adv_SO = adv_SO * (1 + int_modifier)
                output.append("X " + str(1 + int_modifier) + " (INTENSIFIED)")
            elif self.use_blocking and self.find_blocker(adv_SO, index, self.adv_tag):
                output.append("X 0 (BLOCKED)")
                adv_SO = 0
            if self.use_negation and negation != -1:
                if self.neg_negation_nullification and adv_SO < 0:
                    neg_shift = abs(adv_SO)
                elif self.polarity_switch_neg or (self.limit_shift and abs(adv_SO) * 2 < self.adv_neg_shift):
                    neg_shift = abs(adv_SO) * 2
                else:
                    neg_shift = self.adv_neg_shift
                if adv_SO > 0:
                    adv_SO -= neg_shift
                    output.append("- " + str(neg_shift))
                elif adv_SO < 0:
                    adv_SO += neg_shift
                    output.append("+ " + str(neg_shift))
                output.append("(NEGATED)")
                if self.use_intensifiers and int_modifier_negex != 0:
                    adv_SO *= (1 + int_modifier_negex)
                    output.append("X " + str(1 + int_modifier_negex) + " (INTENSIFIED)")
            (adv_SO, new_out) = self.apply_other_modifiers(adv_SO, index, i)
            output += new_out
            if adv_SO != 0:
                if int_modifier != 0 and self.int_multiplier != 1:
                    adv_SO *= self.int_multiplier
                    output.append("X " + str(self.int_multiplier) + " (INT_WEIGHT)")
                if RB not in self.word_counts[3]:
                    self.word_counts[3][RB] = 1
                else:
                    self.word_counts[3][RB] += 1
                    if negation == -1:
                        if self.use_word_counts_lower:
                            adv_SO /= self.word_counts[3][RB]
                            output.append("X 1/" + str(self.word_counts[3][RB]) + " (REPEATED)")
                        if self.use_word_counts_block:
                            adv_SO = 0
                            output.append("X 0 (REPEATED)")
            if self.adv_multiplier != 1:
                adv_SO *= self.adv_multiplier
                output.append("X " + str(self.adv_multiplier) + " (ADVERB)")
            full_output = ""
            for word in output:
                full_output += word + " "
            if adv_SO == 0:
                full_output += "= 0\n"  # calculation is over
            return [adv_SO, full_output]

    ### Main script ###
    ### Note that there are 4 (or even 5) iterations through the self.text. The
    ### rationale for iterating separately for each part of speech (and the
    ### ordering of those iterations) is that adverbs and adjectives which are used
    ### as intensifiers of nouns, verbs, or adjectives need to be marked so they
    ### are not counted twice.
    def get_output(self, input):
        ### self.text ###

        # self.text = [] # the self.text is a list of word, tag lists
        # self.weights = [] # self.weights should be the same length as the self.text, one for each token
        # self.word_counts = [{},{},{},{}] # keeps track of number of times each word lemma appears in the self.text
        # self.text_SO = 0 # a sum of the SO value of all the words in the self.text
        # self.SO_counter = 0 # a count of the number of SO carrying terms
        # self.boundaries = [] # the location of newline self.boundaries from the input
        print("Initial text:", self.text)
        self.fill_text_and_weights(input)
        '''if output_sentences:
            sentence_SO = {}'''

        adv_count = len(self.adv_dict)  # for determining if there are new adverbs
        # TODO: Add repeating the input
        print("######\n---------\n\n---------\nText Length: " + str(len(self.text)) + "\n---------\n")

        if self.fix_cap_tags:
            self.fix_all_caps()

        print("Now text, ", self.text)

        if self.use_nouns:
            nouns_SO = 0
            print("Nouns:\n-----\n")
            for index in range(0, len(self.text)):
                if len(self.text[index]) == 2:
                    word, tag = self.text[index]
                    if tag[:2] == self.noun_tag:
                        word_SO = self.get_noun_SO(index)
                        if word_SO != 0:
                            word_SO = self.apply_weights(word_SO, index)
                            nouns_SO += word_SO
                        '''if output_sentences:
                            sentence_no = get_sentence_no(index)
                            if sentence_no not in sentence_SO:
                                sentence_SO[sentence_no] = word_SO
                            else:
                                sentence_SO[sentence_no] += word_SO'''
            noun_count = self.sum_word_counts(self.word_counts[0])
            if noun_count > 0:
                print("-----\nAverage SO: " + str(nouns_SO / noun_count) + "\n-----\n")
                self.text_SO += nouns_SO
                self.SO_counter += noun_count
            else:
                print("-----\nAverage SO:\n-----\n", nouns_SO)

        if self.use_verbs:
            print("Verbs:\n-----\n")
            verbs_SO = 0
            for index in range(0, len(self.text)):
                if len(self.text[index]) == 2:
                    (word, tag) = self.text[index]
                    if tag[:2] == self.verb_tag:
                        word_SO = self.get_verb_SO(index)
                        if word_SO != 0:
                            word_SO = self.apply_weights(word_SO, index)
                            verbs_SO += word_SO
                        '''if output_sentences:
                            sentence_no = get_sentence_no(index)
                            if sentence_no not in sentence_SO:
                                sentence_SO[sentence_no] = word_SO
                            else:
                                sentence_SO[sentence_no] += word_SO'''
            verb_count = self.sum_word_counts(self.word_counts[1])
            if verb_count > 0:
                print("-----\nAverage SO: " + str(verbs_SO / verb_count) + "\n-----\n")
                self.text_SO += verbs_SO
                self.SO_counter += verb_count
            else:
                print("-----\nAverage SO: 0\n-----\n")

        if self.use_adjectives:
            adjs_SO = 0
            print("Adjectives:\n-----\n")
            for index in range(0, len(self.text)):
                if len(self.text[index]) == 2:
                    (word, tag) = self.text[index]
                    if tag[:2] == self.adj_tag:
                        print('adjective:', word)
                        word_SO = self.get_adj_SO(index)
                        if word_SO != 0:
                            word_SO = self.apply_weights(word_SO, index)
                            adjs_SO += word_SO
                        '''if output_sentences:
                            sentence_no = get_sentence_no(index)
                            if sentence_no not in sentence_SO:
                                sentence_SO[sentence_no] = word_SO
                            else:
                                sentence_SO[sentence_no] += word_SO'''
            adj_count = self.sum_word_counts(self.word_counts[2])
            if adj_count > 0:
                print("-----\nAverage SO: " + str(adjs_SO / adj_count) + "\n-----\n")
                self.text_SO += adjs_SO
                self.SO_counter += adj_count
            else:
                print("-----\nAverage SO: 0\n-----\n")

        adv_outputs = []
        if self.use_adverbs:
            advs_SO = 0
            print("Adverbs:\n-----\n")
            for index in range(len(self.text) - 1, -1, -1):  # backwards iteration, since
                if len(self.text[index]) == 2:
                    (word, tag) = self.text[index]  # adverbs modify adverbs
                    if tag[:2] == self.adv_tag:
                        (word_SO, output) = self.get_adv_SO(index)
                        if word_SO != 0:
                            (word_SO, output) = self.apply_weights_adv(word_SO, index, output)
                            advs_SO += word_SO
                            adv_outputs.insert(0, output)
                        '''if output_sentences:
                            sentence_no = get_sentence_no(index)
                            if sentence_no not in sentence_SO:
                                sentence_SO[sentence_no] = word_SO
                            else:
                                sentence_SO[sentence_no] += word_SO'''
                adv_count = self.sum_word_counts(self.word_counts[3])
            for output in adv_outputs:
                print(output)
            if adv_count > 0:
                print("-----\nAverage SO: " + str(advs_SO / adv_count) + "\n-----\n")
                self.text_SO += advs_SO
                self.SO_counter += adv_count
            else:
                print("-----\nAverage SO: 0\n-----\n")

        if self.SO_counter > 0:
            self.text_SO = self.text_SO / self.SO_counter  # calculate the final SO for the self.text

        print("Text SO:\t" + str(self.text_SO) + "\n")
        '''
        if output_sentences:
            print("-----\nSO by Sentence\n-----\n")
            for i in range(len(self.boundaries)):
                print(self.get_sentence(self.boundaries[i] -1) + " ")
                if i in sentence_SO:
                    print(str(sentence_SO[i]) + "\n")
                else:
                    print("0\n")'''
        print("---------\nTotal SO: " + str(self.text_SO) + "\n---------\n")

        if self.adv_learning and self.new_adv_dict:  # output the new adverb
            f = open(self.adv_dict_path, "a")  # dictionary
            for adverb in self.new_adv_dict:
                f.write(adverb + "\t" + str(int(self.adv_dict[adverb])) + "\n")
            f.close()

        return self.text_SO
