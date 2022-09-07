import pickle
from . import this_path

def events(start_time, end_time):
    with open(this_path("events.pickle"), "rb") as infile:
        events = pickle.load(infile)
        return events