__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to access host and port environment variables
import os

# needed to run temperature monitoring on a non-blocking loop
import threading
import time

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.temperature import MonitorBodyTemperature

# needed to get body temperature readings
from highcliff_digital_twin.temperature_regulation.temperature_sensor import TemperatureScale, get_body_temperature

# needed to handle losing a connection to the AI
from ai_framework.ai_actions import AIConnectionLost


class BodyTemperatureMonitor(MonitorBodyTemperature):
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

        # begin monitoring the body temperature in a separate, non-blocking thread
        thread = threading.Thread(target=self._monitor_body_temperature)
        thread.start()

    def _monitor_body_temperature(self):
        seconds_to_pause_between_body_temperature_readings = 2

        # define the range of normal body temperature
        normal_low_body_temp_in_fahrenheit = 96.4
        normal_high_body_temp_in_fahrenheit = 99.6

        # monitor the current body temperature
        while True:
            # get the current body temperature
            current_body_temperature = get_body_temperature(TemperatureScale.FAHRENHEIT)
            print("body temperature is", current_body_temperature)

            # let the world know about the current state of the body temperature
            if normal_high_body_temp_in_fahrenheit >= current_body_temperature >= normal_low_body_temp_in_fahrenheit:
                print("the body temperature is fine")
            else:
                print("the body temperature is not normal")
                try:
                    self.update_the_world("body_temperature_is_normal", False, self.context())
                except AIConnectionLost:
                    pass

                # give the AI time to react to the abnormal body temperature
                time.sleep(30)

            # pause before taking the next body temperature reading
            time.sleep(seconds_to_pause_between_body_temperature_readings)


def start_body_temperature_monitor():
    BodyTemperatureMonitor(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    start_body_temperature_monitor()
