import os
from ai_framework.ai_actions import AIaction
from threading import Thread


# create a test action template that will be used by all tests
class TestAction(AIaction):
    def __init__(self, server=os.environ['ai_server'], port=os.environ['ai_server_port'], preconditions={}, effects={}):
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        pass


def launch_load_testing_ai_actions(num_load_test_actions):
    # register load-testing actions in daemon threads
    for n in range(num_load_test_actions):
        preconditions = {f"goal_{n}_achieved": False}
        effects = {f"goal_{n}_achieved": True}
        test_action_thread = Thread(target=TestAction, kwargs={"preconditions": preconditions, "effects": effects})
        test_action_thread.start()


if __name__ == "__main__":
    load_test_actions = 1
    launch_load_testing_ai_actions(load_test_actions)
