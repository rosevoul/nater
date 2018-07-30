import enchant
from nltk.metrics import edit_distance
from collections import Counter
from operator import itemgetter


class SpellCorrector(object):
    """Automatically replace misspelled words based on the domain specific dictionary using the Enchant library

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
        for s, sentence in enumerate(text):
            text[s] = self.correct_sentence((sentence))

        return text

    def correct_sentence(self, sentence):
        for w, word in enumerate(sentence):
            sentence[w] = self.correct_word((word))

        return sentence

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


class LexiconCreator(object):
    """Create a lexicon using a custom corpus."""

    @classmethod
    def create(cls, file_path, base_corpus):
        flat_base_corpus = [
            word for sublist in base_corpus for word in sublist]
        frequencies = Counter(flat_base_corpus)

        sorted_words = sorted(frequencies.items(),
                              reverse=True, key=itemgetter(1))
        sorted_words = [w[0] for w in sorted_words]

        cls.write_to_file(file_path, sorted_words)

    @staticmethod
    def write_to_file(file_path, words):
        with open(file_path, "w") as f:
            for w in words:
                f.write('{0}\n'.format(w))
