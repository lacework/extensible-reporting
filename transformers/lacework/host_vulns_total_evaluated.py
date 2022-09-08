import pandas as pd
import datapane as dp
import numpy as np

def host_vulns_total_evaluated(host_vulns):
    df = pd.DataFrame(host_vulns)

    # count severities by host & total sum
    unique_hosts = df.mid.nunique()

    return unique_hosts
