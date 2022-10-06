import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_summary_by_image(container_vulns, severities=["Critical", "High", "Medium", "Low"]):
    df = pd.json_normalize(container_vulns, meta=[['evalCtx', 'image_info', 'repo'],['evalCtx', 'image_info', 'tags'], ['featureKey', 'name'], ['fixInfo', 'fix_available'], 'vulnId', 'severity', 'imageId'])
    
    # filter
    df = df[df['severity'].isin(severities)]

    # delete extra columns
    # df = df[['evalCtx.hostname', 'mid', 'severity']]

    df['Tags'] = df['evalCtx.image_info.tags'].str.join(f"\n")
    # count severities by imageId
    df = df.groupby(['imageId', 'severity','evalCtx.image_info.repo','Tags']).size().reset_index(name='count')
    
    # summarize severities onto one column (and sort)
    df['sev_merged'] = df['severity'].astype('string') + ": " + df['count'].astype('string')
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity', 'count'],ascending=[True,False])
    df = df.groupby('imageId', sort=False, as_index=False).agg({'Tags' : 'first', 'imageId' : 'first', 'evalCtx.image_info.repo' : 'first', 'sev_merged' : f"\n".join})

    # reorder
    df = df[['evalCtx.image_info.repo', 'Tags', 'sev_merged', 'imageId']]
    
    # clean names
    df.rename(columns={'imageId': 'Image ID', 'evalCtx.image_info.repo': 'Repository Name', 'sev_merged': 'CVE Count'}, inplace=True)

    return df
