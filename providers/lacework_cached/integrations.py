import pickle
from . import this_path
from . import generic_open

def integrations(*args, **kwargs):
    return generic_open('integrations')
