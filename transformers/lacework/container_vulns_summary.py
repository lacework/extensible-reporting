import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_summary(container_vulns, severities=["Critical", "High", "Medium", "Low"]):
    df = pd.json_normalize(container_vulns, meta=[['evalCtx', 'image_info', 'repo'], ['featureKey', 'name'], 'vulnId', 'severity', 'imageId'])
    
    # filter
    df = df[df['severity'].isin(severities)]

    # delete extra columns
    df = df[['imageId', 'severity']]

    # count severities by host & total sum
    df = df.groupby(['severity'])['imageId'].agg(['count', 'nunique'])
    df = df.reset_index()

    # sort
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity'])

    # rename columns    
    df.rename(columns={'severity': 'Severity', 'count': 'Total CVEs', 'nunique': 'Images Affected'}, inplace=True)

    return dp.Table(df)
