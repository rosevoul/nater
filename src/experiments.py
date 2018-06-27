import pandas as pd
from timeit import default_timer as timer
from recommender import Recommender, RecommenderWithUserFeedback
from data_structures import *
from experiments_visualization import experiment_1_2_a, experiment_1_2_b, experiment_models_a, experiment_models_b


class ExperimentI:

    def __init__(self, path, model):
        self.rec = Recommender(path, model)
        self.test_scenarios = []

    def conduct_experiment(self, k=10):
        self.prepare_experiment()
        test_ids, tests_reqs_GT, method_reqs_R = self.run_experiment()
        self.visualize_experiment(test_ids, tests_reqs_GT, method_reqs_R)

    def prepare_experiment(self):
    #     test_scenarios_path = ["../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/CNFD_014_1.xlsx"]
    #     for path in test_scenarios_path:
    #         test_scenario = self.load_evaluation_test_scenario(path)
    #         self.test_scenarios.append(test_scenario)

        # Tests with Linked Reqs
        tests_with_reqs_path = '../data/advanced/parsed/tests_with_linked_reqs.csv'
        tests_design_steps_path = '../data/advanced/parsed/tests_design_steps.csv'

        tests_with_linked_reqs = pd.read_csv(tests_with_reqs_path)
        tests_design_steps = pd.read_csv(tests_design_steps_path)

        tids = tests_with_linked_reqs['test_id'].tolist()

        unique_test_ids = list(set(tids))
        for tid in unique_test_ids:
            test = tests_with_linked_reqs.loc[
                tests_with_linked_reqs['test_id'] == tid]
            test = test.fillna('')
            title = test['test_name'].tolist()[0]
            description = test['test_description'].tolist()[0]
            req_ids = test['req_id'].tolist()
            req_ids = [int(rid) for rid in req_ids]

            test_design = tests_design_steps.loc[tests_design_steps['Test ID'] == tid]
            test_design = test_design.fillna('')
            step_ids = test_design['Test Design Step Order'].tolist()
            step_descriptions = test_design['Test Design Description'].tolist()
            step_descriptions = [s.split('=')[0] for s in step_descriptions]
            step_expected_results = test_design['Test Design Expected Result'].tolist()
            step_test_blocks_names = ['Test Block']
            step_test_block_params_n_vals = ['[]']
            req_names = ['Req_Name'] * len(req_ids)

            ets = EvaluationTestScenario(tid, title, description, step_ids, step_descriptions, step_expected_results,
                                         step_test_blocks_names, step_test_block_params_n_vals, req_ids, req_names, order='random')
            self.test_scenarios.append(ets)

    def load_evaluation_test_scenario(self, path):
        from data_reading import ModelDataReader
        read_excel = ModelDataReader.read_excel

        tid = read_excel(path, "Test_Info", "Test ID", 0)
        title = read_excel(path, "Test_Info", "Test Title", 0)
        description = read_excel(path, "Test_Info", "Test Description", 0)
        step_ids = read_excel(path, "Steps_n_Blocks_Simple", "Step ID", 0)
        step_descriptions = read_excel(
            path, "Steps_n_Blocks_Simple", "Step Description", 0)
        step_expected_results = read_excel(
            path, "Steps_n_Blocks_Simple", "Expected Result", 0)
        step_test_blocks_names = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Name", 0)
        step_test_block_params_n_vals = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Parameters", 0)
        req_ids = read_excel(path, "Reqs", "Linked Req ID", 0)
        req_ids = [int(rid) for rid in req_ids]

        req_names = read_excel(path, "Reqs", "Linked Req Name", 0)

        return EvaluationTestScenario(tid, title, description, step_ids, step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, req_ids, req_names)

    def run_experiment(self, k=10):
        method_reqs_R = {}

        for method in ["avg", "sta", "tf-idf", "jac", "lsi"]:
            reqs_R = []
            for test_scenario in self.test_scenarios:
                reqs_R.append(self.rec.recommend_reqs_by_id(test_scenario, k, method))
            method_reqs_R[method] = reqs_R

        test_ids = [test.id for test in self.test_scenarios]
        tests_reqs_GT = []
        for test in self.test_scenarios:
            current_test_reqs = [req.id for req in test.reqs_GT]
            tests_reqs_GT.append(current_test_reqs)

        return test_ids, tests_reqs_GT, method_reqs_R

    def visualize_experiment(self, test_ids, tests_reqs_GT, method_reqs_R):
        print("Experiment 1a, k = 10")
        experiment_1_2_a(20, test_ids, tests_reqs_GT, method_reqs_R)

        print("\nExperiment 1b")
        experiment_1_2_b(test_ids, tests_reqs_GT, method_reqs_R)


