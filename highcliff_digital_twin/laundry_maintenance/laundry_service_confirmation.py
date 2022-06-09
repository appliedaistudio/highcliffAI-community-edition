__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to read the ai server host and port environment variables
import os

# needed to read the laundry schedule from a file
import json

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.laundry import ConfirmLaundryMaintained


class LaundryMaintenanceConfirmation(ConfirmLaundryMaintained):
    def behavior(self):
        # update the context
        new_context = self._smart_appliance_settings()
        self.update_context(new_context)
        print("laundry maintenance is complete")

    @staticmethod
    def _smart_appliance_settings():
        file = open("context/sdfSmartApplianceSettings.json")
        return json.load(file)


def start_confirmation():
    LaundryMaintenanceConfirmation(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    start_confirmation()
