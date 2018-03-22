"""Spelling corrector customizing the Enchant library

    TODO: Override suggest() method in order to give high priority in the custom dictionary
"""

import enchant
from nltk.metrics import edit_distance

class SpellCorrector(object):
	"""Automatically replace misspelled words based on the domain specific dictionary """
	"""Spelling corrector using the Enchant library
	
	Attributes:
	    max_dist (int): Refers to maximum editing distance of the checked word to the correction word
	    lexicon (list): Dictionary of words
	"""
	def __init__(self, lexicon, max_dist=2):
		"""Constructor
		
		Args:
		    max_dist (int, optional): Preferred maximum editing distance
		    lexicon (list): Custom dictionary of words in a txt file
		"""
		self.lexicon = enchant.DictWithPWL('en_GB', lexicon)
		self.max_dist = max_dist

	def correct(self, text):
		corrected_text = [self.correct_word(word) for sentence in text for word in sentence]

		return corrected_text

	def correct_word(self, word):
	    """Search if the given word exists in the dictionary. If the word is not found, replace it with the first word
	    found that is less than the maximum edits away.
	    
	    Args:
	        word (str): The checked word
	    
	    Returns:
	        word: The corrected word
	    """
	    if self.lexicon.check(word):
	        return word

	    suggestions = self.lexicon.suggest(word)

	    if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
	        return suggestions[0]
	    else:
	        return 'None'
