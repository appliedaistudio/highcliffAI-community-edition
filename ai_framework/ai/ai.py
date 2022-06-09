__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"


# used to create and access centralized ai_infrastructure
from ai_framework.ai_infrastructure import LocalNetwork


class AI:
    _network = LocalNetwork.instance()
    _prioritized_goal_list = []
    _capabilities = []
    _diary = []

    def network(self):
        pass

    def set_goals(self, goal_list_in_file_format):
        pass

    def capabilities(self):
        pass

    def add_capability(self, action):
        pass

    def remove_capability(self, action):
        pass

    def run_iteration(self):
        pass

    def reset(self):
        pass

    def diary(self):
        pass
