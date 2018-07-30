import pandas as pd
from timeit import default_timer as timer
from recommender import Recommender, RecommenderWithUserFeedback
from data_structures import *
from experiments_visualization import *


class ExperimentI:

    def __init__(self, path, model):
        self.rec = Recommender(path, model)
        self.test_scenarios = []

    def conduct_experiment(self, k=10):
        self.prepare_experiment()
        test_ids, tests_reqs_GT, method_reqs_R = self.run_experiment()
        self.visualize_experiment(test_ids, tests_reqs_GT, method_reqs_R)

    def prepare_experiment(self):
        test_scenarios_path = [
            "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/CNFD_014_1.xlsx"]
        for path in test_scenarios_path:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from data_container import ModelDataReader
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

        req_names = read_excel(path, "Reqs", "Linked Req Description", 0)

        return EvaluationTestScenario(tid, title, description, step_ids, step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, req_ids, req_names)

    def run_experiment(self, k=10):
        method_reqs_R = {}

        for method in ["avg", "sta", "tf-idf", "jac", "lsi"]:
            reqs_R = []
            for test_scenario in self.test_scenarios:
                reqs_R.append(self.rec.recommend_reqs_by_id(
                    test_scenario, k, method))
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
        from data_container import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_container import ModelDataReader
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
                    test_step.description, k, method, text_weight=0.9, param_weight=0.1))
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
        self.recs = [Recommender(path, model_c), Recommender(
            path, model_cn), Recommender(path, model_s), Recommender(path, model_sn)]
        self.models = ["cbow", "cbow-negative",
                       "skipgram", "skipgram-negative"]
        self.test_scenarios = []

    def conduct_experiment(self, k=20):
        self.prepare_experiment()
        test_steps, test_blocks_GT, method_blocks_R = self.run_experiment()
        self.visualize_experiment(test_steps, test_blocks_GT, method_blocks_R)

    def prepare_experiment(self):
        from data_container import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_container import ModelDataReader
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
                    test_step.description, k, 'avg', text_weight=0.9, param_weight=0.1))
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


class ExperimentUserFeedback:

    def __init__(self, path, model):
        self.rec = RecommenderWithUserFeedback(path, model)
        self.test_scenarios = []

    def conduct_experiment(self):
        self.prepare_experiment()
        tests_steps, tests_blocks_GT, method_blocks_R = self.run_experiment(
            iterations=15)
        self.visualize_experiment(
            tests_steps, tests_blocks_GT, method_blocks_R)

    def prepare_experiment(self):
        from data_container import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_container import ModelDataReader
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

        return EvaluationTestScenario(tid, title, description, step_ids,
                                      step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, [], [])

    def run_recommender_all_tests(self, rec, test_scenarios):

        all_test_scenarios_blocks_R = []
        block_id = rec.data.test_blocks_names.index
        for scenario in test_scenarios:

            scenario_steps = []
            test_blocks_R = []
            selected_blocks = []
            for i, test_step in enumerate(scenario.steps):
                test_blocks_R.append(rec.find_top_blocks(
                    test_step.description, selected_blocks, N=10, method='avg'))
                selected_block = scenario.blocks_GT[i][0].name
                scenario_steps.append(test_step.description)
                selected_blocks.append(block_id(selected_block))

            rec.store_test_n_blocks(
                scenario.title[0], scenario_steps, selected_blocks)
            all_test_scenarios_blocks_R.append(test_blocks_R)

        return all_test_scenarios_blocks_R

    def run_experiment(self, iterations):
        iterations_tests_blocks_R = []

        for itr in range(iterations):
            print(itr + 1, "/", iterations, end="\r")
            all_test_scenarios_blocks_R = self.run_recommender_all_tests(
                self.rec, self.test_scenarios)
            iterations_tests_blocks_R.append(all_test_scenarios_blocks_R)

        test_steps = [
            step.id for scenario in self.test_scenarios for step in scenario.steps]

        tests_steps = []
        tests_blocks_GT = []

        block_id = self.rec.data.test_blocks_names.index

        for scenario in self.test_scenarios:
            tests_steps.append([step.id for step in scenario.steps])
            tests_blocks_GT.append([block_id(block[0].name)
                                    for block in scenario.blocks_GT])

        return tests_steps, tests_blocks_GT, iterations_tests_blocks_R

    def visualize_experiment(self, tests_steps, tests_blocks_GT, iterations_tests_blocks_R):
        number_of_tests = len(self.test_scenarios)
        experiment_user_feedback(
            number_of_tests, tests_steps, tests_blocks_GT, iterations_tests_blocks_R)


