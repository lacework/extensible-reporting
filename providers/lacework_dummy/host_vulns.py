import pickle
from . import this_path
from . import generic_open

def host_vulns(*args, **kwargs):
    return generic_open('host_vulns')
