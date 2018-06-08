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
        
class TestScenario:
    """Args:
            title (str): Test scenario title.
            description (str): Test scenario description.
            steps (:obj:'list' of :obj:'TestStep'): Test scenario steps. 
    """
    def __init__(self, title, description, steps):
        self.title = title
        self.description = description
        self.steps = steps

class EvaluationTestScenario(TestScenario):
    """Args:
            blocks_GT (:obj:'list' of :obj:'list' of :obj:'TestBlock'): Test scenario blocks. Multiple test blocks can implement one test step.
            reqs_GT (:obj:'list' of :obj:'int'): Requirement ids traced to this test scenario.
    """
    def __init__(self, title, description, steps, blocks_GT, reqs_GT):
        TestScenario.__init__(self, title, description, steps)
        self.blocks_GT = blocks_GT
        self.reqs_GT = reqs_GT
