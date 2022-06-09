import os
from ai_framework.ai_actions import AIaction
from threading import Thread


# create a test action template that will be used by all tests
class TestAction(AIaction):
    def __init__(self, server=os.environ['ai_server'], port=os.environ['ai_server_port'], preconditions={}, effects={}):
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        pass


# use the test action template to create an action that unregisters itself
class UnregisterTestAction(TestAction):
    _first_this_action_was_called = True

    def behavior(self):
        # on the first run of this action, report a failure so that the action will be called again
        if self._first_this_action_was_called:
            self.actual_effects["run_unregister_action"] = False
            self._first_this_action_was_called = False
        # on the second run of this action, unregister the action
        else:
            self._unregister()


def launch_unregistering_ai_actions():
    # register self-removing actions
    preconditions = {"run_unregister_action": False}
    effects = {"run_unregister_action": True}
    UnregisterTestAction(preconditions=preconditions, effects=effects)


if __name__ == "__main__":
    launch_unregistering_ai_actions()
