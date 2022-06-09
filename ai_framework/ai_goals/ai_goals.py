from dataclasses import dataclass, field
from math import sqrt


@dataclass(order=True)
class AIGoal:
    # allow goals to be sorted
    sort_index: float = field(init=False, repr=False)

    # define fields in a goal
    goal_state_name: str
    goal_state_value: bool
    criticality: float
    time_sensitivity: float
    deferrable: bool = True
    deferred: bool = False

    # sort goals by priority calculated from criticality and sensitivity
    def __post_init__(self):
        self.sort_index = sqrt(self.criticality ** 2 + self.time_sensitivity ** 2)

        # a goal can be deferred if it is not time sensitive
        not_time_sensitive = self.time_sensitivity <= 0.5
        self.deferrable = not_time_sensitive

    def defer(self):
        if self.deferrable:
            self.deferred = True
            print(f"goal {self.goal_state_name}-{self.goal_state_value} has been deferred")

    def pursue(self):
        self.deferred = False
