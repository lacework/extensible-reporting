import pandas as pd
import datapane as dp
import numpy as np

def host_vulns_summary(host_vulns, severities=["Critical", "High", "Medium", "Low"]):
    df = pd.json_normalize(host_vulns, meta=[['evalCtx', 'hostname'], ['featureKey', 'name'], 'vulnId', 'severity', 'mid'])
    
    # filter
    df = df[df['severity'].isin(severities)]

    # delete extra columns
    df = df[['evalCtx.hostname', 'mid', 'severity']]

    # count severities by host & total sum
    df = df.groupby(['severity'], as_index=False)['mid'].agg(['count', 'nunique'])
    
    for severity in severities:
        if not severity in df.index: df = df.append(pd.DataFrame([{'severity': severity, 'count': 0, 'nunique': 0}]).set_index('severity'))

    df = df.reset_index()

    # sort
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity'])
    df = df.reset_index()
    df = df.drop(columns=['index'])
    
    # rename columns    
    df.rename(columns={'severity': 'Severity', 'count': 'Total CVEs', 'nunique': 'Hosts Affected'}, inplace=True)
    
    return df
