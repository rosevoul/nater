import numpy as np
from nltk import pos_tag
from sklearn.metrics.pairwise import cosine_similarity

def similarity_vector(sent, model):
	sent_vectors = np.empty((0,100), dtype="float32")
	for word in sent:
		word_vector = model.wv[word]
		sent_vectors = np.append(sent_vectors, np.array([word_vector]), axis=0)

	mean_vector = np.mean(sent_vectors, axis=0)
	std_vector = np.std(sent_vectors, axis=0)
	max_vector = np.max(sent_vectors, axis=0)
	min_vector = np.min(sent_vectors, axis=0)

	# Add the metrics' vectors to one vector; this is the similarity vector
	similarity_vector = np.concatenate([mean_vector, std_vector, max_vector, min_vector])

	return similarity_vector

def extract_pos(sent):
	tagged_words = pos_tag(['We'] + sent)[1:]
	# keep the primary verb and the primary noun
	# TODO change this to spacy implementation
	verbs = [word for (word, tag) in tagged_words if tag.startswith('VBP')]
	nouns = [word for (word, tag) in tagged_words if tag.startswith('NNP')]
	pos_tagged_sent = verbs
	pos_tagged_sent.extend(nouns)
	
	return pos_tagged_sent 

def most_similar_test_block(step, model, test_blocks, threshold=0.8, method="sent"):
	similarities = []

	for block in test_blocks:
		if method=="pos":
			block = extract_pos(block)
			step = extract_pos(step)
		step_vector = similarity_vector(step, model)
		block_vector = similarity_vector(block, model) # TODO precalculate the similarity vectors of the blocks
		# calculate the similarity and save in array
		similarities.append(cosine_similarity([step_vector], [block_vector])[0][0])

	# Return the block description that is matching the highest similarity
	top_similarity = max(similarities)
	if top_similarity < threshold:
		return "None_similar"

	# Get index of top similarity
	most_similar_block = test_blocks[np.argmax(similarities)]

	return most_similar_block

def find_associated_block(previous_block, associated_blocks):

	for i, block_set in enumerate(associated_blocks):
		for j, block in enumerate(block_set):
			if associated_blocks[i][j] == previous_block:
				associated_block = associated_blocks[i+1]
				return associated_block

	return "None_associated"
