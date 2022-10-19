import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_summary(container_vulns, severities=["Critical", "High", "Medium", "Low"]):
    df = pd.json_normalize(container_vulns, meta=[['evalCtx', 'image_info', 'repo'], ['featureKey', 'name'], 'vulnId', 'severity', 'imageId'])
    
    # filter
    df = df[df['severity'].isin(severities)]

    # delete extra columns
    df = df[['imageId', 'severity', 'vulnId', 'featureKey.name']]
    df.drop_duplicates(inplace=True)
    
    # count severities by host & total sum
    df = df.groupby(['severity'])['imageId'].agg(['count', 'nunique'])
    for severity in severities:
        if not severity in df.index: df = df.append(pd.DataFrame([{'severity': severity, 'count': 0, 'nunique': 0}]).set_index('severity'))

    df = df.reset_index()

    # sort
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity'])

    # rename columns    
    df.rename(columns={'severity': 'Severity', 'count': 'Total CVEs', 'nunique': 'Images Affected'}, inplace=True)
    df = df.reset_index(drop=True)

    return df
