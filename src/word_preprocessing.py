class WordPreprocessor(object):
	"""Preprocess text word-wise"""
	def __init__(self, entities, acronyms, split_by):
		self.entities = entities
		self.acronyms = acronyms
		self.split_by = split_by

	def preprocess(self, text):
		pass
		