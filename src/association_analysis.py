import pandas as pd
from orangecontrib.associate.fpgrowth import *  

class AssociationAnalysis(object):
    """Perform Association Analysis on test block diagrams with tree structure"""
    def __init__(self, implemented_tests, test_blocks, human_blocks, human_blocks_children, path):
        self.implemented_tests = implemented_tests
        self.test_blocks = test_blocks
        self.human_blocks = human_blocks
        self.human_blocks_children = human_blocks
        self.path = path
    
    def associate_blocks(self):
        assoc_sets_names, assoc_sets_occur = self.associate(self.preprocess_blocks())

        return assoc_sets_names

        # # Compare association sets with children lists
        # occurences = []
        # indices = []

        # for i, children in enumerate(self.human_blocks_children):
        #     for j, pair in enumerate(assoc_sets_names):
        #         if set(children) == set(pair):
        #             occurences.append(assoc_sets_occur[j])
        #             indices.append(i)
        
        # # Find the chunk of the children that matched with sets based on indices
        # assoc_result = self.human_blocks.iloc[indices]
        # # Add a column of occurences
        # assoc_result["occurrences"] = occurences
        # assoc_result = assoc_result.drop_duplicates(subset=['name'])
        # assoc_result = assoc_result.reset_index(drop=True)
        # assoc_result = assoc_result.sort_values(by=['occurrences'], ascending=False)
        # assoc_result.to_csv("matches_result.csv")

        # return assoc_result

    def preprocess_blocks(self):
        # Iterate through the tests and find the sets of blocks
        all_named_sets = []
        for test_csv in self.implemented_tests:
            test = pd.read_csv(test_csv)
            groups = dict(tuple(test.groupby('testcase')))
            
            for testcase, df in groups.items():
                test_sets = self.assign_name(self.find_sets(df), df)
                all_named_sets.extend(test_sets)

        # Index using the test blocks' names
        index_sets = self.assign_id(all_named_sets, self.test_blocks)
        clean_index_sets = self.cleanup(index_sets)

        return clean_index_sets
            
    def associate(self, sets):
        # Find the combinations that appear more than 2 times
        itemsets = frequent_itemsets(sets, 2)

        # Discard one-element combinations and sort based on number of occurences
        combs = [item for item in list(itemsets) if len(item[0]) > 1]
        sorted_sets = sorted(combs, key=lambda x: x[1], reverse=True)
        sets_list = [list(x[0]) for x in sorted_sets]
        occur_list = [x[1] for x in sorted_sets]

        named_sets = self.reassign_name(self.test_blocks, sets_list)

        # Save in dataframe
        associations = pd.DataFrame({'names': named_sets, 'occurences': occur_list, 'indices': sets_list})
        associations.to_csv(self.path + "/tmp/associations.csv")

        return (named_sets, occur_list)

    @staticmethod
    def find_sets(df):
        # Create list of items of the same depth
        test_tree = df[["depth", "step_id"]]
        max_depth = test_tree["depth"].max()

        sets = []
        for i in range(max_depth):
            current_depth_steps = test_tree.loc[test_tree['depth'] == i + 1]
            # For each depth, create sublists of the ids with the same parent
            steps_list = current_depth_steps["step_id"].tolist()
            
            parents_list = []
            for step in steps_list:
                parent_step = step[:-1]
                if parent_step not in parents_list:
                    parents_list.append(parent_step)
                    step_sets = [s for s in steps_list if s.startswith(parent_step)]
                    if len(step_sets) != 1:
                        sets.append(step_sets)
        
        return sets

    @staticmethod
    def assign_name(sets, df):
        named_sets = []
        for pair in sets:
            named_pair = []
            for step_id in pair:
                name = df[df['step_id'] == step_id]['name']
                named_pair.append(name.item())
            named_sets.append(named_pair)
        
        return named_sets

    @staticmethod   
    def reassign_name(test_blocks, idx_sets):
        name_sets = []
        for pair in idx_sets:
            single_pair = []
            for idx in pair:
                name = test_blocks["name"][idx]
                single_pair.append(name)
            name_sets.append(single_pair)
        
        return name_sets

    @staticmethod
    def assign_id(named_sets, test_blocks):
        index_sets = []
        for pair in named_sets:
            index_pair = []
            for name in pair:
                index = test_blocks.index[test_blocks['name'] == name].tolist()
                index_pair.append(index)
            index_sets.append(index_pair)

        return index_sets

    @staticmethod
    def cleanup(index_sets):

        clean_index_sets = []
        for pair in index_sets:
            pair = [index[0] for index in pair if len(index) == 1]
            clean_index_sets.append(pair)
            
        clean_index_sets = [p for p in clean_index_sets if len(p) >= 2]
        
        return clean_index_sets
