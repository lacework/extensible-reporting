import pickle
from . import this_path
from . import generic_open

def container_vulns(*args, **kwargs):
    return generic_open('container_vulns')
