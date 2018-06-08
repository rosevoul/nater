from timeit import default_timer as timer
from recommender import Recommender
from data_structures import *

class ExperimentII:
    def __init__(self, path, model):
        self.rec = Recommender(path, model)        
        self.test_scenarios = []
    
    def conduct_experiment(self, k=20):
        self.prepare_experiment()
        test_steps, test_blocks_GT, method_blocks_R = self.run_experiment()
        self.visualize_experiment(test_steps, test_blocks_GT, method_blocks_R)

    def prepare_experiment(self):
        test_scenarios_path = ["../data/advanced/evaluation_experiments/implemented_test_cases/experiments_test_scenarios/atomic/CNFD_014_1.xlsx"]
        for path in test_scenarios_path:
            test_scenario = self.load_evaluation_test_scenario(path)
            self.test_scenarios.append(test_scenario)

    def load_evaluation_test_scenario(self, path):
        from ast import literal_eval
        from data_reading import ModelDataReader
        read_excel = ModelDataReader.read_excel
        
        step_ids = read_excel(path, "Steps_n_Reqs_Simple", "Step ID", 5)
        step_descriptions = read_excel(path, "Steps_n_Reqs_Simple", "Step Description", 5)
        step_expected_results = read_excel(path, "Steps_n_Reqs_Simple", "Expected Result", 5)
        step_test_blocks_names = read_excel(path, "Steps_n_Reqs_Simple", "Test Block Name", 5)
        step_test_block_params_n_vals = read_excel(path, "Steps_n_Reqs_Simple", "Test Block Parameters", 5)

        steps = []
        blocks = []
        N = max((int(sid) for sid in step_ids))

        i = 0
        while len(steps) < N:
            ts = TestStep(i, step_descriptions[i], step_expected_results[i])
            steps.append(ts)

            M = step_ids.count(str(len(steps)))
            step_blocks = []
            for j in range(M):
                tb = TestBlock(step_test_blocks_names[i + j], dict(literal_eval(step_test_block_params_n_vals[i + j])))
                step_blocks.append(tb)
            blocks.append(step_blocks)
            i = i + M

        return EvaluationTestScenario("Title", "Description", steps, blocks, []) 

    def run_experiment(self, k=20):
        method_blocks_R = {}
        
        all_test_steps = [step for scenario in self.test_scenarios for step in scenario.steps]
        
        for method in ["avg", "sta", "tf-idf", "jac", "lsi"]:
            test_blocks_R = []
            for test_step in all_test_steps:
                test_blocks_R.append(self.rec.find_top_blocks(test_step.description, k, method))
            method_blocks_R[method] = test_blocks_R
        
        test_steps = [step.id for scenario in self.test_scenarios for step in scenario.steps]
        block_id = self.rec.data.test_blocks_names.index
        test_blocks_GT = [block_id(block[0].name) for scenario in self.test_scenarios for block in scenario.blocks_GT] 
        
        return test_steps, test_blocks_GT, method_blocks_R
    
    def visualize_experiment(self, test_steps, test_blocks_GT, method_blocks_R):
        from experiments_visualization import experiment_2a, experiment_2b
        print("Experiment 2a, k = 1")
        experiment_2a(1, test_steps, test_blocks_GT, method_blocks_R)
        print("Experiment 2a, k = 5")
        experiment_2a(5, test_steps, test_blocks_GT, method_blocks_R)
        print("Experiment 2a, k = 10")
        experiment_2a(10, test_steps, test_blocks_GT, method_blocks_R)
        print("Experiment 2b")
        experiment_2b(test_steps, test_blocks_GT,  method_blocks_R)
