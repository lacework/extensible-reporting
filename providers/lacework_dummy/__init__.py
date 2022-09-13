import logging
logger = logging.getLogger(__name__)

import datetime
import os

import pickle

def this_path(file):
    return os.path.join(os.path.dirname(__file__), file)

def save_data(data, name):
    save_path = this_path(name + ".pickle")
    logger.info('Saving ' + name + ' data to ' + save_path)
    with open(save_path, "wb") as outfile:
        pickle.dump(data, outfile)
    
def generic_open(name):
    data_file = this_path(name + '.pickle')
    logger.info('Loading ' + data_file)
    with open(data_file, "rb") as infile:
        results = pickle.load(infile)
        return results

from .events import events
from .container_vulns import container_vulns
from .host_vulns import host_vulns
from .compliance_reports import compliance_reports
from .integrations import integrations