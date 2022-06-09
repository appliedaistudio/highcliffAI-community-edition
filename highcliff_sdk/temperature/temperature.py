__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio"
__version__ = "0.1"

from ai_framework.ai_actions import AIaction


class MonitorBodyTemperature(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {}
        effects = {"body_temperature_monitored": True}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _monitor_body_temperature_failed(self):
        # this should be called by the custom behavior if it fails to monitor the body temperature
        self.actual_effects["body_temperature_monitored"] = False


class AuthorizeBodyTemperatureAdjustment(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {}
        effects = {"body_temperature_adjustment_authorized": True}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _body_temperature_adjustment_authorization_failed(self):
        # this should be by custom behavior if it fails to get authorization to make an adjustment
        self.actual_effects["body_temperature_adjustment_authorized"] = False


class AdjustBodyTemperature(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {"body_temperature_adjustment_authorized": True}
        effects = {"body_temperature_adjusted": True, "body_temperature_adjustment_authorized": False}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _body_temperature_adjustment_failed(self):
        # this should be called by custom behavior if it fails to complete the adjustment
        self.actual_effects["body_temperature_adjusted"] = False
        self.actual_effects["body_temperature_adjustment_authorized"] = False


class ConfirmNormalBodyTemperature(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {"body_temperature_adjusted": True}
        effects = {"body_temperature_is_normal": True, "body_temperature_adjusted": False}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _body_temperature_is_not_normal(self):
        # this should be called by custom behavior if it determines that no adjustment is needed
        self.actual_effects["body_temperature_is_normal"] = False
