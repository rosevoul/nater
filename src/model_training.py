import sys
from data_reading import ModelDataReader
from word_preprocessing import WordPreprocessor
from lexicon_creation import LexiconCreator
from spell_correction import SpellCorrector
from word_embeddings import WordEmbeddings
import pickle
import os

class ModelTraining(object):
    """Text preprocessing and generation of a word2vec model"""
    def __init__(self, path):
        self.path = path
        self.data = None
        self.model = None
        self.test_steps = list()
        self.test_blocks = list()
        self.read_data()

    def read_data(self):
        ser_data_path = self.path + "/tmp/model_data.bin"
        if (os.path.exists(ser_data_path)):
            self.data = pickle.load(open(ser_data_path, "rb"))
        else:
            self.data = ModelDataReader(path)
            pickle.dump(self.data, open(ser_data_path, "wb"))

    def preprocess(self):
        # First preprocess data to create lexicon and use it to spell correct
        word_preprocessing = WordPreprocessor(self.data.entities, self.data.aliases, self.data.test_blocks_parameters, split_by_sentence=True)
        lexicon_path = self.path + "/tmp/lexicon.txt"
        if not (os.path.exists(lexicon_path)):
            correct_spelled_data = word_preprocessing.model_preprocess(self.data.correct_spelled_data)
            lexicon = LexiconCreator.create(lexicon_path, base_corpus=correct_spelled_data)
        spell_corrector = SpellCorrector(lexicon_path)
        
        docs = word_preprocessing.model_preprocess(self.data.docs)
        test_steps = word_preprocessing.model_preprocess(self.data.test_steps)
        test_blocks_names = word_preprocessing.preprocess_variable_names(self.data.test_blocks_names)
        test_blocks_descriptions = word_preprocessing.model_preprocess(self.data.test_blocks_descriptions)
        test_blocks_preconditions = word_preprocessing.model_preprocess(self.data.test_blocks_preconditions)
        test_blocks_postconditions = word_preprocessing.model_preprocess(self.data.test_blocks_postconditions)       
        test_blocks_parameters = word_preprocessing.preprocess_block_parameters(self.data.test_blocks_parameters)

        test_steps = spell_corrector.correct(test_steps)
        
        # Store corrected data to model_lexicon
        model_dataset = [docs, test_blocks_names, test_blocks_descriptions, test_blocks_preconditions, 
                         test_blocks_postconditions, test_blocks_parameters, test_steps]
        self.model_corpus = []
        for lst in model_dataset:
            self.model_corpus.extend(lst)
        lexicon = LexiconCreator.create(self.path + "/tmp/model_lexicon.txt", base_corpus=self.model_corpus)
        
    def get_tokens_length(self):
        return sum(len(lst) for lst in self.model_corpus)

    def generate(self, method="cbow", negative=True):
        self.model = WordEmbeddings.generate_model(self.model_corpus, method, negative)
        
        store_model_path = self.path + "/tmp/model_CN.bin"
        pickle.dump(self.model, open(store_model_path, "wb"))

    def get_vocab_length(self):
        vocab = list(self.model.wv.vocab.keys())
        
        return len(vocab)

if __name__ == '__main__':
    path = '../data/advanced/'

    print("Reading data...")
    model = ModelTraining(path)
    print("Preprocessing data...")
    model.preprocess()
    print("Tokens: ")
    print(model.get_tokens_length())
    print("Generating model...")
    model.generate()
    print("Model generated.")
    print("Vocab:")
    print(model.get_vocab_length())


