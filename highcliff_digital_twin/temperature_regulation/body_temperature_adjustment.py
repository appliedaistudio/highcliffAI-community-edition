__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.temperature import AdjustBodyTemperature

# needed to read the ai server and port environment variables
import os


class SmartThermostat(AdjustBodyTemperature):
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
                            "sensorOutput": "![Output](https://34a0vrrs61o2fpmoztvq511d-wpengine.netdna-ssl.com/wp-content/uploads/2019/10/WiFi-Survey-Heatmap.jpg)"
                        }
                    }
                }
            }
        }
        self.update_context(new_context)
        print("the temperature of the room has been adjusted")


def start_smart_thermostat():
    SmartThermostat(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    start_smart_thermostat()
