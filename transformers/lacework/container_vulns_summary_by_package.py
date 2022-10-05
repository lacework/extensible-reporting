import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_summary_by_package(container_vulns, severities=["Critical", "High", "Medium", "Low"]):
    df = pd.json_normalize(container_vulns, meta=[['featureKey', 'name'], 'vulnId', 'severity', 'imageId'])
    df.rename(columns={'featureKey.name': 'packageName'}, inplace=True)
    # filter
    df = df[df['severity'].isin(severities)]

    # count severities by package & vuln
    df = df.groupby(['packageName', 'vulnId'], sort=False).agg(severity=('severity', 'first'), count=('imageId', 'count'))

    # group by package, severity, and agg by sum of count
    df = df.groupby(['packageName', 'severity'], sort=False).agg(count=('count', 'sum')).reset_index()
    
    # sort by critical
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity', 'count'],ascending=[True,False])
        
    # add combined column
    df['sev_merged'] = df['severity'].astype('string') + ": " + df['count'].astype('string')

    # group by package and count total cves
    df = df.groupby('packageName', sort=False).agg(Count=('count', 'sum'), severities=('sev_merged', f", ".join))
    df = df.reset_index()

    # combine package and severities
    df['Package Info'] = df['packageName'].astype('string') + "\n" + df['severities'].astype('string')

    # reorder and strip unneeded columns
    df = df[['Package Info', 'Count']]
    
    return df
