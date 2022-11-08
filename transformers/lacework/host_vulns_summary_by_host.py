import pandas as pd
import datapane as dp
import numpy as np

def host_vulns_summary_by_host(host_vulns, severities=["Critical", "High", "Medium", "Low"], limit=False):
    df = pd.json_normalize(host_vulns, meta=[['cveProps', 'metadata'], ['evalCtx', 'hostname'], ['featureKey', 'name'], 'vulnId', 'severity', 'mid'])
    
    if 'severity' not in df:
        df['severity'] = False

    # filter
    df = df[df['severity'].isin(severities)]

    # delete extra columns
    df = df[['evalCtx.hostname', 'mid', 'severity']]

    # count severities by MID
    df = df.groupby(['mid', 'severity','evalCtx.hostname']).size().reset_index(name='count')
    
    # summarize severities onto one column (and sort)
    df['sev_merged'] = df['severity'].astype('string') + ": " + df['count'].astype('string')
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity', 'count'],ascending=[True,False])
    df = df.groupby('mid', sort=False, as_index=False).agg({'mid' : 'first', 'evalCtx.hostname' : 'first', 'sev_merged' : f"\n".join})

    # clean names
    df.rename(columns={'mid': 'Machine ID', 'evalCtx.hostname': 'Hostname', 'sev_merged': 'Severity Count'}, inplace=True)
    df = df.drop(columns=['Machine ID'])

    if limit:
        df = df.head(limit)
    
    return df
