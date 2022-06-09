__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

import os
import time
import unittest

# needed to start up the remote ai server
import rpyc
from ai_framework.ai_server import start_ai_server

# needed to create test actions
from ai_framework.ai_actions import AIaction

# needed to run the ai server in a separate, non-blocking thread
from threading import Thread

# used to format the goal file
import json

# todo: test against invalid goal lists at startup


# create a test action template that will be used by all tests
class TestAction(AIaction):
    def __init__(self, server=os.environ['ai_server'], port=os.environ['ai_server_port'], preconditions={}, effects={}):
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        pass


# use the test action template to create an action that fails
class FailedTestAction(TestAction):
    _num_failures = 0
    _max_num_failures = 2

    def behavior(self):
        # this action should fail only a certain number of times
        if self._num_failures <= self._max_num_failures:
            self._num_failures += 1
            raise Exception('This is a failed action')


# use the test action template to create an action that unregisters itself
class UnregisterTestAction(TestAction):
    _first_this_action_was_called = True

    # todo: what do i do when the actual effects are changed and need to be changed back
    # todo: in the base class, set actual effects equal to intended effects
    def behavior(self):
        # on the first run of this action, report a failure so that the action will be called again
        if self._first_this_action_was_called:
            self.actual_effects["run_unregister_action"] = False
            self._first_this_action_was_called = False
        # on the second run of this action, unregister the action
        else:
            self._unregister()


# use the test action template to create an action for a goal state unknown to the ai's world
class UnheardOfTestAction(TestAction):
    def behavior(self):
        pass


class TestAI(unittest.TestCase):

    @staticmethod
    def _build_ai_server_goals_list_json_file(num_goals):
        with open('../../general_digital_twin/complex_load_testing/config/complex_load_testing_ai_goals_list.json', 'w') as f:
            # create a batch of goals designed to stress test the ai server
            goals_list = []
            for n in range(num_goals):
                # write and collect the goals into a dictionary
                goal = {
                    'goal_state_name': f"goal_{n}_achieved",
                    'goal_state_value': True,
                    'criticality': 0.1,
                    'time_sensitivity': 0.1
                }
                goals_list.append(goal)

            # create a goal to test failed actions
            failed_action_goal = {
                'goal_state_name': "run_failed_action",
                'goal_state_value': True,
                'criticality': 0.1,
                'time_sensitivity': 1
            }
            #goals_list.append(failed_action_goal)

            # create a goal to test an action that unregisters itself
            unregister_action_goal = {
                'goal_state_name': "run_unregister_action",
                'goal_state_value': True,
                'criticality': 0.4,
                'time_sensitivity': 0.4
            }
            #goals_list.append(unregister_action_goal)

            # create a goal to test an unachievable goal
            unachievable_goal = {
                'goal_state_name': "pursue_the_unachievable",
                'goal_state_value': True,
                'criticality': 0.5,
                'time_sensitivity': 0.5
            }
            #goals_list.append(unachievable_goal)

            # create a goal to test an un-heard-of goal
            un_heard_of_goal = {
                'goal_state_name': "pursue_the_un_heard_of",
                'goal_state_value': True,
                'criticality': 0.3,
                'time_sensitivity': 0.3
            }
            #goals_list.append(un_heard_of_goal)

            # convert the goals dictionary into pretty-printed json and write to file
            goals_json = json.dumps(goals_list, indent=4)
            f.write(goals_json)

    @staticmethod
    def _build_initial_world_state_json_file(num_goals):
        with open(
                '../../general_digital_twin/complex_load_testing/config/complex_load_testing_initial_world_state.json', 'w') as f:
            initial_world_state = {}

            # create states designed to prompt the ai to begin stress testing
            for n in range(num_goals):
                initial_world_state[f"goal_{n}_achieved"] = False

            # create a state to test failed actions
            initial_world_state['run_failed_action'] = False

            # create a state to test an action that unregisters itself
            initial_world_state['run_unregister_action'] = False

            # create a goal to test an unachievable goal
            initial_world_state['pursue_the_unachievable'] = False

            # convert the states dictionary into pretty-printed json and write to file
            initial_world_state_json = json.dumps(initial_world_state, indent=4)
            f.write(initial_world_state_json)

    @classmethod
    def setUpClass(cls) -> None:
        # build the required initialization and configuration files
        num_goals = 1
        cls._build_ai_server_goals_list_json_file(num_goals)
        cls._build_initial_world_state_json_file(num_goals)

        # start the ai server in a separate, non-blocking daemon thread
        server_thread = Thread(target=start_ai_server, kwargs={"ai_server_config_file": "complex_load_testing_ai_server_config.ini"})
        server_thread.setDaemon(True)
        server_thread.start()

        port = os.environ['ai_server_port']
        ai_server = os.environ['ai_server']

        # register load-testing actions in daemon threads
        for n in range(num_goals):
            preconditions = {f"goal_{n}_achieved": False}
            effects = {f"goal_{n}_achieved": True}
            test_action_thread = Thread(target=TestAction, kwargs={"preconditions": preconditions, "effects": effects})
            test_action_thread.setDaemon(True)
            test_action_thread.start()

        # register failing action
        preconditions = {"run_failed_action": False}
        effects = {"run_failed_action": True}
        failed_test_action_thread = Thread(target=FailedTestAction,
                                           kwargs={"preconditions": preconditions, "effects": effects})
        failed_test_action_thread.setDaemon(True)
        failed_test_action_thread.start()

        # register self-removing actions
        preconditions = {"run_unregister_action": False}
        effects = {"run_unregister_action": True}
        unregister_test_action_thread = Thread(target=UnregisterTestAction,
                                               kwargs={"preconditions": preconditions, "effects": effects})
        unregister_test_action_thread.setDaemon(True)
        unregister_test_action_thread.start()

        # build the un-heard of action
        preconditions = {"pursue_the_un_heard_of": False}
        effects = {"pursue_the_un_heard_of": True}
        unheard_of_test_action_thread = Thread(target=UnheardOfTestAction,
                                               kwargs={"preconditions": preconditions, "effects": effects})
        unheard_of_test_action_thread.setDaemon(True)
        unheard_of_test_action_thread.start()

        # connect to the ai server and get a copy of the ai's diary
        cls._ai_server_connection = rpyc.connect(ai_server, port)
        cls._ai_diary = cls._ai_server_connection.root.ai_diary()

        # give the ai server time to achieve given objectives
        seconds_to_wait_for_the_ai_server_to_complete_objectives = 60
        time.sleep(seconds_to_wait_for_the_ai_server_to_complete_objectives)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_contents_of_diary(self):
        # make sure the diary has contents as expected
        # test action name and action preconditions
        pass

    def test_large_ai_server_connections(self):
        # create a ton of actions, a ton of goals, and check for a ton of successful diary entries
        pass

    def test_continued_ai_operations_when_an_action_fails(self):
        # the ai should continue to run even when one of the registered actions fails
        pass

    def test_ai_executes_goals_in_priority_order(self):
        # the ai should prioritize goals and execute them in order
        pass

    def test_removing_remote_capability(self):
        # the ai should recognize when an action removes itself
        pass

    def test_not_enough_resources_to_achieve_a_goal(self):
        # if the ai does not have the proper registered resources to achieve a goal
        # it should record that it has no plan for that goal
        pass

    def test_goal_not_already_in_the_world(self):
        # if the ai encounters a goal not already in the world (in some state).
        # it should record that goal as unmet in the world
        pass

    def test_aimless_iterations(self):
        # the ai should be able to handle iterations with no goals
        pass


if __name__ == '__main__':
    unittest.main()
