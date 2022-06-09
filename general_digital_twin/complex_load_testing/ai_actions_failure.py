import os

from ai_framework.ai_actions import AIaction


# create a test action template that will be used by all tests
class TestAction(AIaction):
    def __init__(self, server=os.environ['ai_server'], port=os.environ['ai_server_port'], preconditions={}, effects={}):
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)
        self._context = {"TestAction": True}

    def behavior(self):
        pass


# use the test action template to create an action that fails
class FailedTestAction(TestAction):
    _num_failures = 0
    _max_num_failures = 2

    def behavior(self):
        # this action should fail only a certain number of times
        self.update_context({"NewContext": True})
        if self._num_failures <= self._max_num_failures:
            self._num_failures += 1
            raise Exception('This is a failed action')


def launch_failing_ai_actions():
    # register failing action
    preconditions = {"run_failed_action": False}
    effects = {"run_failed_action": True}
    FailedTestAction(preconditions=preconditions, effects=effects)


if __name__ == "__main__":
    launch_failing_ai_actions()
