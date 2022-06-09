__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.laundry import LaundryService

# needed to read the ai server and port environment variables
import os

# needed to read the laundry smart appliance settings from a file
import json


class LaundrySmartAppliances(LaundryService):
    def behavior(self):
        # update the context
        new_context = self._smart_appliance_settings()
        self.update_context(new_context)
        print("smart appliances have been activated by the AI")

    @staticmethod
    def _smart_appliance_settings():
        file = open("context/sdfSmartApplianceSettings.json")
        return json.load(file)


def smart_laundry_appliances():
    LaundrySmartAppliances(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    smart_laundry_appliances()