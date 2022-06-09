__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

from enum import Enum
import random


class TemperatureScale(Enum):
    CELSIUS = 1
    FAHRENHEIT = 2


# simulates a sensor that returns a reading of the body temperature
def get_body_temperature(scale):
    if scale == TemperatureScale.CELSIUS:
        body_temperature = random.uniform(35, 38)
    else:
        body_temperature = random.uniform(96, 100)

    return body_temperature