class ExperimentTimePerformance:

    def __init__(self, path, model):
        self.rec = Recommender(path, model)
        self.test_scenarios = []

    def conduct_experiment(self):
        self.prepare_experiment()
        reqs_R_times, blocks_R_times = self.run_experiment()
        self.visualize_experiment(reqs_R_times, blocks_R_times)

    def prepare_experiment(self):
        from data_container import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_container import ModelDataReader
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
        req_names = read_excel(path, "Reqs", "Linked Req Description", 0)

        return EvaluationTestScenario(tid, title, description, step_ids, step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, req_ids, req_names)

    def run_experiment(self):
        reqs_R_times = []
        blocks_R_times = []

        for test_scenario in self.test_scenarios:
            start = timer()
            self.rec.recommend_reqs(test_scenario)
            reqs_R_times.append(timer() - start)

            block_R_times = []

            for test_step in test_scenario.steps:
                start = timer()
                self.rec.recommend_test_blocks(test_step.description)
                block_R_times.append(timer() - start)

            blocks_R_times.append(block_R_times)

        return reqs_R_times, blocks_R_times

    def visualize_experiment(self, reqs_R_times, blocks_R_times):
        number_of_tests = len(self.test_scenarios)
        experiment_time_performance(
            number_of_tests, reqs_R_times, blocks_R_times)


class ExperimentTestCoverage:

    def __init__(self, path, model):
        self.rec = Recommender(path, model)
        self.test_scenarios = []

    def conduct_experiment(self):
        self.prepare_experiment()
        automated_test_steps_GT, traced_requirements_GT, automated_test_steps_S, traced_requirements_S = self.run_experiment()
        self.visualize_experiment(
            automated_test_steps_GT, traced_requirements_GT, automated_test_steps_S, traced_requirements_S)

    def prepare_experiment(self):
        from data_container import ModelDataReader
        get_files = ModelDataReader.get_files

        test_scenarios_dir_path = "../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/"
        test_scenarios_files = get_files(test_scenarios_dir_path, ".xlsx")

        for path in test_scenarios_files:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_container import ModelDataReader
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
        req_names = read_excel(path, "Reqs", "Linked Req Description", 0)

        return EvaluationTestScenario(tid, title, description, step_ids, step_descriptions, step_expected_results,
                                      step_test_blocks_names, step_test_block_params_n_vals, req_ids, req_names)

    def run_experiment(self):
        automated_test_steps_GT = []
        traced_requirements_GT = []
        automated_test_steps_S = []
        traced_requirements_S = []

        block_id = self.rec.data.test_blocks_names.index

        for test_scenario in self.test_scenarios:
            print(test_scenario.title)
            reqs_GT = [req.id for req in test_scenario.reqs_GT]
            reqs_R = self.rec.recommend_reqs_by_id(
                test_scenario, N=15, method='avg')
            print("reqs_GT", reqs_GT)
            print("reqs_R", reqs_R)

            reqs_count = 0
            for req_GT in reqs_GT:
                if req_GT in reqs_R:
                    reqs_count += 1

            print(reqs_count)

            blocks_count = 0
            for i, test_step in enumerate(test_scenario.steps):
                blocks_R = self.rec.find_top_blocks(
                    test_step.description, N=15, method='avg', text_weight=0.9, param_weight=0.1)
                block_GT = block_id(test_scenario.blocks_GT[i][0].name)

                if block_GT in blocks_R:
                    blocks_count += 1

            automated_test_steps_GT.append(len(test_scenario.steps))
            traced_requirements_GT.append(len(reqs_GT))
            automated_test_steps_S.append(blocks_count)
            traced_requirements_S.append(reqs_count)

        return (automated_test_steps_GT, traced_requirements_GT, automated_test_steps_S, traced_requirements_S)

    def visualize_experiment(self, automated_test_steps_GT, traced_requirements_GT, automated_test_steps_S, traced_requirements_S):
        test_list = list(range(len(self.test_scenarios)))
        experiment_test_coverage(test_list, automated_test_steps_GT,
                                 traced_requirements_GT, automated_test_steps_S, traced_requirements_S)
