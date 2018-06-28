from copy import deepcopy
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from data_reading import DataReader
from word_preprocessing import WordPreprocessor
from suggestions import most_similar_text, assign_scores, compute_similarities, parameter_similarities, score_associated_blocks
import pickle
import os
import pandas as pd
from pprint import pprint

class Recommender(object):
    def __init__(self, path, model=None):
        self.path = path
        self.model = model
        self.data = None

        self.load_data()

    def load_data(self):
        self.data = DataReader(self.path)
        self.preprocess_data()

    def preprocess_data(self):
        self.prep = WordPreprocessor(self.data.entities, self.data.aliases, self.data.test_blocks_parameters)

        # Block description & name keywords preprocessing
        self.test_blocks_n_keywords = self.prep.preprocess_variable_names(self.data.test_blocks_names)
        self.test_blocks_d_keywords = []
        for d in self.data.test_blocks_descriptions:
            filtered_keywords = self.prep.nlp_filter(d)
            self.test_blocks_d_keywords.append(filtered_keywords)

        # Merge the keywords
        self.test_blocks_nd_keywords = deepcopy(self.test_blocks_n_keywords)
        for i, n_kw in enumerate(self.test_blocks_nd_keywords):
            d_kw = self.test_blocks_d_keywords[i]
            d_keywords_non_duplicate = [kw for kw in d_kw if kw not in n_kw]
            n_kw.extend(d_keywords_non_duplicate)
            self.test_blocks_nd_keywords[i] = list(n_kw)

        # Parameters preprocessing
        self.test_blocks_parameters = self.prep.preprocess_block_parameters(
            self.data.test_blocks_parameters)

        # Requirements preprocessing
        self.reqs_keywords = []
        for rd in self.data.reqs_descriptions:
            filtered_req_keywords = self.prep.nlp_filter(rd)
            self.reqs_keywords.append(list(set(filtered_req_keywords)))

    def inspect_test_block(self, test_block_name):
        print(test_block_name)
        bi = self.data.test_blocks_names.index(test_block_name)

        print("\nDescr: ", self.data.test_blocks_descriptions[bi])
        print("PreCnd: ", self.data.test_blocks_preconditions[bi])
        print("PostCnd: ", self.data.test_blocks_postconditions[bi])
        print("Parameters: ", self.data.test_blocks_parameters[bi])
        print()
        print("Keywords: ")
        pprint(self.test_blocks_nd_keywords[bi])
        
        print("Score: ", self.blocks_scores[bi])

    def inspect_req(self, req_id):
           print(req_id)
           rid = self.data.reqs_ids.index(req_id)

           print("\nDescr: ", self.data.reqs_descriptions[rid])
           print("Name: ", self.data.reqs_names[rid])
           print("Cover Status: ", self.data.reqs_cover_statuses[rid])
           
           print("Score: ", self.req_scores[rid])


    def extract_step_keywords(self, test_step_description):        
        # Extract, keywords, parameters and values
        keywords, params_n_vals = self.prep.extract_block_parameters(test_step_description)
        # Apply NLP filter to keywords
        filtered_description_keywords = self.prep.nlp_filter(keywords)
        # Apply parameter filter to parameters
        filtered_parameters = [pv[0]for pv in params_n_vals if params_n_vals]

        return filtered_description_keywords, filtered_parameters

    def extract_test_keywords(self, test_scenario):
        filtered_test_title = self.prep.preprocess_variable_names(test_scenario.title)[0]
        filtered_test_description = self.prep.nlp_filter(test_scenario.description)
        filtered_test_description = self.prep.remove_test_words(filtered_test_description)

        filtered_test_steps_descriptions = [self.prep.nlp_filter(step.description) for step in test_scenario.steps]
        filtered_test_steps_descriptions = [kw for descr in filtered_test_steps_descriptions for kw in descr]
        
        test_keywords = []
        test_keywords.extend(filtered_test_title + filtered_test_description + 
                             filtered_test_steps_descriptions)
        test_keywords = list(set(test_keywords))
            
        return test_keywords

    def recommend_test_blocks(self, test_step_description, N=10, method='avg'):
        return [self.data.test_blocks_names[i] for i in self.find_top_blocks(test_step_description, N, method)]

    def recommend_reqs(self, test_scenario,  N=10, method='tf-idf'):
        return [self.data.reqs_descriptions[i] for i in self.find_top_reqs(test_scenario, N, method)]
    
    def recommend_reqs_by_id(self, test_scenario, N, method):
        return [self.data.reqs_ids[i] for i in self.find_top_reqs(test_scenario, N, method)]
    
    def find_top_blocks(self, test_step_description, N, method):
        description_keywords, parameters = self.extract_step_keywords(test_step_description)
        # Similarity of keywords
        k_similarities = compute_similarities(description_keywords, self.test_blocks_nd_keywords, method, self.model)
        # Similarity of parameters
        p_similarities = parameter_similarities(parameters, self.test_blocks_parameters)
        # Recommender scores
        top_blocks_indices, self.blocks_scores = assign_scores(N, k_similarities, 0.8, p_similarities, 0.2)
        
        return top_blocks_indices

    def find_top_reqs(self, test_scenario, N, method):
            test_keywords = self.extract_test_keywords(test_scenario)
            top_req_indices, self.req_scores = most_similar_text(test_keywords, self.reqs_keywords, self.model, N, method)
            
            return top_req_indices
    

