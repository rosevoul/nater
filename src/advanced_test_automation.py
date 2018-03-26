import sys
from data_reading import DataReader
from word_preprocessing import WordPreprocessor
from lexicon_creation import LexiconCreator
from spell_correction import SpellCorrector
from word_embeddings import WordEmbeddings
from association_analysis import AssociationAnalysis
from suggestions import most_similar_test_block, find_associated_block
from utils import store_results

class AdvancedTestAutomation(object):
    """Advanced Test Automation based on text matching."""
    def __init__(self):
        self.data = None
        self.test_steps = list()
        self.test_blocks = list()

    def read_data(self, path):
        self.data = DataReader(path)

    def preprocess(self):
        word_preprocessing = WordPreprocessor(self.data.entities, self.data.aliases, split_by_sentence=True)
        docs = word_preprocessing.preprocess(self.data.docs)
        test_steps = word_preprocessing.preprocess(self.data.test_steps)
        test_blocks = word_preprocessing.preprocess(self.data.test_blocks)

        lexicon = LexiconCreator.create(base_corpus=docs)

        spell_corrector = SpellCorrector("lexicon.txt")
        
        self.test_steps = spell_corrector.correct(test_steps)
        self.test_blocks = spell_corrector.correct(test_blocks)

        self.model = WordEmbeddings.generate_model([docs, self.test_blocks, self.test_steps], method="cbow")

        associator = AssociationAnalysis(self.data.implemented_tests, self.data.test_blocks, 
                                            self.data.human_blocks, self.data.human_blocks_children)
        self.associated_blocks = associator.associate_blocks()

    def suggest_matches(self):
        auto_test = []

        for step in self.test_steps:
            block = most_similar_test_block(step, self.model, self.test_blocks)
            if block=="None_similar":
                block = find_associated_block(previous_block, self.associated_blocks)
            auto_test.append([step, block])
            previous_block = block

        # TODO save to a file named with current date or original test name
        store_results(auto_test, "data/auto-tests/results.md")

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
