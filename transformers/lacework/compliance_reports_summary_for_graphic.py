import pandas as pd
import datapane as dp
import numpy as np

def compliance_reports_summary_for_graphic(compliance_reports, severities=["Critical", "High", "Medium", "Low"]):

    df = pd.DataFrame(compliance_reports)
    df = df[df['STATUS'].isin(["NonCompliant"])]
    
    df['RESOURCE_COUNT'] = (df['VIOLATIONS'].str.len())
        
    # sort to determine account order, while we still have the severity & resource count data
    df = df.sort_values(by=['SEVERITY', 'RESOURCE_COUNT'],ascending=[True,False])
    account_order = df['ACCOUNT_ID'].unique()
    
    # group
    df = df.groupby(['ACCOUNT_ID', 'SEVERITY']).agg(failed_control_count=('SEVERITY', 'count'), failed_resources=('RESOURCE_COUNT', 'sum')).reset_index()
    
    # sort by accounts with most criticals, followed by most highs
    df['ACCOUNT_ID'] = pd.Categorical(df['ACCOUNT_ID'], account_order)
    df.sort_values(by=['ACCOUNT_ID', 'SEVERITY'], ascending=True)

    # convert int and filter severities
    df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
    df = df[df['SEVERITY'].isin(severities)]

    # rename    
    df.rename(columns={'ACCOUNT_ID': 'Account ID', 'SEVERITY': 'Severity', 'failed_resources': 'Non-compliant Resources', 'failed_control_count': 'Failed controls'}, inplace=True)
    
    # pivot and preseve severity order (pivot breaks this)
    severity_order = df['Severity'].unique()
    df = pd.pivot_table(df, values='Non-compliant Resources', index='Account ID', columns='Severity', sort=False)
    df = df.reindex(severity_order, axis=1)
    
    return df
