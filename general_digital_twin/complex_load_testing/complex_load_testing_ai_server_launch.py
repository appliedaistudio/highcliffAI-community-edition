import json
from ai_framework.ai_server import start_ai_server


def _build_ai_server_goals_list_json_file(num_goals):
    with open('config/complex_load_testing_ai_goals_list.json', 'w') as f:
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
        goals_list.append(failed_action_goal)

        # create a goal to test an action that unregisters itself
        unregister_action_goal = {
            'goal_state_name': "run_unregister_action",
            'goal_state_value': True,
            'criticality': 0.4,
            'time_sensitivity': 0.4
        }
        goals_list.append(unregister_action_goal)

        # create a goal to test an unachievable goal
        unachievable_goal = {
            'goal_state_name': "pursue_the_unachievable",
            'goal_state_value': True,
            'criticality': 0.5,
            'time_sensitivity': 0.5
        }
        goals_list.append(unachievable_goal)

        # create a goal to test an un-heard-of goal
        un_heard_of_goal = {
            'goal_state_name': "pursue_the_un_heard_of",
            'goal_state_value': True,
            'criticality': 0.3,
            'time_sensitivity': 0.3
        }
        goals_list.append(un_heard_of_goal)

        # convert the goals dictionary into pretty-printed json and write to file
        goals_json = json.dumps(goals_list, indent=4)
        f.write(goals_json)


def _build_initial_world_state_json_file(num_goals):
    with open('config/complex_load_testing_initial_world_state.json', 'w') as f:
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

        # convert the state's dictionary into pretty-printed json and write to file
        initial_world_state_json = json.dumps(initial_world_state, indent=4)
        f.write(initial_world_state_json)


def launch_ai_server() -> None:
    # build the required initialization and configuration files
    num_load_test_goals = 1
    _build_ai_server_goals_list_json_file(num_load_test_goals)
    _build_initial_world_state_json_file(num_load_test_goals)

    # start the ai server, this is blocking and should be the last command in this method
    start_ai_server("config/complex_load_testing_ai_server_config.ini")


if __name__ == "__main__":
    launch_ai_server()
