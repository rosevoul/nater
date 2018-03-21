import re

class WordPreprocessor(object):
	"""Preprocess text word-wise"""

	REPLACEMENT_PATTERNS = [
		# Contractions
	    (r'won\'t', 'will not'),
	    (r'can\'t', 'cannot'),
	    (r'i\'m', 'i am'),
	    (r'ain\'t', 'is not'),
	    (r'(\w+)\'ll', '\g<1> will'),
	    (r'(\w+)n\'t', '\g<1> not'),
	    (r'(\w+)\'ve', '\g<1> have'),
	    (r'(\w+)\'s', '\g<1> is'),
	    (r'(\w+)\'re', '\g<1> are'),
	    (r'(\w+)\'d', '\g<1> would'),
	    # Symbols
	    (r'&', ' and '),
	    # Words
	    (r'SCOS-2000', 'SCOS'),
	    (r'SCOS 2000', 'SCOS')	    
	]

	def __init__(self, entities, aliases, split_by_sentence=False):
		self.entities = entities
		self.aliases = aliases
		self.split_by = split_by

		self.split_data_words = []

        self.patterns = [(re.compile(regex), repl)
                         for (regex, repl) in REPLACEMENT_PATTERNS]

	def split(self, data):
		# Convert 'nan' to "" (empty string)
		split_data = [text for text in data if text != 'nan']

		# Split by sentence or paragraph
		if self.split_by_sentence:
			split_data_sent = []
			for text in split_data:
				split_data_sent.extend(sent_tokenize(text))
			split_data = split_data_sent

		split_data = [self.replace_regex(text) for text in split_data]

		self.split_data_words = [word_tokenize(text) for text in split_data]

	def preprocess(self, data):
		# Strip the numbers
		# Lowercase
		# Replace '\n' with " " (whitespace)
		# Remove all the punctuation
		self.split(text)
		preprocessed_data = []
		for words in self.split_data_words:
			clean_words = [w for w in words if not w.isnumeric()]
			clean_words = [w.lower() for w in clean_words]
			clean_words = [w.replace('\n', ' ') for w in clean_words]
			clean_words = [w for w in clean_words if w not in string.punctuation]
			preprocessed_data.append(clean_words)

		# Remove empty lists
		preprocessed_data = [lst for lst in preprocessed_data if lst != []]

		return preprocessed_data

    def replace_regex(self, string):
        new_string = string
        for (pattern, repl) in self.patterns:
            new_string = re.sub(pattern, repl, new_string)

        return new_string
