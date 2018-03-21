import sys
from data_reading import DataReader
from word_preprocessing import WordPreprocessor
from lexicon_creation import LexiconCreator
from spell_correction import SpellCorrector
from word_embeddings import WordEmbeddings
from association_analysis import AssociationAnalysis

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

        spell_corrector = SpellCorrector(lexicon)
        self.test_steps = spell_corrector.correct(test_steps)
        self.test_blocks = spell_corrector.correct(test_blocks)

        model = WordEmbeddings.generate_model([docs, self.test_blocks, self.test_steps], method="cbow")

        associations = AssociationAnalysis.associate_blocks(self.data.implemented_tests)

    def suggest_matches(self):
        pass

    def evaluate(self):
        pass

def main():
    path = sys.argv[1]

    ata = AdvancedTestAutomation()
    ata.read_data(path)
    ata.preprocess()
    ata.suggest_matches()
    ata.evaluate()

if __name__ == '__main__':
    main()
