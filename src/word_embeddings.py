from gensim.models import Word2Vec

class WordEmbeddings(object):
	"""Generate word embeddings using Word2Vec"""
	def __init__(self, arg):
		self.arg = arg

	@staticmethod
	def generate_model(dataset, method, negative, size):

		training_data = dataset
		
		if method is "skipgram" and negative:
			model = Word2Vec(training_data, size=size, min_count=1, window=5, sg=1)
		elif method is "skipgram" and not negative:
			model = Word2Vec(training_data, size=size, min_count=1, window=5, sg=1, negative=0)
		elif method is "cbow" and negative:
			model = Word2Vec(training_data, size=size, min_count=1, window=5)
		else:
			model = Word2Vec(training_data, size=size, min_count=1, window=5, negative=1)

		return model
