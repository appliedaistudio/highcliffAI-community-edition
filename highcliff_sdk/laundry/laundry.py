__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio"
__version__ = "0.1"

from ai_framework.ai_actions import AIaction


class LaundryScheduler(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {}
        effects = {"laundry_monitored": True}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _laundry_scheduling_failed(self):
        # this should be called by the custom behavior if there is a problem keeping up with the laundry schedule
        self.actual_effects["laundry_monitored"] = False


class LaundryServiceAuthorization(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {}
        effects = {"laundry_service_authorized": True}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _laundry_service_authorization_failed(self):
        # this should be by custom behavior if it fails to get authorization to start laundry services
        self.actual_effects["laundry_service_authorized"] = False


class LaundryService(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {"laundry_service_authorized": True}
        effects = {"laundry_service_provided": True, "laundry_service_authorized": False}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _laundry_service_failed(self):
        # this should be called by custom behavior if it fails to provide the service
        self.actual_effects["laundry_service_provided"] = False
        self.actual_effects["laundry_service_authorized"] = False


class ConfirmLaundryMaintained(AIaction):
    def __init__(self, server="localhost", port=12345):
        preconditions = {"laundry_service_provided": True}
        effects = {"laundry_maintained": True, "laundry_service_provided": False}
        super().__init__(preconditions=preconditions, initial_effects=effects, server=server, port=port)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def _laundry_is_not_maintained(self):
        # this should be called by custom behavior if it fails to confirmed that laundry is maintained
        self.actual_effects["laundry_maintained"] = False
