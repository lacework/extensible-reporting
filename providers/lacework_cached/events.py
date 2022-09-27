import pickle
from . import this_path
from . import generic_open

def events(*args, **kwargs):
    return generic_open('events')
