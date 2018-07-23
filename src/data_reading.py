import os
import docx
import pandas as pd


class DataReader(object):
    """Read the necessary data from various sources related to the Test Routine Automation."""

    def __init__(self, path):
        self.path = path
        self.test_blocks_names, self.test_blocks_descriptions,  self.test_blocks_preconditions, \
            self.test_blocks_postconditions, self.test_blocks_parameters = self.read_test_blocks()
        self.reqs_ids, self.reqs_names, self.reqs_descriptions, \
            self.reqs_cover_statuses = self.read_requirements()
        self.entities = self.read_entities()
        self.aliases = self.read_aliases()

    def read_test_blocks(self):
        """Read extracted descriptions from machine -high level- test blocks (CSV file) """
        test_blocks_file_path = os.path.join(
            self.path, "parsed/test-blocks/machine_blocks_corrected.csv")
        test_blocks_info = pd.read_csv(test_blocks_file_path)
        test_blocks_info = test_blocks_info.fillna('')
        test_blocks_names = test_blocks_info["name"].tolist()
        test_blocks_descriptions = test_blocks_info["description"].tolist()
        test_blocks_preconditions = test_blocks_info["precondition"].tolist()
        test_blocks_postconditions = test_blocks_info["postcondition"].tolist()
        test_blocks_parameters = test_blocks_info["parameters"].tolist()

        return (test_blocks_names, test_blocks_descriptions, test_blocks_preconditions,
                test_blocks_postconditions, test_blocks_parameters)

    def read_requirements(self):
        """Read requirements from various systems and applications (CSV file) """
        reqs_file_path = os.path.join(
            self.path, "parsed/requirements.csv")
        reqs_info = pd.read_csv(reqs_file_path)
        reqs_info = reqs_info.fillna('')
        reqs_ids = reqs_info["req_id"].tolist()
        reqs_names = reqs_info["name"].tolist()
        reqs_descriptions = reqs_info["description"].tolist()
        reqs_cover_statuses = reqs_info["cover_status"].tolist()

        return (reqs_ids, reqs_names, reqs_descriptions, reqs_cover_statuses)

    def read_entities(self):
        entities_path = os.path.join(self.path, "parsed/entities.csv")
        entities = pd.read_csv(entities_path)
        parameters = entities['Parameters'].tolist()
        applications = entities['Applications'].dropna().tolist()
        systems = entities['Systems'].dropna().tolist()

        return (parameters, applications, systems)

    def read_aliases(self):
        aliases_path = os.path.join(self.path, "parsed/aliases.csv")
        aliases_info = pd.read_csv(aliases_path)
        aliases = aliases_info['Alias'].tolist()
        names = aliases_info['Name'].tolist()

        return (aliases, names)


