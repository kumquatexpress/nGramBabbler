# Babbler: reads in a corpus and uses conditional probabilities to
# write out a string of words, with each word generated based off of
# the probability that it occurred after the previous n words in the corpus.
#
# Boyang Niu
# boyang.niu@gmail.com
# 11-13-2013
#
#

import random
import collections


class Babbler(object):

    def __init__(self, filename, ngram_count):
        """
        Populates the dictionary of word counts that make up the babbler
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
        self.phrase_counts, self.phrase_sum = self.generate_list_for_rng(
            phrase_counts)

    def get_frequencies(self, words):
        """
        Given a list of words, gives back a list of tuples of
        (float frequencies, string word) that dictate the probabilities
        of the next word.
        """
        if words not in self.word_table:
            return []
        return {word2: (float(self.word_table[words][word2]) /
                        sum(self.word_table[words].values()))
                for word2 in self.word_table[words]}

    def generate_next_word(self, words):
        """
        Given the words that have already occurred, generate the next word.
        """
        # truncate the word list to the given number of ngrams of this babbler
        trunc_words = " ".join(" ".join(words).split(" ")[-1 *
                                                          self.ngram_size:])
        # if we encounter a string that we haven't ever seen, generate random
        if trunc_words not in self.word_table:
            return self.generate_random_word()
        # generate the number that we use to pick the next word
        rng_table, rng_sum = self.generate_list_for_rng(
            self.get_frequencies(trunc_words))
        rng_num = random.random() * rng_sum
        for freq, word in rng_table:
            if rng_num > freq:
                continue
            else:
                return word

    def generate_random_word(self):
        # partial dict for holding values temporarily
        rng_num = random.random() * self.phrase_sum
        for freq, word in self.phrase_counts:
            if rng_num > freq:
                continue
            else:
                return word

    def generate_list_for_rng(self, rng_dict):
        """
        Takes a dictionary from word to word count and returns
        a tuple (a list of tuples from word frequency to word, sum of
        frequencies)
        """
        # rng_table is a list of tuples (freq, word) of probabilities
        rng_table = []
        rng_sum = 0
        for v in rng_dict:
            rng_sum += rng_dict[v]
            rng_table.append((rng_sum, v))
        return rng_table, rng_sum
