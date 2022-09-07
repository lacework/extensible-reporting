import pickle
from . import this_path

def host_vulns(start_time, end_time):
    with open(this_path("host_vulns.pickle"), "rb") as infile:
        results = pickle.load(infile)
        return results