class FinalRecommender(Recommender):
    
    def load_data(self):
        ser_data_path = self.path + "/tmp/data.bin"
        if (os.path.exists(ser_data_path)):
            self.data = pickle.load(open(ser_data_path, "rb"))
        else:
            self.data = DataReader(self.path)
            pickle.dump(self.data, open(ser_data_path, "wb"))
        
        self.preprocess()

class PhaseIIRecommender(Recommender):
    """Recommender with the ability to split compound sentences.
    """
    def parse_user_input(self, user_test_step):
        description = user_test_step.description
        expected_result = user_test_step.expected_result
        description_sentences = self.prep.split_compound_sentence(description)
        expected_result_sentences = self.prep.split_compound_sentence(expected_result)

        print("Description contains ", len(description_sentences), " sentences.")
        print("Expected result contains ", len(expected_result_sentences), " sentences.")
        
        return description_sentences, expected_result_sentences


class PhaseIIIRecommender(Recommender):
    """Recommender with the ability to satisfy preconditions.
    """
    def satisfy_preconditions(self, test_block_name):
        bi = self.data.test_blocks_names.index(test_block_name)
        prec = self.data.test_blocks_preconditions[bi]
        if prec == 'The action has been performed':
            prec = ''
        precondition_keywords = self.prep.nlp_filter(
            prec)

        if precondition_keywords:
            pres_similarities = tfidf_similarities(
                precondition_keywords, self.stack)
            pres_similarities = [value for j, value in pres_similarities]
            print("Block Precondition and Stack similarities: ", pres_similarities)
            threshold = 0.9
            if max(pres_similarities) < threshold:
                print("---------------------------")
                print("CASE M")
                print("No similarity greater than ", str(
                    threshold), ". MIDDLE STEP has to be added before this one with Expected Result = Current block Precondition...")
                middle_step_expected_result = self.data.test_blocks_preconditions[
                    bi]
                print("MIDDLE STEP EXPECTED RESULT: ", middle_step_expected_result)
                # L3 recommendations
                middle_block = self.recommend("", middle_step_expected_result)
                print("MIDDLE BLOCK: ", middle_block)
                print("---------------------------")
            else:
                print("CASE R")
        else:
            print("CASE R")

        def update_stack(self, test_block_name):
            bi = self.data.test_blocks_names.index(test_block_name)
            postcnd = self.test_blocks_poc_keywords[bi]

            for kw in postcnd:
                if "stop" in kw or "close" in kw:
                    self.stack.pop()

            if postcnd:
                self.stack.append(postcnd)

            print("Stack: ", self.stack)

class RecommenderWithUserFeedback(Recommender):
    """Recommender that incorporates user feedback.
    """
    def load_data(self):
        self.data = DataReader(self.path)
        self.preprocess_data()
        self.tests_dataframe = self.load_tests()

    def extract_old_tests(self):
        timestamps = self.tests_dataframe.timestamp.unique().tolist()
        tests = []
        for timestamp in timestamps:
            test = self.tests_dataframe.loc[self.tests_dataframe['timestamp'] == timestamp, 'block_id'].tolist()
            tests.append(test)
        
        return tests

    def load_tests(self):
       self.tests_blocks_file = self.path + '/tmp/tests_n_blocks.csv'
       if os.path.exists(self.tests_blocks_file):
           return pd.read_csv(self.tests_blocks_file)
       
       return pd.DataFrame(columns=['timestamp', 'title', 'step', 'block', 'block_id'])

    def store_test_n_blocks(self, title, steps, blocks):
        block_ids = [self.data.test_blocks_names.index(block) for block in blocks]
        timestamp = str(pd.Timestamp.now())
        # current_test = pd.DataFrame({'timestamp': timestamp,'title': title, 'step': steps, 'block': blocks, 'block_id': block_ids})
        current_test = pd.DataFrame({'step': steps, 'block': blocks, 'block_id': block_ids})
        current_test['timestamp'] = timestamp
        print("TITLE", title)
        current_test['title'] = title
        self.tests_dataframe = self.tests_dataframe.append(current_test, ignore_index = True)
        
        self.tests_dataframe.to_csv(self.tests_blocks_file, index=False)

    def find_top_blocks(self, test_step_description, selected_blocks, N, method):
        description_keywords, parameters = self.extract_step_keywords(test_step_description)
        # Similarity of keywords and parameters
        k_similarities = compute_similarities(description_keywords, self.test_blocks_nd_keywords, method, self.model)
        p_similarities = parameter_similarities(parameters, self.test_blocks_parameters)
        
        # Association Analysis Confidence scores
        old_tests = self.extract_old_tests()
        test_blocks_indices = list(range(len(self.data.test_blocks_names)))
        
        if selected_blocks and old_tests:
            confidence_scores = score_associated_blocks(old_tests, selected_blocks, test_blocks_indices)
        else:
            confidence_scores = []
                
        # Recommender scores        
        top_blocks_indices, self.blocks_scores = assign_scores(N, k_similarities, 0.5, p_similarities, 0.1, confidence_scores, 0.4)
        
        return top_blocks_indices