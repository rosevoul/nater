import re
import string
from nltk import word_tokenize, sent_tokenize, pos_tag
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

    
    def __init__(self, entities, aliases, test_blocks_parameters, split_by_sentence=False):
        self.aliases = aliases
        self.split_by_sentence = split_by_sentence

        self.split_data_words = []

        self.patterns = [(re.compile(regex), repl)
                         for (regex, repl) in self.REPLACEMENT_PATTERNS]

        self.all_block_parameters = set([param for block in self.preprocess_block_parameters(test_blocks_parameters) for param in block])
        spacecraft_parameters, applications, systems = entities
        self.spacecraft_parameters = [w.lower() for w in spacecraft_parameters]
        applications = [w.lower() for w in applications]
        systems = [w.lower() for w in systems]
        self.domain_specific_words = set(
            ['sparam', 'eud4s2k', 's2k', 'sles12', 'misccontext.sta'] + applications + systems)
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.remove('all')
        self.punctuation = string.punctuation + '``' + "''"
        self.invalid_symbols = set(string.punctuation.replace("_", ""))

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

        self.split_data_words = [word_tokenize(
            text) for text in regex_filter_data]

    def model_preprocess(self, data):
        # Split to sentences and apply regex filter
        # Strip the numbers
        # Strip newline characters
        # Lowercase
        # Remove stopwords
        # Remove all the punctuation
        # Replace spacecraft parameters with sparam
        # Remove words that contain numbers or/and punctuation

        self.split(data)
        preprocessed_data = []
        filtered_words = []
        for words in self.split_data_words:
            # filtered_words = (w for w in words if not w.isnumeric())
            # filtered_words = (w.replace('\n', '').replace('\r', '') for w in words)
            # filtered_words = (w.lower() for w in filtered_words)
            # filtered_words = (w for w in filtered_words if not w in self.stop_words)
            # filtered_words = (
            #     w for w in filtered_words if w not in self.punctuation)
            # filtered_words = (
            #     'sparam' if w in self.spacecraft_parameters else w for w in filtered_words)
            # filtered_words = (w for w in filtered_words if w in self.domain_specific_words or not any(
            #     c.isdigit() or c in self.invalid_symbols for c in w))
            # preprocessed_data.append(list(filtered_words))

            preprocessed_data.append(self.nlp_filter(words))

        # Remove empty lists
        preprocessed_data = [lst for lst in preprocessed_data if lst]

        return preprocessed_data

    def apply_stem(self, text):
        stemmer = PorterStemmer()
        stemmed_data = []
        for words in text:
            stemmed_words = (stemmer.stem(w)
                             for w in words if not w in self.domain_specific_words)
            stemmed_data.append(list(stemmed_words))

        return stemmed_data

    def replace_regex(self, string):
        new_string = string
        for (pattern, repl) in self.patterns:
            new_string = re.sub(pattern, repl, new_string)

        return new_string

    def preprocess_variable_names(self, data):
        # Process variable-like names(containing uppercase and camel case) to keywords        
        names = []
        for variable_name in data:
            name_keywords = []
            name_split = variable_name.split('_') 
            left = name_split[0]
            name_keywords = self.split_uppercase(left)
            if len(name_split) > 1:
                right = name_split[1:]
                name_keywords.extend(self.split_uppercase(''.join(right)))            
            names.append(name_keywords)
        
        return names


    def nlp_filter(self, bag_of_words):
        """ Applies nlp filter in a sentence represented by a bag of words
        Input: a string, raw natural language sentence or a bag of words representing a sentence
        Ouput: a filtered bag of words
        """
        
        if type(bag_of_words) != list:
            bag_of_words = word_tokenize(bag_of_words)
        
        filtered_words = (w.lower() for w in bag_of_words)
        filtered_words = (w for w in filtered_words if not w in self.stop_words)
        filtered_words = (w for w in filtered_words if not w in self.punctuation)
        filtered_words = (w for w in filtered_words if w in self.domain_specific_words 
                            or not any(c.isdigit() or c in self.invalid_symbols for c in w))

        return list(filtered_words)

    def remove_test_words(self, bag_of_words):
        test_word_parts = ['test', 'verif']
        filtered_words = (w for w in bag_of_words if not any(word_part in w for word_part in test_word_parts))

        return list(filtered_words)

    def split_compound_sentence(self, data):
        """ Split one 'and' or ',' compound sentence to more sentences
        Input: a string, raw natural language sentence
        Output: a list of strings, each string is representing a sentence 
        """
        sentences = []
        data = data.replace(' and ', ' , ')
        sents = data.split(',')
        if len(sents) != 1:
            sent_verb = [] * len(sents)
            for i, sent in enumerate(sents):
                if i == 0:
                    pos = pos_tag(word_tokenize('I ' + sent))
                else: 
                    pos = pos_tag(word_tokenize(sent))
                verbs = [w[0] for w in pos if w[1].startswith('V') and w[1] != 'VBG']
                if verbs:
                    previous_verb = verbs
                    sent_verb.append(verbs)
                else:
                    sent_verb.append(previous_verb)
                    sent = previous_verb[-1] + sent
                sentences.append(sent)
            return sentences
        else:
            return [data]

    def identify_block_parameter(self, parameter_parts):
        parameter_parts.reverse()
        parameter_candidates = []
        parameter_part_candidates = [param for param in self.all_block_parameters if parameter_parts[0] in param.lower()]

        i = 1
        while parameter_part_candidates:
            parameter_candidates.append(parameter_part_candidates)
            parameter_part_candidates = [param for param in parameter_candidates[i-1] if parameter_parts[i].lower() in param.lower()]
            i = i + 1
        if parameter_candidates:
            parameter_candidate = parameter_candidates[-1][0]
            
            return parameter_candidate

        else: 
            return "NoPARAM"

    def extract_block_parameters(self, sentence):
        """
        Input: a string, raw natural language sentence
        Ouput: a tuple (keywords, params)
                keywords: a bag of words that contains the keywords for the sentence
                params: a bag of tuples (parameter, value) that contains the parameters
                        and the corresponding values for the sentence
        """
        words = word_tokenize(sentence)
        param_assignments = words.count('=')
        
        if not param_assignments:
            params_n_vals = []
        
        params_n_vals = []
        for _ in range(param_assignments):
            sid = words.index('=')
            param, val = self.identify_block_parameter(words[:sid]), words[sid+1]
            params_n_vals.append((param.lower(), val))
            del words[sid:sid+2]
            
        return words, params_n_vals
    
    @staticmethod
    def preprocess_block_parameters(data):
        # Extract the block parameters only (without values)
        params_n_vals = (eval(block_params_n_vals) for block_params_n_vals in data) 
        parameters = []
        for block_params_n_vals in params_n_vals:
            block_parameters = [param.lower() for (param, val) in block_params_n_vals]
            parameters.append(block_parameters)

        return parameters

    @staticmethod
    def split_uppercase(s):
        r = []
        l = False
        for c in s:
            # l being: last character was not uppercase
            if l and c.isupper():
                r.append(' ')
            l = not c.isupper() and not c.isdigit()
            r.append(c)
        result = ''.join(r)
        
        return result.lower().split()        
