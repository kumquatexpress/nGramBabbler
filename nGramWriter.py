#!/usr/bin/python
#
# nGramWriter: uses a database of nGrams to print a babbled length of text
# starting from a given word.
#
# Boyang Niu
# boyang.niu@gmail.com
# 11-22-2013
#

import dbConnector as db
import nGram as ng
import random


class nGramWriter(object):

    def __init__(self, length, dbfile="ngrams.db"):
        """
        Initializes a new nGramPrinter, with a dbfile set by
        default to "ngrams.db"
        """
        Session = db.get_session(dbfile)

        self.session = Session()
        self.length = length
        self.ngrams = self.find_nGrams_by_length(length)

    def find_nGrams_by_length(self, length, count="all"):
        if count != "all":
            return self.session.query(ng.nGram).filter(
                ng.nGram.size == length).limit(count).all()
        return self.session.query(ng.nGram).filter(ng.nGram.size == length).all()

    def find_random_start(self):
        return random.choice([n.prev_words for n in self.ngrams])

    def get_next_word(self, prev_words):
        """
        Prev_words comes in as a list of two seperate tokens and needs to be
        made into a word again in order to search the database.
        This function returns the next word probabilistically.
        """
        total = 0
        frequencies = []
        prev_words = " ".join(prev_words)

        temp_dict = filter(lambda x: x.prev_words == prev_words, self.ngrams)
        for n in temp_dict:
            total += n.count
            frequencies.append((n.next_word, total))
        frequencies.sort(key=lambda x: x[1])

        selection = random.randint(0, total)
        for k, v in frequencies:
            if selection <= v:
                return k

    def print_sentence(self, length=20, start_word=None):
        """
        Repeatedly calls get_next_word on the last n words of the sentence, n
        being the length of nGrams of this writer.
        """
        if start_word is None:
            start_word = self.find_random_start()

        sentence = start_word.split(" ")
        start_word = sentence[-self.length:]

        while len(sentence) < length:
            sentence.append(self.get_next_word(start_word))
            start_word = sentence[-self.length:]
        return " ".join(sentence)