class ExperimentII:

    def __init__(self, path, model):
        self.rec = Recommender(path, model)
        self.test_scenarios = []

    def conduct_experiment(self, k=20):
        self.prepare_experiment()
        test_steps, test_blocks_GT, method_blocks_R = self.run_experiment()
        self.visualize_experiment(test_steps, test_blocks_GT, method_blocks_R)

    def prepare_experiment(self):
        from data_reading import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_reading import ModelDataReader
        read_excel = ModelDataReader.read_excel

        step_ids = read_excel(path, "Steps_n_Blocks_Simple", "Step ID", 0)
        step_descriptions = read_excel(
            path, "Steps_n_Blocks_Simple", "Step Description", 0)
        step_expected_results = read_excel(
            path, "Steps_n_Blocks_Simple", "Expected Result", 0)
        step_test_blocks_names = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Name", 0)
        step_test_block_params_n_vals = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Parameters", 0)

        return EvaluationTestScenario('tid', 'title', 'description', step_ids,
                                      step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, [], [])

    def run_experiment(self, k=20):
        method_blocks_R = {}

        all_test_steps = [
            step for scenario in self.test_scenarios for step in scenario.steps]

        for method in ["avg", "sta", "tf-idf", "jac", "lsi"]:
            test_blocks_R = []
            for test_step in all_test_steps:
                test_blocks_R.append(self.rec.find_top_blocks(
                    test_step.description, k, method))
            method_blocks_R[method] = test_blocks_R

        test_steps = [
            step.id for scenario in self.test_scenarios for step in scenario.steps]
        block_id = self.rec.data.test_blocks_names.index
        test_blocks_GT = [block_id(
            block[0].name) for scenario in self.test_scenarios for block in scenario.blocks_GT]

        return test_steps, test_blocks_GT, method_blocks_R

    def visualize_experiment(self, test_steps, test_blocks_GT, method_blocks_R):
        print("Experiment 2a, k = 1")
        experiment_1_2_a(1, test_steps, test_blocks_GT, method_blocks_R)
        print("Experiment 2a, k = 5")
        experiment_1_2_a(5, test_steps, test_blocks_GT, method_blocks_R)
        print("Experiment 2a, k = 10")
        experiment_1_2_a(10, test_steps, test_blocks_GT, method_blocks_R)
        print("Experiment 2b")
        experiment_1_2_b(test_steps, test_blocks_GT,  method_blocks_R)


