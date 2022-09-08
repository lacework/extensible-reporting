import pickle
from . import this_path

def compliance_reports(accounts=[]):
    with open(this_path("compliance_reports.pickle"), "rb") as infile:
        compliance_reports = pickle.load(infile)
        return compliance_reports