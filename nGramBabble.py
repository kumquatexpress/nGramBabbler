#!/usr/bin/python
#
# This is the main function for the Babbler class, using a Babbler,
# it takes in the ngram number of choice and a filename and outputs
# 500 words of babble.  Given command line arguments
#
# $python nGramBabble.py [number] [filename] [length]
#

import Babbler as Babble
import sys


def main():
    arguments = sys.argv
    if len(arguments) < 4:
        print("Usage: python nGramBabble.py [number] [filename] [length]")
        return 0
    ngrams = int(arguments[1])
    filename = arguments[2]
    length = int(arguments[3])
    b = Babble.Babbler(filename, ngrams)
    babble = []
    while True:
        if len(babble) > length:
            if babble[-1][-1] == ".":
                break
        babble.append(b.generate_next_word(babble))
    print(" ".join(babble))

if __name__ == '__main__':
    main()
