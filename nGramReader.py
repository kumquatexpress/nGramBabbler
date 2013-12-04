# nGramReader: reads in text files and finds the conditional probabilities of
# words occurring after a string of previous [n] given words, then loads
# this information into a sqlite3 database in the form of nGram objects
# for an nGramWriter to use.
#
#
# Boyang Niu
# boyang.niu@gmail.com
# 11-13-2013
#

import collections
import nGram as ng
import dbConnector as db


class nGramReader(object):

    def __init__(self, filename, ngram_count):
        """
        Populates the dictionary of word counts that make up the reader
        with counts based on [ngram_count] previous words when given a
        [filename] file that acts as a corpus.
        """

        word_table = {}
        phrase_counts = {}
        totalwords = 0
        # deque automatically evicts the first entry when over maxlen
        tempwords = collections.deque(maxlen=ngram_count)

        with open(filename) as f:
            for line in f:
                for word in line.strip().split(" "):
                    word = word.lower()
                    # if this is the first word in the corpus
                    if not len(tempwords) == ngram_count:
                        tempwords.append(word)
                        continue
                    # otherwise we use the previous words to generate the next
                    tempword = " ".join(tempwords)
                    if tempword not in word_table:
                        word_table[tempword] = {}
                        phrase_counts[tempword] = 1
                    else:
                        phrase_counts[tempword] += 1
                    # add counts to the word table
                    if word not in word_table[tempword]:
                        word_table[tempword][word] = 1
                    else:
                        word_table[tempword][word] += 1
                    # add the current word to the previous words and evict one
                    tempwords.append(word)
                    # add to the total count of words
                    totalwords += 1

        self.total_words = totalwords
        self.word_table = word_table
        self.ngram_size = ngram_count
        self.Session = db.get_session()

    def make_db_transactions(self):
        """
        Creates nGram objects and loads them into the database.
        """
        session = self.Session()
        for phrase in self.word_table:
            for word in self.word_table[phrase]:
                count = self.word_table[phrase][word]
                ngram = ng.nGram(phrase, word, count, self.ngram_size)
                session.add(ngram)
        session.commit()
