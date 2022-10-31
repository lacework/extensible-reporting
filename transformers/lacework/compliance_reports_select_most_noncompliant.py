import pandas as pd
import datapane as dp
import numpy as np
import json

def compliance_reports_select_most_noncompliant(compliance_reports):
    for acct in compliance_reports:
        count = 0
        index = 0
        for idx, report in enumerate(compliance_reports[acct]):
            s = sum(map(lambda x : x['STATUS'] == 'NonCompliant', report))
            if s > count:
                index = idx
        compliance_reports[acct] = compliance_reports[acct][index]

    return compliance_reports