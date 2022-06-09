import os
from ai_framework.ai_actions import AIaction


# todo add a context here
# create a test action template that will be used by all tests
class TestAction(AIaction):
    def __init__(self, server=os.environ['ai_server'], port=os.environ['ai_server_port'], preconditions={}, effects={}):
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)
        self._context = {"TestContext": True}

    def behavior(self):
        pass


# use the test action template to create an action for a goal state unknown to the ai's world
class UnheardOfTestAction(TestAction):
    def behavior(self):
        new_context = {"NewContext": True}
        self.update_context(new_context)


def launch_un_heard_of_ai_actions():
    # build the un-heard of action
    preconditions = {"pursue_the_un_heard_of": False}
    effects = {"pursue_the_un_heard_of": True}
    UnheardOfTestAction(preconditions=preconditions, effects=effects)


if __name__ == "__main__":
    launch_un_heard_of_ai_actions()
