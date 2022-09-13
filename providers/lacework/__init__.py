from laceworksdk import LaceworkClient
from laceworksdk import exceptions

import datetime
LWApiError = exceptions.ApiError

class LazyWrapper(object):
    def __init__(self, func):
        self.func = func
        self.value = None
    def __call__(self):
        if self.value is None:
            self.value = self.func()
        return self.value

lw = LazyWrapper(LaceworkClient)

# lw = LaceworkClient() # This would leverage your default Lacework CLI profile.

def datetime_to_lacework_time(datestr):
    return datestr.strftime("%Y-%m-%dT%H:%M:%S%z")

from .events import events
from .container_vulns import container_vulns
from .host_vulns import host_vulns
from .integrations import integrations
from .compliance_reports import compliance_reports