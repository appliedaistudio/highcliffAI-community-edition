__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

import os

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.temperature import AuthorizeBodyTemperatureAdjustment


class TemperatureChangeAuthorizationApp(AuthorizeBodyTemperatureAdjustment):
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
                            "sensorOutput": "![Output](https://lh3.googleusercontent.com/GHjZPUn5OdMA3JqYwHd3iIzxVK2KALlIK8G1rqG0WGP1oTiwlVxNL9pwJy6sB85gVViF=w200-rwa)"
                        }
                    }
                }
            }
        }
        self.update_context(new_context)
        print("temperature change is authorized by care provider")


def start_app():
    TemperatureChangeAuthorizationApp(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    start_app()
