#
# nGram: basic object holding a dictionary mapping
# { [n words]: { [nextword]: [count of nextword following n words in corpus],
# ... } , ... }
# Can be used with nGramReader to load objects into a database with sqlalchemy.
#
# Boyang Niu
# boyang.niu@gmail.com
# 11-13-2013
#


class nGram(object):

    def __init__(self, prev_words, next_word, count, size):
        self.prev_words = prev_words
        self.next_word = next_word
        self.count = count
        self.size = size

    def __repr__(self):
        return "<nGram('%s', '%s', '%s')>" % (self.prev_words,
                                              self.next_word, self.size)
