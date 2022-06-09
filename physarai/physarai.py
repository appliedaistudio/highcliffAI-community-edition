__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# used to create copies of the world state for recording in the AI diary
from copy import copy, deepcopy

# AI, GOAP
from goap.algo.astar import PathNotFoundException
from goap.planner import RegressivePlanner

# PhysarAI inherits from the general AI framework
from ai_framework.ai.ai import AI
from ai_framework.ai_actions import ActionStatus

# used to manage and prioritize goals
from ai_framework.ai_goals import AIGoal

# used to create and access centralized ai_infrastructure
from ai_framework.ai_infrastructure import LocalNetwork

# used to make AI a singleton
from ai_framework.singleton import Singleton


@Singleton
class PhysarAI(AI):
    _network = LocalNetwork.instance()
    _prioritized_goal_list = []
    _capabilities = []
    _diary = []

    def network(self):
        return self._network

    def set_goals(self, goal_list_in_file_format):
        # convert the given list from the file format to a data class format
        goal_list_in_data_class_format = []
        for goal_entry in goal_list_in_file_format:
            goal = AIGoal(
                goal_entry['goal_state_name'],
                goal_entry['goal_state_value'],
                goal_entry['criticality'],
                goal_entry['time_sensitivity']
            )
            goal_list_in_data_class_format.append(goal)

        # sort the goals by priority and store the results
        self._prioritized_goal_list = sorted(goal_list_in_data_class_format, reverse=True)

    def capabilities(self):
        return self._capabilities

    def add_capability(self, action):
        self._capabilities.append(action)

    def remove_capability(self, action):
        # removes a capability
        self.capabilities().remove(action)

    def run_iteration(self):
        # deferring operations of this public function to a private function results in this public
        # function not blocking when called as a distributed service
        self._run_ai_iteration()

    def reset(self):
        self._network.reset()
        self._prioritized_goal_list = None
        self._diary = []
        self._capabilities = []

    def diary(self):
        return self._diary

    def _the_world(self):
        # this function returns the current state of the world
        return self._network.the_world()

    def _state_name_exists_in_the_world(self, state_name):
        # search the world for an event with a state name that matches the one given
        state_name_exists = False
        for world_event in self._the_world():
            if state_name == world_event.world_state_name:
                state_name_exists = True
                break
        return state_name_exists

    def _goal_is_met(self, goal_state_name, goal_state_value):
        # search the world for an event with a state name and value that matches the goal state name and value given
        goal_met = False
        for world_event in self._the_world():
            if goal_state_name == world_event.world_state_name and goal_state_value == world_event.world_state_value:
                goal_met = True
                break
        return goal_met

    def _context(self, world_state_name, world_state_value):
        # search through the world events and find the context whose state name and value matches those given
        context = {}
        for world_event in self._the_world():
            state_name_matches = world_state_name == world_event.world_state_name
            state_value_matches = world_state_value == world_event.world_state_value
            if state_name_matches and state_value_matches:
                context = world_event.context
                break
        return context

    def _select_goal(self):
        # work on the next highest-priority goal that has not yet been met

        # the default is to select no goal and no context
        selected_goal = AIGoal("NONE", True, 0, 0)
        goal_context = {}

        # go through goals in priority order
        for goal in self._prioritized_goal_list:

            goal_is_inactive = goal.deferred
            state_name_is_missing_from_the_world = not self._state_name_exists_in_the_world(goal.goal_state_name)
            goal_is_not_yet_met = not self._goal_is_met(goal.goal_state_name, goal.goal_state_value)

            if goal_is_inactive:
                # the goal has been deferred. skip it
                pass
            elif state_name_is_missing_from_the_world:
                # the goal has no corresponding state in the world. assume the goal is not met, pursue the goal
                goal_not_met = not goal.goal_state_value
                self._network.update_the_world(goal.goal_state_name, goal_not_met, goal_context)
                goal_context = self._context(goal.goal_state_name, goal.goal_state_value)
                selected_goal = goal
                break
            elif goal_is_not_yet_met:
                # the goal has not been met. select it.
                goal_context = self._context(goal.goal_state_name, goal.goal_state_value)
                selected_goal = goal
                break
            else:
                # the goal is already met. skip it
                pass

        return selected_goal, goal_context

    def _reflect(self, prioritized_goals, goal, resource_list, world_state_before,
                 plan, action_name, post_act_context, action_preconditions, action_status, world_state_after):
        diary_entry = {
            "prioritized_goals": prioritized_goals,
            "my_goal": goal,
            "my_resources": resource_list,
            "the_world_state_before": world_state_before,
            "my_plan": plan,
            "action_taken": action_name,
            "post_act_context": post_act_context,
            "action_preconditions": action_preconditions,
            "action_status": action_status,
            "the_world_state_after": world_state_after
        }
        self._diary.append(diary_entry)

    def _check_capability_connections(self):
        # go through the current list of capabilities and confirm that we are still actively connected to each
        confirmed_connected_capabilities_list = []
        for capability in self._capabilities:
            try:
                capability.check_connection()
                confirmed_connected_capabilities_list.append(capability)
            except:
                # when we lose a capability connection,
                # the protocol automatically cleans and clears the reference to the capability
                pass

        # reset the list of capabilities to those with confirmed connections
        self._capabilities = confirmed_connected_capabilities_list

    def _the_world_states(self):
        return self._network.the_world_states()

    def _plan(self, goal):
        # check the connections on all registered capabilities before making any plans
        self._check_capability_connections()

        # if planning still fails because some random capability becomes disconnected,
        # proceed with this round of planning by assuming we have no capabilities
        try:
            planner = RegressivePlanner(self._the_world_states(), self.capabilities())
        except:
            no_capabilities = []
            planner = RegressivePlanner(self._the_world_states(), no_capabilities)

        plan = None

        try:
            # make a plan
            plan = planner.find_plan({goal.goal_state_name: goal.goal_state_value})

        except PathNotFoundException:
            # no viable plan found. no action to be taken
            pass

        except KeyError:
            # there are no registered ai_actions that can satisfy the specified goal. no action to be taken
            pass

        return plan

    @staticmethod
    def _act(plan, goal_context):
        # todo think through restructuring this to make it easier to understand. for example, i don't
        # todo understand why the post-act context has to be in that first try statement
        try:
            # execute the first act in the plan. it will affect the world and get us one step closer to the goal
            # the plan will be updated and ai_actions executed until the goal is reached
            next_action = plan[0].action
            post_act_context = {}
            action_taken = type(next_action).__name__
            action_preconditions = copy(next_action.preconditions)
            intended_effect = copy(next_action.effects)
            try:
                next_action.update_context(goal_context)
                next_action.act()
                post_act_context = next_action.context()
            except:
                # if there is an unknown failure while executing the action, ignore it and move on
                # todo penalize the action with a cost increase if it fails in this way, this is a new kind of ML
                pass

        except IndexError:
            # if the given plan has no ai_actions, then record no action taken,
            # context, preconditions, or intended effect
            action_taken = ""
            action_preconditions = {}
            intended_effect = {}
            post_act_context = {}

        except TypeError:
            # if there is no viable plan, then record no action taken, preconditions or intended effect
            action_taken = ""
            action_preconditions = {}
            intended_effect = {}
            post_act_context = {}

        return action_taken, post_act_context, action_preconditions, intended_effect

    def _resource_list(self):
        # returns a list of registered capabilities useful as resources
        resource_list = []
        for resource in self._capabilities:
            # parse and refine the resource name, then add it to the resource list
            start = '<'
            end = ' object at'
            raw_resource_name = str(resource)
            refined_resource_name = (raw_resource_name.split(start))[1].split(end)[0]
            resource_list.append(refined_resource_name)

        return resource_list

    def _world_state_is_real(self, world_state):
        # a world state is real if it exists in the world

        if world_state == {}:
            world_state_name = ""
            world_state_value = ""
        else:
            world_state_name = list(world_state.keys())[0]
            world_state_value = world_state[world_state_name]

        is_real = False

        # search through the world and look for a world event that matches the given world state name and value
        for world_event in self._the_world():
            state_name_matches = world_state_name == world_event.world_state_name
            state_value_matches = world_state_value == world_event.world_state_value
            if state_name_matches and state_value_matches:
                is_real = True
                break

        return is_real

    def _run_ai_iteration(self):
        # select and pursue a single goal from the internal list of prioritized goals
        selected_goal, goal_context = self._select_goal()

        # take a snapshot of the current world state before taking action that may change it
        world_state_snapshot = copy(self._the_world_states())

        # make a plan
        plan = self._plan(selected_goal)

        # execute the first act in the plan. it will affect the world and get us one step closer to the goal
        # the plan will be updated and ai_actions executed until the goal is reached
        action_taken, post_act_context, action_preconditions, intended_effect = self._act(plan, goal_context)

        # the action is a success if the altered world matches the action's intended effect
        action_had_intended_effect = self._world_state_is_real(intended_effect)
        if action_had_intended_effect:
            action_status = ActionStatus.SUCCESS
        else:
            action_status = ActionStatus.FAIL

        # get a list of the currently-registered resources
        resource_list = self._resource_list()

        # record the results of this iteration
        self._reflect(deepcopy(self._prioritized_goal_list),
                      copy({selected_goal.goal_state_name: selected_goal.goal_state_value}),
                      copy(resource_list), world_state_snapshot, copy(plan),
                      copy(action_taken), copy(post_act_context), copy(action_preconditions),
                      copy(action_status), copy(self._the_world_states()))

        # un-defer any currently deferred goals
        for goal in self._prioritized_goal_list:
            goal.pursue()

        # defer the currently-selected goal if the ai has registered capabilities,
        # but ran into problems meeting the selected goal

        registered_capabilities_exist = self._capabilities != []
        the_ai_could_not_find_a_plan = plan == []
        the_last_action_taken_has_failed = action_status == ActionStatus.FAIL
        the_ai_encountered_problems_meeting_the_goal = the_ai_could_not_find_a_plan or the_last_action_taken_has_failed

        if registered_capabilities_exist and the_ai_encountered_problems_meeting_the_goal:
            selected_goal.defer()
