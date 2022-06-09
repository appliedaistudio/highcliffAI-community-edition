__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to read the ai server host and port environment variables
import os

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.temperature import ConfirmNormalBodyTemperature


class NormalBodyTemperatureConfirmation(ConfirmNormalBodyTemperature):
    def behavior(self):
        new_context = {
            "info": {
                "title": "Body temperature sensor description using the OneDM Semantic Definition Format",
                "version": "2022-21-05",
                "copyright": "Copyright 2022 appliedAIstudio LLC. All rights reserved.",
                "license": "https://example.com/license"
            },
            "namespace": {
                "cap": "https://appliedai.studio/highcliffai/temp"
            },
            "defaultNamespace": "temp",
            "sdfObject": {
                "Sensor": {
                    "sdfProperty": {
                        "type": {
                            "description": "The type of sensor (Thermal, ...)",
                            "type": "boolean"
                        }
                    },
                    "sdfAction": {
                        "takeReading": {
                            "description": "Take a temperature sensor reading."
                        },
                        "sdfData": {
                            "sensorOutput": "![Output](https://simplifaster.com/wp-content/uploads/2017/07/Human-Body-Heat-Map.jpg)"
                        }
                    }
                }
            }
        }
        self.update_context(new_context)
        print("a normal body temperature has been confirmed")


def start_confirmation():
    NormalBodyTemperatureConfirmation(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    start_confirmation()
