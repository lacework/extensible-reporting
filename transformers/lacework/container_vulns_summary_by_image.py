import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_summary_by_image(container_vulns, severities=["Critical", "High", "Medium", "Low"], limit=False):
    df = pd.json_normalize(container_vulns, meta=[['evalCtx', 'image_info', 'repo'],['evalCtx', 'image_info', 'tags'], ['featureKey', 'name'], ['fixInfo', 'fix_available'], 'vulnId', 'severity', 'imageId'])
    
    # delete extra columns
    df = df[['evalCtx.image_info.repo', 'evalCtx.image_info.tags', 'featureKey.name', 'fixInfo.fix_available', 'vulnId', 'severity', 'imageId']]

    # filter
    df = df[df['severity'].isin(severities)]

    # combine repo and tags into newline separated repo_tag
    df['repo_tags'] = df.apply(lambda y: "\n".join(list(map(lambda x: y['evalCtx.image_info.repo'] + ':' + x, y['evalCtx.image_info.tags']))), axis=1)    
    df.drop(columns=['evalCtx.image_info.tags'], inplace=True)
    df.drop_duplicates(inplace=True)
    
    # assemble multiple repos / tags into one line per imageid
    df = df.groupby(['imageId', 'vulnId', 'featureKey.name']).agg(repositories=('repo_tags', f"\n".join), fix_available=('fixInfo.fix_available', 'first'), severity=('severity', 'first')).reset_index()
    
    # count by severity
    df = df.groupby(['imageId', 'severity']).agg(repositories=('repositories', 'first'), count=('vulnId','count')).reset_index()
        
    # sort and concat severities
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df['sev_merged'] = df['severity'].astype('string') + ": " + df['count'].astype('string')
    df = df.sort_values(by=['severity', 'count'],ascending=[True,False])
    df = df.groupby('imageId', sort=False).agg(repositories=('repositories', 'first'),severities=('sev_merged', f"\n".join)).reset_index()
    
    # reorder
    df = df[['repositories', 'severities', 'imageId']]
    
    # clean names
    df.rename(columns={'imageId': 'Image ID', 'repositories': 'Repository / Tag', 'severities': 'CVE Count'}, inplace=True)

    if limit:
        df = df.head(limit)
    return df
