from collections import Counter
from operator import itemgetter

class LexiconCreator(object):
	"""Create a lexicon using a custom corpus."""
	
	@classmethod	
	def create(cls, file_path, base_corpus):
		flat_base_corpus = [word for sublist in base_corpus for word in sublist]
		frequencies = Counter(flat_base_corpus)
		
		sorted_words = sorted(frequencies.items(), reverse=True, key=itemgetter(1))
		sorted_words = [w[0] for w in sorted_words]
		
		cls.write_to_file(file_path, sorted_words)

	# TODO store "lexicon.txt" in appropriate location	
	@staticmethod
	def write_to_file(file_path, words):
	    with open (file_path, "w") as f:
	        for w in words:
	        	f.write('{0}\n'.format(w))
