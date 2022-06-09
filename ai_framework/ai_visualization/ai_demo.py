__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to create markdown files for the demo visualization software
from mdutils.mdutils import MdUtils

# needed to create time stamps for visualizing the diary entries
from datetime import datetime

# needed to delete files from the demo folder
import os
import glob

# needed to tag the entry with an action status
from ai_framework.ai_actions import ActionStatus

# needed to determine the age of a file on different platforms
import platform

# needed to format the text in the ai action context
import json

# needed to enumerate display file types
from enum import Enum


# define the possible hash tags
DemoTags = {
    "preconditions": "#pre",
    "postconditions": "#post",
    "goals": "#goals",
    "goal": "#goal",
    "idle": "#idle",
    "blocked": "#blocked",
    "states": "#states",
    "ai_action": "#aiaction",
    f"{ActionStatus.SUCCESS.value}": "#success",
    f"{ActionStatus.FAIL.value}": "#fail"
}


# define the types of demo display files
class DisplayFileTypes(Enum):
    GENERAL_AI_ACTION = 1
    BLOCKED_AI_ACTION = 2
    IDLE_AI_ACTION = 3
    FAILED_AI_ACTION = 4
    GOAL_STATE = 5
    INVALID_WORLD_STATE = 6
    UNKNOWN = 7


