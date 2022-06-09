__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# AI, GOAP

# needed to copy the intended effects into the actual effects
import copy
# needed to keep the action alive in its thread
import time
# defines action status
from enum import Enum
from threading import Thread

# needed to connect to the remote server
import rpyc
from goap.action import Action

# needed for context validation
from ai_framework.ai_context import is_validate_context


class AIConnectionLost(Exception):
    pass


class AIaction(Action):

    def __init__(self, preconditions={}, initial_effects={}, server="localhost", port=12345):
        # the preconditions for using this action
        self.preconditions = preconditions

        # the intended effect of the action on the world
        self.effects = initial_effects

        # the actual effect of the action on the world
        self.actual_effects = None

        # the data context under which this action occurs
        self._context = {}

        # create a connection to the remote ai
        self._connection = rpyc.connect(server,
                                        port,
                                        config={"allow_all_attrs": True,
                                                "allow_public_attrs": True,
                                                "allow_setattr": True,
                                                "instantiate_custom_exceptions": True,
                                                "import_custom_exceptions": True,
                                                "sync_request_timeout": None,
                                                "allow_pickle": True
                                                })

        # create a connection to the network resources
        self._network = self._connection.root.network()

        # note: the following must be done as last parts of initialization

        # create and register a remote action
        try:
            self._connection.root.add_action(self)

        except:
            # if the connection to the ai server is lost. retry the connection until re-established
            while True:
                try:
                    print("reconnecting")
                    self._connection = rpyc.connect(server,
                                                    port,
                                                    config={"allow_all_attrs": True,
                                                            "allow_public_attrs": True,
                                                            "allow_setattr": True,
                                                            "instantiate_custom_exceptions": True,
                                                            "import_custom_exceptions": True,
                                                            "sync_request_timeout": None,
                                                            "allow_pickle": True
                                                            })

                    # re-create a connection to the network resources
                    self._network = self._connection.root.network()

                    # register with the ai once the connection is re-established
                    self._connection.root.add_action(self)
                    print("reconnected")
                    break
                except:
                    continue

        # keep the action alive while still able to process incoming requests from the AI
        thread = Thread(target=self._stay_alive)
        thread.start()

    @staticmethod
    def _stay_alive():
        # keep the action alive in its thread
        while True:
            time.sleep(5)

    @staticmethod
    def check_connection():
        # lets the ai server know that the connection to this action is still active
        # this method does not need to perform any action. it needs only execute
        pass

    def update_the_world(self, state_name, state_value, context):
        # update the world state
        # todo this fails when there is a break in connection. how to handle the failure?
        try:
            self._network.update_the_world(state_name, state_value, context)
        except:
            raise AIConnectionLost

    def act(self):
        # assume that the act will have the intended effect
        self.actual_effects = copy.copy(self.effects)

        # every AI action runs custom behavior. this behavior may change the actual effects
        self.behavior()

        # build a world event then update the world with that new world event
        if self.actual_effects == {}:
            new_world_event_state_name = ""
            new_world_event_state_value = True
            self.update_the_world(new_world_event_state_name, new_world_event_state_value, self._context)
        else:
            # step through the actual effects and update the world with each actual effect listed
            new_world_event_state_names = list(self.actual_effects.keys())
            for new_world_event_state_name in new_world_event_state_names:
                new_world_event_state_value = self.actual_effects[new_world_event_state_name]
                self.update_the_world(new_world_event_state_name, new_world_event_state_value, self._context)

    def _unregister(self):
        # unregisters the action from the ai server
        self._connection.root.remove_action(self)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def context(self):
        return self._context

    def update_context(self, new_context):
        if is_validate_context(new_context):
            self._context = new_context


class ActionStatus(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