class ModelDataReader(DataReader):
    """Read the necessary data from various sources related to the Test Automation."""

    def __init__(self, path):
        super().__init__(path)
        self.docs = self.read_docs()
        self.test_steps = self.read_test_steps()
        self.implemented_tests = self.read_implemented_tests()
        self.correct_spelled_data = self.read_correct_spelled_data()

    def read_docs(self):
        implemented_test_scenarios_file_path = os.path.join(
            self.path, "implemented-test-scenarios/TESTS.xlsx")
        test_scenarios_dir_path = os.path.join(
            self.path, "test-scenarios-reqs-coverage")
        reqs_dir_path = os.path.join(self.path, "reqs")
        documentation_dir_path = os.path.join(self.path, "documentation")

        # Read data from Implemented test scenarios
        implemented_test_scenarios_files_dict = pd.read_excel(
            implemented_test_scenarios_file_path, sheet_name=None, usecols=0)
        implemented_test_scenarios_files = list(
            implemented_test_scenarios_files_dict.keys())
        implemented_test_scenarios_files = [
            f for f in implemented_test_scenarios_files[4:] if f != "REDUNDANCY_CONCEPT"]

        implemented_test_scenarios_info = []
        for file in implemented_test_scenarios_files:
            implemented_test_scenarios_info.extend(self.read_excel(
                implemented_test_scenarios_file_path, file, 1, None))
            implemented_test_scenarios_info.extend(self.read_excel(
                implemented_test_scenarios_file_path, file, 2, None))
            implemented_test_scenarios_info.extend(self.read_excel(
                implemented_test_scenarios_file_path, file, 3, None))

        print("Implemented test scenarios files... Done.")

        # Read data from Test scenarios (Excel files)
        test_scenarios_info = []
        test_scenarios_files = self.get_files(test_scenarios_dir_path, ".xlsx")

        for file in test_scenarios_files:
            test_scenarios_info.extend(self.read_excel(
                file, "Requirements", "Req Name", 1))
            test_scenarios_info.extend(self.read_excel(
                file, "Requirements", "Description", 1))
            test_scenarios_info.extend(self.read_excel(
                file, "Test Design Steps", "Test Design Step Name", 1))
            test_scenarios_info.extend(self.read_excel(
                file, "Test Design Steps", "Test Name", 1))
            test_scenarios_info.extend(self.read_excel(
                file, "Test Design Steps", "Test Design Description", 1))
            test_scenarios_info.extend(self.read_excel(
                file, "Test Design Steps", "Test Design Expected Result", 1))

        print("Test scenarios files...", len(test_scenarios_files))

        # Read data from Requirements (Excel files)
        reqs_info = []
        reqs_files = self.get_files(reqs_dir_path, ".xlsx")

        for file in reqs_files:
            reqs_info.extend(
                self.read_excel(file, "Sheet1", "Description"))

        print("Requirements files...", len(reqs_files))

        # Read data from Software Documentation (Word files)
        documentation_info = []
        documentation_files = self.get_files(
            documentation_dir_path, ".docx", include_subdirs=True)

        for file in documentation_files:
            documentation_info.extend(self.read_word(file))
        print("Documentation files...", len(documentation_files))

        # Merge data
        docs = []
        docs.extend(implemented_test_scenarios_info)
        docs.extend(test_scenarios_info)
        docs.extend(reqs_info)
        docs.extend(documentation_info)

        return docs

    def read_test_steps(self):
        scenarios_dir_path = os.path.join(self.path, "evaluation")
        file = scenarios_dir_path + "/TestScenariosWithSteps.xlsx"

        test_steps = []
        test_steps.extend(self.read_excel(
            file, "Test Design Steps", "Test Design Description", 1))

        return test_steps

    def read_implemented_tests(self):
        implemented_tests_path = os.path.join(
            self.path, "parsed/implemented-tests")
        implemented_tests = self.get_files(implemented_tests_path, ".csv")

        return implemented_tests

    def read_correct_spelled_data(self):
        sum_documents_dir_path = os.path.join(self.path, "sum_docs")
        correct_spelled_data = []
        sum_documents = self.get_files(sum_documents_dir_path, ".docx")
        for file in sum_documents:
            correct_spelled_data.extend(self.read_word(file))
        print("Correct spelled data... Done.")

        return correct_spelled_data

    @staticmethod
    def read_excel(file, sheet, column, header_row=0):
        excel_infoframe = pd.read_excel(
            file, sheet_name=sheet, header=header_row).astype(str)
        text_list = excel_infoframe[column].values.tolist()

        return text_list

    @staticmethod
    def read_word(file):
        doc = docx.Document(file)
        text_list = []
        for par in doc.paragraphs:
            text_list.append(par.text)

        return text_list

    @staticmethod
    def get_files(dir_path, file_extension, include_subdirs=False):

        if include_subdirs:
            files = [os.path.join(root, name)
                     for root, dirs, files in os.walk(dir_path)
                     for name in files
                     if name.endswith((file_extension))]
        else:
            files = [os.path.join(dir_path, f) for f in os.listdir(
                dir_path) if f.endswith(file_extension)]

        return files