class AIDemo:
    def __init__(self, demo_mode=False, markdown_folder='/'):
        self._demo_mode = demo_mode
        self._markdown_folder = markdown_folder
        self._file_formatted_goal_list = []
        self._blocked_node_removed_already = True
        self._idle_node_removed_already = True

    def reset_demo(self):
        if self._demo_mode:
            # clear the demo folder of all contents
            files = glob.glob(f'{self._markdown_folder}*')
            for f in files:
                try:
                    os.remove(f)
                except:
                    pass

            # create demo visualization for the idle state
            idle_state_name = "IDLE"
            md_file = MdUtils(file_name=self._markdown_folder + idle_state_name)
            md_file.new_line(DemoTags['idle'])
            md_file.create_md_file()

            # create demo visualization for the blocked state
            blocked_state_name = "BLOCKED"
            md_file = MdUtils(file_name=self._markdown_folder + blocked_state_name)
            md_file.new_line(DemoTags['blocked'])
            md_file.create_md_file()

    def _create_world_state_file(self, clean_state_name, tag):
        # create a markdown file from the given state name

        # create a new state demo file
        md_file = MdUtils(file_name=self._markdown_folder + clean_state_name)

        # tag the new file
        md_file.new_line(tag)

        # write the state file to the folder
        md_file.create_md_file()

    def demo_goals(self, file_formatted_goal_list):
        if self._demo_mode:
            # keep track of the goals
            self._file_formatted_goal_list = file_formatted_goal_list

            # create a new goals demo file
            md_file = MdUtils(file_name=self._markdown_folder + 'goals')

            # tag the file as containing goals
            md_file.new_line(DemoTags['goals'])

            # add individual goals to the goal demo file
            for goal in file_formatted_goal_list:
                goal_state_name = goal['goal_state_name']
                goal_state_value = goal['goal_state_value']
                goal = f"{goal_state_name}-{goal_state_value}"

                # create a new goal file
                self._create_world_state_file(goal, DemoTags['goal'])

                # link to the new goal file
                md_file.new_line(f"[[{goal}]]")

            # write the goal demo file to the folder
            md_file.create_md_file()

    def update_demo_goals(self, diary_entry):

        if self._demo_mode:
            # Open the goals file with access mode 'a'
            file_object = open(self._markdown_folder + 'goals.md', 'a')

            # write new content to the goals file based on the given diary entry
            self._write_iteration_header(file_object)
            self._write_prioritized_goal_list(diary_entry, file_object)
            self._write_goal(diary_entry, file_object)
            self._write_resource_list(diary_entry, file_object)
            self._write_plan(diary_entry, file_object)
            self._write_action(diary_entry, file_object)
            self._write_world_state_before(diary_entry, file_object)
            self._write_world_state_after(diary_entry, file_object)

            # Close the file
            file_object.close()

    @staticmethod
    def _write_world_state_after(diary_entry, file_object):
        # write the world state after the action was taken
        file_object.writelines("\n")
        for world_state in list(diary_entry['the_world_state_after'].keys()):
            world_state_value = diary_entry['the_world_state_after'][world_state]
            after_element = f"\n<after {world_state}={world_state_value}>"
            file_object.writelines(after_element)

    @staticmethod
    def _write_world_state_before(diary_entry, file_object):
        # write the world state before the action was taken

        file_object.writelines("\n")
        for world_state in list(diary_entry['the_world_state_before'].keys()):
            world_state_value = diary_entry['the_world_state_before'][world_state]
            before_element = f"\n<before {world_state}={world_state_value}>"
            file_object.writelines(before_element)

    @staticmethod
    def _write_action(diary_entry, file_object):
        # create and write the action taken as part of the given diary entry

        if "SUCCESS" in str(diary_entry['action_status']):
            action_status = "success"
        else:
            action_status = "fail"
        if diary_entry['action_taken'] == "":
            action_name = "NONE"
        else:
            action_name = diary_entry['action_taken']
        file_object.writelines(f"\n<action name={action_name} status={action_status}>")

    @staticmethod
    def _write_plan(diary_entry, file_object):
        # create and write the plan to achieve the currently-selected goal

        plan_open_tag = f"\n\n<plan>"
        plan_close_tag = "\n<plan>"
        plan_content = ""
        # include the plan steps in the action plan
        if diary_entry['my_plan'] is None:
            # write an empty plan
            file_object.writelines(f"\n\n<plan state=NONE>")
        else:
            # build plan content
            for step in diary_entry['my_plan']:
                start = '<'
                end = ' object at'
                step_string = str(step)
                step_content = (step_string.split(start))[1].split(end)[0]
                plan_content += f"\n      {step_content}"
            # write plan and content
            file_object.writelines(plan_open_tag)
            file_object.writelines(plan_content)
            file_object.writelines(plan_close_tag)

    @staticmethod
    def _write_resource_list(diary_entry, file_object):
        # create and write the list of resources currently registered with the ai
        if len(diary_entry['my_resources']) == 0:
            # there are no resources
            file_object.writelines("\n<resources status=NONE>")
        else:
            # there are resources
            resource_list_open_tag = f"\n<resources>"
            resource_list_close_tag = f"\n<resources>"
            resources = ""
            for resource in diary_entry['my_resources']:
                resources += f"\n      {resource}"

            file_object.writelines(resource_list_open_tag)
            file_object.writelines(resources)
            file_object.writelines(resource_list_close_tag)

    @staticmethod
    def _write_goal(diary_entry, file_object):
        # create and write the details of the selected goal
        try:
            goal_state = list(diary_entry['my_goal'].keys())[0]
            goal_value = diary_entry['my_goal'][goal_state]
            goal_element = f"\n\n<goal {goal_state}={goal_value}>"
        except:
            goal_element = f"\n\n<goal state=NONE>"
        file_object.writelines(goal_element)

    @staticmethod
    def _write_prioritized_goal_list(diary_entry, file_object):
        # create and write the prioritized list of goal
        if len(diary_entry['prioritized_goals']) == 0:
            # there are no goals
            file_object.writelines("\n<prioritized_goals status=NONE>")
        else:
            # there is a list of prioritized goals
            prioritized_goal_list_open_tag = f"\n<prioritized-goals>"
            prioritized_goal_list_close_tag = f"\n<prioritized-goals>"
            goal_content = ""
            for goal in diary_entry['prioritized_goals']:
                goal_content += \
                    f"\n      <goal state={goal.goal_state_name}-{goal.goal_state_value} " \
                    f"priority={round(goal.sort_index, 2)} " \
                    f"deferred={goal.deferred}>"

            file_object.writelines(prioritized_goal_list_open_tag)
            file_object.writelines(goal_content)
            file_object.writelines(prioritized_goal_list_close_tag)

    @staticmethod
    def _write_iteration_header(file_object):
        # write the header that will show up at the beginning of each diary entry
        file_object.writelines("\n\n\nartificial intelligence iteration")

    def _is_a_goal(self, world_state_name, world_state_value):
        # determines if the given world state is a goal
        for goal in self._file_formatted_goal_list:
            if world_state_name == goal['goal_state_name'] and world_state_value == goal['goal_state_value']:
                return True
        return False

    @staticmethod
    def _world_state_changes(world_before, world_after):
        # return a dictionary of the states in the world after that are different from the world before

        world_state_changes = {}

        states_in_the_world_before = list(world_before.keys())
        for world_after_state_name in world_after:
            world_after_state_value = world_after[world_after_state_name]

            # find the states in the world after but not in the world before
            if world_after_state_name not in states_in_the_world_before:
                world_state_changes[world_after_state_name] = world_after_state_value

            # find the states with different values in the world before and after
            elif world_before[world_after_state_name] != world_after_state_value:
                world_state_changes[world_after_state_name] = world_after_state_value

        return world_state_changes

    def demo_diary_entry(self, entry):
        if self._demo_mode:
            # generate a timestamp
            time_stamp = datetime.timestamp(datetime.now())

            # create a new diary demo file
            md_file = MdUtils(file_name=self._markdown_folder + f'ai_action_{time_stamp}')

            # tag the file as a diary entry
            md_file.new_line(DemoTags['ai_action'])

            no_goal = {"NONE": True}

            # if the action is an idle run of the ai, link to the idle state
            if entry['my_goal'] == no_goal:
                md_file.new_line('[[IDLE]]')

            # if the action fails to find a viable plan, link to the blocked state
            elif entry['my_plan'] is None:
                md_file.new_line('[[BLOCKED]]')

            # otherwise link to active world states:
            else:

                # link action preconditions to the diary entry
                self._create_and_link_world_states(DemoTags['preconditions'],
                                                   entry['action_preconditions'],
                                                   DemoTags[entry['action_status'].value],
                                                   md_file)

                # link 'the world states after' to the diary entry
                world_state_changes = self._world_state_changes(entry['the_world_state_before'],
                                                                entry['the_world_state_after'])
                self._create_and_link_world_states(DemoTags['postconditions'],
                                                   world_state_changes,
                                                   DemoTags[entry['action_status'].value],
                                                   md_file)

            # add the post-act context to the diary entry
            md_file.new_line('')
            formatted_context = json.dumps(entry['post_act_context'], indent=2)
            md_file.write(formatted_context, wrap_width=0)

            # write the diary entry demo file to the folder
            md_file.create_md_file()

    def _create_and_link_world_states(self, states_tag, world_states, action_status_tag, md_file):
        # tag the beginning of the states
        md_file.new_line(f"\nbegin-{states_tag}")

        for world_state_name in world_states:
            world_state_value = world_states[world_state_name]
            world_state = f"{world_state_name}-{world_state_value}"

            # determine the appropriate tag for this state (world state or goal)
            if self._is_a_goal(world_state_name, world_state_value):
                tag = DemoTags['goal']
            else:
                tag = DemoTags['states']

            # create a new world state file
            self._create_world_state_file(world_state, tag)

            # link to the new world state file
            md_file.new_line(f"[[{world_state}]]")

        # tag the end of the states
        md_file.new_line(f"end-{states_tag}\n")

        # tag the status of the diary entry
        md_file.new_line(action_status_tag)

    @staticmethod
    def _read_conditions(file_content, begin_marker, end_marker):
        refined_conditions_list = []

        try:
            # get the indexes of the maker positions in the file content
            idx1 = file_content.index(begin_marker)
            idx2 = file_content.index(end_marker)

            # use the indexes of the marker positions to extract the text between the beginning and end markers
            conditions_text = file_content[idx1 + len(begin_marker) + 1: idx2]
            raw_conditions_list = conditions_text.splitlines()

            # remove the unwanted brackets from each post condition
            for raw_condition in raw_conditions_list:
                idx1 = raw_condition.index("[[")
                idx2 = raw_condition.index("]]")
                refined_condition = raw_condition[idx1 + len("[["): idx2]
                refined_conditions_list.append(refined_condition)
        except:
            pass

        return refined_conditions_list

    def retire_nodes(self, world_states):
        if self._demo_mode:
            # remove any node whose state is inconsistent with the known world states
            # todo put in the states that are now valid. change the method nome to something like refresh

            # build a list of invalid world states
            invalid_world_states = self._invalid_world_states(world_states)

            # step through each file, evaluate the file and remove it if necessary
            for file_name in os.listdir(self._markdown_folder):

                file_content = self._read_file_content(file_name)
                file_display_type = self._file_display_type(file_name, file_content, invalid_world_states)

                if file_display_type == DisplayFileTypes.BLOCKED_AI_ACTION:
                    self._remove_blocked_action(file_name)

                elif file_display_type == DisplayFileTypes.IDLE_AI_ACTION:
                    self._remove_idle_action(file_name)

                elif file_display_type == DisplayFileTypes.GOAL_STATE:
                    pass

                elif file_display_type == DisplayFileTypes.GENERAL_AI_ACTION:
                    self._remove_general_action(file_content, file_name, invalid_world_states)

                elif file_display_type == DisplayFileTypes.INVALID_WORLD_STATE:
                    os.remove(self._markdown_folder + file_name)

                elif file_display_type == DisplayFileTypes.FAILED_AI_ACTION:
                    os.remove(self._markdown_folder + file_name)

    def _remove_general_action(self, file_content, file_name, invalid_world_states):
        # keep the ai action if any of the effects that it had on the world are still valid

        # build a list of preconditions present in the current file
        begin_marker = "begin-" + DemoTags['preconditions']
        end_marker = "end-" + DemoTags['preconditions']
        preconditions = self._read_conditions(file_content, begin_marker, end_marker)

        # build a list of post conditions present in the current file
        begin_marker = "begin-" + DemoTags['postconditions']
        end_marker = "end-" + DemoTags['postconditions']
        post_conditions = self._read_conditions(file_content, begin_marker, end_marker)

        # subtract the preconditions from the post conditions to get the net effect of the action
        net_effects = self._net_effects(preconditions, post_conditions)

        # count the number of valid net effects
        valid_net_effects = len(net_effects)
        for effect in net_effects:
            if effect in invalid_world_states:
                valid_net_effects -= 1

        # if there is at least one valid net effect, keep the file, otherwise delete it
        there_is_at_least_one_valid_net_effect = valid_net_effects > 0
        if there_is_at_least_one_valid_net_effect:
            # keep the file
            pass
        else:
            os.remove(self._markdown_folder + file_name)

    @staticmethod
    def _net_effects(preconditions, post_conditions):
        # build a list of post conditions not present in the preconditions
        net_effects = []
        for post_condition in post_conditions:
            if post_condition not in preconditions:
                net_effects.append(post_condition)
        return net_effects

    def _remove_idle_action(self, file_name):
        # remove idle actions if we haven't already removed an idle action
        if self._idle_node_removed_already:
            self._idle_node_removed_already = False
        else:
            os.remove(self._markdown_folder + file_name)
            self._idle_node_removed_already = True

    def _remove_blocked_action(self, file_name):
        # remove blocked actions if we haven't already removed a blocked action
        if self._blocked_node_removed_already:
            self._blocked_node_removed_already = False
        else:
            os.remove(self._markdown_folder + file_name)
            self._blocked_node_removed_already = True

    @staticmethod
    def _action_is_idle(file_content):
        return "IDLE" in file_content

    @staticmethod
    def _file_display_type(file_name, file_content, invalid_world_states):
        if DemoTags['goal'] in file_content or DemoTags['goals'] in file_content:
            display_type = DisplayFileTypes.GOAL_STATE
        elif file_name.replace(".md", "") in invalid_world_states:
            display_type = DisplayFileTypes.INVALID_WORLD_STATE
        elif DemoTags[ActionStatus.FAIL.value] in file_content:
            display_type = DisplayFileTypes.FAILED_AI_ACTION
        elif "BLOCKED" in file_content:
            display_type = DisplayFileTypes.BLOCKED_AI_ACTION
        elif "IDLE" in file_content:
            display_type = DisplayFileTypes.IDLE_AI_ACTION
        elif "ai_action" in file_name:
            display_type = DisplayFileTypes.GENERAL_AI_ACTION
        else:
            display_type = DisplayFileTypes.UNKNOWN

        return display_type

    def _read_file_content(self, filename):
        try:
            with open(self._markdown_folder + filename) as file:
                file_content = str(file.readlines())
        except PermissionError:
            file_content = ""

        return file_content

    @staticmethod
    def _invalid_world_states(world_states):
        # invalid states are the boolean opposites of all world states
        invalid_world_states = []
        world_state_names = world_states.keys()
        for world_state_name in world_state_names:
            invalid_world_state_value = not world_states[world_state_name]
            invalid_world_state = f"{world_state_name}-{invalid_world_state_value}"
            invalid_world_states.append(invalid_world_state)
        return invalid_world_states

    @staticmethod
    def _is_markdown_file(filename):
        markdown_extension = ".md"
        if markdown_extension in filename:
            return True
        else:
            return False

    @staticmethod
    def _creation_date(path_to_file):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime
