from laceworksdk import LaceworkClient
import datetime

lw = LaceworkClient() # This would leverage your default Lacework CLI profile.

def datetime_to_lacework_time(datestr):
    return datestr.strftime("%Y-%m-%dT%H:%M:%S%z")

from .events import events
from .container_vulns import container_vulns
from .host_vulns import host_vulns