class ExperimentModels:

    def __init__(self, path, model_c, model_cn, model_s, model_sn):
        self.recs = [Recommender(path, model_c), Recommender(path, model_cn), Recommender(path, model_s), Recommender(path, model_sn)]
        self.models = ["cbow", "cbow-negative", "skipgram", "skipgram-negative"]
        self.test_scenarios = []

    def conduct_experiment(self, k=20):
        self.prepare_experiment()
        test_steps, test_blocks_GT, method_blocks_R = self.run_experiment()
        self.visualize_experiment(test_steps, test_blocks_GT, method_blocks_R)

    def prepare_experiment(self):
        from data_reading import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_reading import ModelDataReader
        read_excel = ModelDataReader.read_excel

        step_ids = read_excel(path, "Steps_n_Blocks_Simple", "Step ID", 0)
        step_descriptions = read_excel(
            path, "Steps_n_Blocks_Simple", "Step Description", 0)
        step_expected_results = read_excel(
            path, "Steps_n_Blocks_Simple", "Expected Result", 0)
        step_test_blocks_names = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Name", 0)
        step_test_block_params_n_vals = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Parameters", 0)

        return EvaluationTestScenario('tid', 'title', 'description', step_ids,
                                      step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, [], [])

    def run_experiment(self, k=20):
        model_blocks_R = {}

        all_test_steps = [
            step for scenario in self.test_scenarios for step in scenario.steps]

        for i, rec in enumerate(self.recs):
            test_blocks_R = []
            for test_step in all_test_steps:
                test_blocks_R.append(rec.find_top_blocks(
                    test_step.description, k, 'avg'))
            model_blocks_R[self.models[i]] = test_blocks_R

        test_steps = [
            step.id for scenario in self.test_scenarios for step in scenario.steps]
        block_id = rec.data.test_blocks_names.index
        test_blocks_GT = [block_id(
            block[0].name) for scenario in self.test_scenarios for block in scenario.blocks_GT]

        return test_steps, test_blocks_GT, model_blocks_R

    def visualize_experiment(self, test_steps, test_blocks_GT, model_blocks_R):
        print("Experiment 2a, k = 1")
        experiment_models_a(1, test_steps, test_blocks_GT, model_blocks_R)
        print("Experiment 2a, k = 5")
        experiment_models_a(5, test_steps, test_blocks_GT, model_blocks_R)
        print("Experiment 2a, k = 10")
        experiment_models_a(10, test_steps, test_blocks_GT, model_blocks_R)
        print("Experiment 2b")
        experiment_models_b(test_steps, test_blocks_GT,  model_blocks_R)

# =============================================================================

class ExperimentUserFeedback:
    def __init__(self, path, model):
        self.rec = RecommenderWithUserFeedback(path, model)
        self.test_scenarios = []

    def conduct_experiment(self):
        self.prepare_experiment()
        test_steps, test_blocks_GT, method_blocks_R = self.run_experiment(iterations=2)
        self.visualize_experiment(test_steps, test_blocks_GT, method_blocks_R)


    def prepare_experiment(self):
        from data_reading import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_reading import ModelDataReader
        read_excel = ModelDataReader.read_excel

        step_ids = read_excel(path, "Steps_n_Blocks_Simple", "Step ID", 0)
        step_descriptions = read_excel(
            path, "Steps_n_Blocks_Simple", "Step Description", 0)
        step_expected_results = read_excel(
            path, "Steps_n_Blocks_Simple", "Expected Result", 0)
        step_test_blocks_names = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Name", 0)
        step_test_block_params_n_vals = read_excel(
            path, "Steps_n_Blocks_Simple", "Test Block Parameters", 0)

        return EvaluationTestScenario('tid', 'title', 'description', step_ids,
                                      step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, [], [])


    def run_experiment(self, iterations):
        iterations_blocks_R = []

        for iteration in range(iterations):
            test_blocks_R = []
            for scenario in self.test_scenarios:
                for test_step in scenario.steps:
                    test_blocks_R.append(self.rec.find_top_blocks(test_step.description, N=10, method='avg'))
                iterations_blocks_R.append(test_blocks_R)

        test_steps = [step.id for scenario in self.test_scenarios for step in scenario.steps]
        block_id = self.rec.data.test_blocks_names.index
        test_blocks_GT = [block_id(block[0].name) for scenario in self.test_scenarios for block in scenario.blocks_GT]

        return test_steps, test_blocks_GT, iterations_blocks_R


    def visualize_experiment(self, test_steps, test_blocks_GT, iterations_blocks_R):
        print(iterations_blocks_R)
