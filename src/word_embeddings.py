from gensim.models import Word2Vec

class WordEmbeddings(object):
	"""Generate word embeddings using Word2Vec"""
	def __init__(self, arg):
		self.arg = arg

	@staticmethod
	def generate_model(dataset, method):

		training_data = dataset
		
		if method is "skipgram":
			model = Word2Vec(training_data, min_count=1, size=100, window=5, sg=1)
		else:
			model = Word2Vec(training_data, min_count=1, size=100, window=5)

		return model
