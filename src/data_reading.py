class DataReader(object):
	"""Read the necessary data from various sources."""
	def __init__(self, arg):
		self.docs = []
		self.test_steps = []
		self.test_blocks = []
		self.implemented_tests = []
		self.entities = []
		self.acronyms = []
		