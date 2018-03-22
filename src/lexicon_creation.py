from collections import Counter
from operator import itemgetter

class LexiconCreator(object):
	"""Create a lexicon using a custom corpus."""
	
	@classmethod	
	def create(cls, base_corpus):
		frequencies = Counter(base_corpus)
		
		sorted_words = sorted(frequencies.items(), reverse=True, key=itemgetter(1))
		sorted_words = [w[0] for w in sorted_words]
		
		cls.write_to_file(sorted_words)

	# TODO store "lexicon.txt" in appropriate location	
	@staticmethod
	def write_to_file(words, filename="lexicon.txt"):
	    with open (filename, "w") as f:
	        for w in words:
	            f.write("%s\n" % w)    
