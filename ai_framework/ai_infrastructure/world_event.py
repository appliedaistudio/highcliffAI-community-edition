__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

from dataclasses import dataclass

# needed to define a default timestamp value for world events
import datetime

# needed to validate the context
from ai_framework.ai_context import is_validate_context


@dataclass()
class WorldEvent:
    # define the fields in a world event
    world_state_name: str
    world_state_value: bool
    context: dict
    time_stamp: str = datetime.datetime.now()

    def __post_init__(self):
        # validate the context
        if not is_validate_context(self.context):
            raise Exception("The context is not valid")
