import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_summary_by_package(container_vulns, severities=["Critical", "High", "Medium", "Low"]):
    df = pd.json_normalize(container_vulns, meta=[['featureKey', 'name'], 'vulnId', 'severity', 'imageId'])
    
    # clean and santiize
    df.rename(columns={'featureKey.name': 'packageName'}, inplace=True)
    df=df[['packageName','imageId','vulnId','severity']]
    df.drop_duplicates(inplace=True)

    # filter
    df = df[df['severity'].isin(severities)]

    # add image count by package    
    df_image_count_by_package = df.loc[:, ('imageId','packageName')]
    df_image_count_by_package.drop_duplicates(inplace=True)
    df_image_count_by_package = df_image_count_by_package.groupby(['packageName']).agg(imageCount=('imageId', 'count')).reset_index()
    
    df = df.groupby(['packageName', 'severity']).agg(cveCount=('vulnId', 'count')).reset_index()
    
    # sort by critical
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity','cveCount'],ascending=[True,False])
    
    # add combined column
    df['sev_merged'] = df['severity'].astype('string') + ": " + df['cveCount'].astype('string')

    # group by package and count total cves
    df = df.groupby('packageName', sort=False).agg(severities=('sev_merged', f", ".join)).reset_index()

    # combine package and severities
    df['Package Info'] = df['packageName'].astype('string') + "\n" + df['severities'].astype('string')
    
    df = df.merge(df_image_count_by_package, how='left')
    df.rename(columns={'imageCount': 'Count'}, inplace=True)
    
    # reorder and strip unneeded columns
    df = df[['Package Info', 'Count']]
    
    return df
