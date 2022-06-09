__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to read the environment variables
import os

# needed to run the ai
from ai_framework.ai import AI

# needed to run the ai as a remote server
import rpyc

# needed to start the server in its own thread
from rpyc.utils.server import ThreadedServer

# needed to keep the registered action thread alive
import time

# needed to run the ai as a remote server in its own thread
import threading

# needed to read goals from a file
import json

# needed to demo the ai server functionality
from ai_framework.ai_visualization import AIDemo

# needed to read server configuration from the config file
from configparser import ConfigParser

# needed to populate the initial world state

# the global server configuration file
# this is implemented as a global variable rather than one passed into the main function
# because the rpyc.Server class does not allow overwriting of the constructor. this is
# a workaround to that limitation
config = ConfigParser()

ai = AI()


class AIServer(rpyc.Service):
    _server_started = False

    def _init_server(self):
        # connect to the ai
        global ai
        self._ai = ai

        global config
        self._seconds_to_sleep_between_ai_runs = float(config['server_execution']['seconds_to_sleep_between_ai_runs'])
        self._node_retirement_age_in_seconds = int(config["demo"]["seconds_to_wait_before_no_longer_displaying_a_node"])

        # create initial parameters for demo visualization
        demo_markdown_file_folder = config['demo']['demo_markdown_file_folder']
        demo_mode = config['demo']['demo_mode'] == "True"
        self._ai_demo = AIDemo(demo_mode=demo_mode, markdown_folder=demo_markdown_file_folder)
        self._ai_demo.reset_demo()

        # read the ai goals from file and set
        ai_goal_list_json_file = config['server_execution']['ai_goal_list_json_file']
        with open(ai_goal_list_json_file) as json_file:
            file_formatted_ai_goal_list = json.load(json_file)
        self._ai.set_goals(file_formatted_ai_goal_list)

        # demo the ai goals
        self._ai_demo.demo_goals(file_formatted_ai_goal_list)

        # set the initial state of the world if directed to do so by the configuration file
        set_initial_world_state = config['server_execution']['set_initial_world_state']
        if set_initial_world_state:
            initial_world_state_json_file = config['server_execution']['initial_world_state_json_file']
            with open(initial_world_state_json_file) as json_file:
                # read the world states from the initial world state file
                initial_world_state = json.load(json_file)
                world_state_names = initial_world_state.keys()

                # update the world based on each of the world states from the world state file
                for world_state_name in world_state_names:
                    # create an event from the world state file
                    world_state_value = initial_world_state[world_state_name]
                    no_context = {}

                    # write the event to the world
                    self._ai.network().update_the_world(world_state_name, world_state_value, no_context)

    def on_connect(self, conn):
        # start the server after the first connection
        if not self._server_started:
            self._init_server()
            thread = threading.Thread(target=self._run_ai)
            thread.start()
        self._server_started = True

    def _run_ai(self):
        while True:
            self._ai.run_iteration()

            # run the demo by visualizing the last entry from the ai diary
            last_diary_entry = -1
            diary_entry = self._ai.diary()[last_diary_entry]
            self._ai_demo.demo_diary_entry(diary_entry)
            self._ai_demo.update_demo_goals(diary_entry)

            # tell the visualization when to no longer visualize a node
            # todo remove the node retirement age from the server config settings
            self._ai_demo.retire_nodes(self._ai.network().the_world_states())

            # wait before the next ai run
            time.sleep(self._seconds_to_sleep_between_ai_runs)

    def on_disconnect(self, conn):
        pass

    def exposed_add_action(self, action):
        self._ai.add_capability(action)

        # this server runs each request as a separate thread.
        # the thread must be kept alive to keep the reference to the action valid.
        while True:
            time.sleep(5)

    def exposed_remove_action(self, action):
        self._ai.remove_capability(action)

    def exposed_reset(self):
        # return the running server to a clean state
        self._ai.reset()

    def exposed_network(self):
        # return a reference to the AI's network resources
        return self._ai.network()

    def exposed_ai_diary(self):
        # return the contents of the ai diary
        return self._ai.diary()


def start_ai_server(ai_instance=AI(), ai_server_config_file="ai_server_config.ini"):
    # set the ai instance
    global ai
    ai = ai_instance

    # initiate the configuration file
    global config
    config = ConfigParser()
    config.read(ai_server_config_file)

    allow_all_attrs = config['server_protocol']['allow_all_attrs'] == "True"
    allow_public_attrs = config['server_protocol']['allow_public_attrs'] == "True"
    allow_setattr = config['server_protocol']['allow_setattr'] == "True"
    instantiate_custom_exceptions = config['server_protocol']['instantiate_custom_exceptions'] == "True"
    import_custom_exceptions = config['server_protocol']['import_custom_exceptions'] == "True"
    allow_pickle = config['server_protocol']['allow_pickle'] == "True"

    # start the server
    thread = ThreadedServer(AIServer(),
                            port=os.environ['ai_server_port'],
                            protocol_config={"allow_all_attrs": allow_all_attrs,
                                             "allow_public_attrs": allow_public_attrs,
                                             "allow_setattr": allow_setattr,
                                             "instantiate_custom_exceptions": instantiate_custom_exceptions,
                                             "import_custom_exceptions": import_custom_exceptions,
                                             "allow_pickle": allow_pickle
                                             }
                            )
    thread.start()


if __name__ == "__main__":
    start_ai_server()
