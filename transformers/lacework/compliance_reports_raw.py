import pandas as pd
import datapane as dp
import numpy as np

def compliance_reports_raw(compliance_reports, severities=["Critical", "High"]):
    rows = []
  
    for report in compliance_reports:
        recommendations = report['recommendations']
        reportType = report['reportType']
          
        for row in recommendations:
            row['reportType']= reportType
            rows.append(row)
      
    df = pd.json_normalize(rows)
    df = df[df['STATUS'].isin(["NonCompliant"])]
    
    df = df.sort_values(by=['SEVERITY', 'ASSESSED_RESOURCE_COUNT'],ascending=[True,False])
    
    df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
    df = df[df['SEVERITY'].isin(severities)]
    
    df = df.reset_index()

    df['Non-compliant vs Assessed resources'] = df['ASSESSED_RESOURCE_COUNT'].astype('string') + " / " + df['RESOURCE_COUNT'].astype('string')
    df = df[['ACCOUNT_ID', 'CATEGORY', 'TITLE', 'SEVERITY', 'Non-compliant vs Assessed resources']]
    
    return df