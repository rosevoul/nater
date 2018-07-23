class TestBlock:
    """Each test block consists of a name and a list of parameters with their values.
    Args:
        name (str): Name of a test block. 
        params_n_vals ('dict'): Parameters and values of a test block.
                dict containing:
                * param (str): Name of a test block parameter.
                * val (str): Value of a test block parameter.
    """

    def __init__(self, name, params_n_vals):
        self.name = name
        self.params_n_vals = params_n_vals


class TestStep:
    """ Each test step consists of a description and an expected result.
    Args:
        description (str): Description of a test scenario step. 
        expected_result (str): Expected result of a test scenario step.
    """

    def __init__(self, sid, description, expected_result):
        self.id = sid
        self.description = description
        self.expected_result = expected_result


class Requirement:

    def __init__(self, rid, name):
        self.id = rid
        self.name = name


class TestScenario:
    """Args:
            id (int): Test scenario id.
            title (str): Test scenario title.
            description (str): Test scenario description.
            steps (:obj:'list' of :obj:'TestStep'): Test scenario steps. 
    """

    def __init__(self, tid, title, description, step_ids, step_descriptions, step_expected_results, order='important'):
        self.id = tid
        self.title = title
        self.description = description
        self.steps = []
        self.steps = self.read_steps(
            step_ids, step_descriptions, step_expected_results, order)

    def read_steps(self, step_ids, step_descriptions, step_expected_results, order):
        steps = []
        N = max((int(sid) for sid in step_ids))

        if order == 'important':
            for i in range(N):
                ts = TestStep(i, step_descriptions[
                              i], step_expected_results[i])
                steps.append(ts)
        else:
            for i in range(len(step_descriptions)):
                ts = TestStep(i, step_descriptions[
                              i], step_expected_results[i])
                steps.append(ts)

        return steps


class EvaluationTestScenario(TestScenario):
    """Args:
            blocks_GT (:obj:'list' of :obj:'list' of :obj:'TestBlock'): Test scenario blocks. Multiple test blocks can implement one test step.
            reqs_GT (:obj:'list' of :obj:'int'): Requirement ids traced to this test scenario.
    """

    def __init__(self, tid, title, description, step_ids, step_descriptions, step_expected_results, step_test_blocks_names, step_test_block_params_n_vals, req_ids, req_names, order='important'):
        TestScenario.__init__(self, tid, title, description,
                              step_ids, step_descriptions, step_expected_results, order)

        self.blocks_GT = []
        self.reqs_GT = []

        self.blocks_GT = self.read_blocks(
            step_ids, step_test_blocks_names, step_test_block_params_n_vals)
        self.reqs_GT = self.read_reqs(req_ids, req_names)

    def read_blocks(self, step_ids, step_test_blocks_names, step_test_block_params_n_vals):
        from ast import literal_eval

        steps = []
        blocks = []
        N = max((int(sid) for sid in step_ids))

        i = 0
        for s in range(N):
            M = step_ids.count(str(s + 1))
            current_step_blocks = []
            for j in range(M):
                tb = TestBlock(step_test_blocks_names[
                               i + j], dict(literal_eval(step_test_block_params_n_vals[i + j])))
                current_step_blocks.append(tb)
            blocks.append(current_step_blocks)
            i = i + M

        return blocks

    def read_reqs(self, req_ids, req_names):
        reqs_GT = []

        for i in range(len(req_ids)):
            reqs_GT.append(Requirement(req_ids[i], req_names[i]))

        return reqs_GT
