class nGram(object):

    def __init__(self, prev_words, next_word, count, size):
        self.prev_words = prev_words
        self.next_word = next_word
        self.count = count
        self.size = size

    def __repr__(self):
        return "<nGram('%s', '%s', '%s')>" % (self.prev_words,
                                              self.next_word, self.size)
