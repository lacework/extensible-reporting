import datetime
import os

def this_path(file):
    return os.path.join(os.path.dirname(__file__), file)

from .events import events
from .container_vulns import container_vulns
from .host_vulns import host_vulns

def save_data(data, name):
    import pickle
    with open(this_path(name + ".pickle"), "wb") as outfile:
        pickle.dump(data, outfile)
    