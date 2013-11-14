Babbler
=======
A simple n-gram babbler that spits out probabilitic word choices when given a corpus to prime itself on and an integer denoting the number of words to guess on.
---------------------------------------------------------------------------------------

To use, create an ngram Babbler by feeding it a file and an integer:

  b = Babbler("test.txt", 2)

Then successively call generate_next_word([list of words]) with the 
words that the Babbler is generating:

  word_list = []
  while [condition]:
       word_list.append(b.generate_next_word(word_list))
  return " ".join(word_list)
