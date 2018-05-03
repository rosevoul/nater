import re
import string
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

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
        (r'\n', ' '),
        (r'-', ''),
        (r'>', ' select '),
        (r'=', ' = '),    
        # Case specific
        (r'SCOS-2000', 's2k'),
        (r'scos-2000', 's2k'),
        (r'SCOS 2000', 's2k'),
        (r'scos 2000', 's2k'),
        (r'milli seconds', 'milliseconds')
    ]

    def __init__(self, entities, aliases, split_by_sentence=False):
        self.entities = entities
        self.aliases = aliases
        self.split_by_sentence = split_by_sentence

        self.split_data_words = []

        self.patterns = [(re.compile(regex), repl)
                         for (regex, repl) in self.REPLACEMENT_PATTERNS]

    def split(self, data):
        # Convert 'nan' to "" (empty string)
        split_data = [text for text in data if text != 'nan']
        # Split by sentence or paragraph
        if self.split_by_sentence:
            split_data_sent = []
            for text in split_data:
                split_data_sent.extend(sent_tokenize(text))
            split_data = split_data_sent
        # Apply regex filter
        regex_filter_data = [self.replace_regex(text) for text in split_data]
        
        self.split_data_words = [word_tokenize(text) for text in regex_filter_data]

    def preprocess(self, data, use_stem=True):
        # Split to sentences and apply regex filter 
        # Strip the numbers
        # Lowercase
        # Remove stopwords
        # Remove all the punctuation
        # Replace spacecraft parameters with sparam
        # Remove words that contain numbers or/and punctuation
        # Stem
        
        stop_words = set(stopwords.words('english'))
        invalid_symbols = set(string.punctuation.replace("_", ""))
        stemmer = PorterStemmer()
        parameters, applications, systems = self.entities
        parameters = [w.lower() for w in parameters]
        applications = [w.lower() for w in applications]
        systems = [w.lower() for w in systems]
        domain_specific_words = set(['sparam', 'eud4s2k', 's2k', 'sles12'] + applications + systems)

        self.split(data)
        preprocessed_data = []
        filtered_words = []
        for words in self.split_data_words:
            filtered_words = (w for w in words if not w.isnumeric())
            filtered_words = (w.lower() for w in filtered_words)
            filtered_words = (w for w in filtered_words if not w in stop_words)
            filtered_words = (w for w in filtered_words if w not in string.punctuation)
            filtered_words = ('sparam' if w in parameters else w for w in filtered_words)
            filtered_words = (w for w in filtered_words if w in domain_specific_words or not any(c.isdigit() or c in invalid_symbols for c in w))
            stemmed_words = (stemmer.stem(w) for w in filtered_words if not w in domain_specific_words)
            if use_stem:
                preprocessed_data.append(list(stemmed_words))
            else:
                preprocessed_data.append(list(filtered_words))

        # Remove empty lists
        preprocessed_data = [lst for lst in preprocessed_data if lst != []]

        return preprocessed_data

    def replace_regex(self, string):
        new_string = string
        for (pattern, repl) in self.patterns:
            new_string = re.sub(pattern, repl, new_string)

        return new_string
