import pickle
from . import this_path
from . import generic_open

def compliance_reports(*args, **kwargs):
    return generic_open('compliance_reports')