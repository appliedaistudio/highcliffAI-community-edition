__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# the Highcliff ai_actions we are going to implement
from highcliff_sdk.laundry import LaundryScheduler

# needed to access host and port environment variables
import os

# needed to randomly select laundry days
import random

# needed to run laundry schedule monitoring on a non-blocking loop
import threading
import time

# needed to read the laundry schedule from a file
import json

# needed to handle losing a connection to the AI
from ai_framework.ai_actions import AIConnectionLost


class LaundryScheduleMonitor(LaundryScheduler):
    def behavior(self):
        # update the context
        new_context = self._laundry_schedule()
        self.update_context(new_context)

        # begin monitoring the laundry schedule in a separate, non-blocking thread
        thread = threading.Thread(target=self._monitor_laundry_schedule)
        thread.start()

    def _monitor_laundry_schedule(self):
        seconds_to_pause_between_monitoring_the_laundry_schedule = 10
        seconds_it_takes_to_do_the_laundry = 30

        # monitor the laundry schedule
        while True:
            if self._is_laundry_day():

                # if it is laundry day, let the world know that the laundry needs to be maintained
                print("it's laundry day")
                try:
                    self.update_the_world("laundry_maintained", False, self.context())
                except AIConnectionLost:
                    pass

                # give the AI time to react to it being laundry day
                time.sleep(seconds_it_takes_to_do_the_laundry)
            else:
                print("it is not laundry day")
                pass

            # pause before checking the laundry schedule again
            time.sleep(seconds_to_pause_between_monitoring_the_laundry_schedule)

    @staticmethod
    def _laundry_schedule():
        file = open("context/sdfLaundrySchedule.json")
        return json.load(file)

    @staticmethod
    def _is_laundry_day():
        # randomly decides (1 in 6 chance) if today is laundry day
        return random.choice([True, False, False, False, False, False])


def start_laundry_schedule_monitor():
    LaundryScheduleMonitor(server=os.environ['ai_server'], port=os.environ['ai_server_port'])


if __name__ == "__main__":
    start_laundry_schedule_monitor()
