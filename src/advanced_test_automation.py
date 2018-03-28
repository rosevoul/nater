import sys
from data_reading import DataReader
from word_preprocessing import WordPreprocessor
from lexicon_creation import LexiconCreator
from spell_correction import SpellCorrector
from word_embeddings import WordEmbeddings
from association_analysis import AssociationAnalysis
from suggestions import most_similar_test_block, find_associated_block
from utils import store_results
import pickle
import os

class AdvancedTestAutomation(object):
    """Advanced Test Automation based on text matching."""
    def __init__(self):
        self.data = None
        self.test_steps = list()
        self.test_blocks = list()

    def read_data(self, path):
        self.path = path
        ser_data_path = self.path + "/tmp/data.bin"
        if (os.path.exists(ser_data_path)):
            self.data = pickle.load(open(ser_data_path, "rb"))
        else:
            self.data = DataReader(path)
            pickle.dump(self.data, open(ser_data_path, "wb"))

    def preprocess(self):
        ser_preproc_test_steps_path = self.path + "/tmp/preproc_test_steps.bin"
        ser_preproc_model_path = self.path + "/tmp/preproc_model.bin"
        ser_preproc_test_blocks_path = self.path + "/tmp/preproc_test_blocks.bin"
        ser_preproc_associated_blocks_path = self.path + "/tmp/preproc_associated_blocks.bin"

        if (os.path.exists(ser_preproc_associated_blocks_path)):
            self.test_steps = pickle.load(open(ser_preproc_test_steps_path, "rb"))
            self.model = pickle.load(open(ser_preproc_model_path, "rb"))
            self.test_blocks = pickle.load(open(ser_preproc_test_blocks_path, "rb"))
            self.associated_blocks = pickle.load(open(ser_preproc_associated_blocks_path, "rb"))
        else:
            word_preprocessing = WordPreprocessor(self.data.entities, self.data.aliases, split_by_sentence=True)
            docs = word_preprocessing.preprocess(self.data.docs)
            test_steps = word_preprocessing.preprocess(self.data.test_steps)
            test_blocks = word_preprocessing.preprocess(self.data.test_blocks)

            lexicon = LexiconCreator.create(self.path + "/tmp/lexicon.txt", base_corpus=docs)
            spell_corrector = SpellCorrector(self.path + "/tmp/lexicon.txt")
            self.test_steps = spell_corrector.correct(test_steps)
            self.test_blocks = spell_corrector.correct(test_blocks)

            self.model = WordEmbeddings.generate_model([docs, self.test_blocks, self.test_steps], method="cbow")

            associator = AssociationAnalysis(self.data.implemented_tests, self.data.test_blocks_info, 
                                                self.data.human_blocks, self.data.human_blocks_children, self.path)
            self.associated_blocks = associator.associate_blocks()

            pickle.dump(self.test_steps, open(ser_preproc_test_steps_path, "wb"))
            pickle.dump(self.model, open(ser_preproc_model_path, "wb"))
            pickle.dump(self.test_blocks, open(ser_preproc_test_blocks_path, "wb"))
            pickle.dump(self.associated_blocks, open(ser_preproc_associated_blocks_path, "wb"))

    def suggest_matches(self):
        auto_test = []
        print(self.associated_blocks)

        for i, step in enumerate(self.test_steps[:100]):
            block = most_similar_test_block(step, self.model, self.test_blocks)
            if block=="None_similar":
                block = find_associated_block(previous_block, self.associated_blocks)
            auto_test.append([step, block])
            previous_block = block
            print(str(i + 1) + "/" + str(len(self.test_steps[:100])))

        # TODO save to a file named with current date or original test name
        store_results(auto_test, self.path + "/auto-tests/results.md")

    def evaluate(self):
        pass

def main():
    path = sys.argv[1]

    ata = AdvancedTestAutomation()
    ata.read_data(path)
    print("data read!")
    ata.preprocess()
    print("preprocess finished!")
    ata.suggest_matches()
    print("suggestions generated!")
    ata.evaluate()

if __name__ == '__main__':
    main()
