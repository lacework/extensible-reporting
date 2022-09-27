import pandas as pd
import datapane as dp
import numpy as np

def compliance_reports_summary(compliance_reports, severities=["Critical", "High"]):

    df = pd.DataFrame(compliance_reports)
    df = df[df['STATUS'].isin(["NonCompliant"])]
    
    df = df.sort_values(by=['SEVERITY', 'RESOURCE_COUNT'],ascending=[True,False])
    
    df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
    df = df[df['SEVERITY'].isin(severities)]
    
    df = df.groupby(['ACCOUNT_ID', 'SEVERITY']).agg(count=('SEVERITY', 'count'), resources=('RESOURCE_COUNT', 'sum'), assessed=('ASSESSED_RESOURCE_COUNT', 'sum')).reset_index() # .size().reset_index(name='count')
    df['sev_merged'] = df['SEVERITY'].astype('string') + ": " + df['count'].astype('string')

    df = df.groupby('ACCOUNT_ID').agg({'sev_merged' : f"\n".join, 'resources' : 'sum', 'assessed' : 'sum'}).reset_index()
    df.rename(columns={'ACCOUNT_ID': 'Account ID', 'sev_merged': 'Severity Count', 'resources': 'Non-compliant Resources', 'assessed': 'Total Assessed Resources'}, inplace=True)
    
    return df
