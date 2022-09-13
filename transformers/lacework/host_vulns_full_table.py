import pandas as pd
import datapane as dp
import numpy as np

def host_vulns_full_table(host_vulns, severities=["Critical", "High"]):
    df = pd.json_normalize(host_vulns, meta=[['evalCtx', 'hostname'], ['featureKey', 'name'], 'vulnId', 'severity', 'mid'])
    
    # filter
    df = df[df['severity'].isin(severities)]
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values('severity')
    
    # concat fields
    df['vuln_details'] = df['severity'].astype('string') + ': ' + df['featureKey.name'] + '(' + df['vulnId'] + ')'
    
    # dedupe, remove empties
    df['vuln_details'].replace('', np.nan, inplace=True)
    df.dropna(subset=['vuln_details'], inplace=True)

    # group by mid
    df = df[['evalCtx.hostname', 'mid', 'vuln_details']]
    df = df.fillna('').groupby('mid', as_index=False).agg({'mid' : 'first', 'evalCtx.hostname' : 'first', 'vuln_details' : f"\n".join})
    
    # rename columns    
    df.rename(columns={'mid': 'Machine ID', 'evalCtx.hostname': 'Hostname', 'vuln_details': 'Vulnerabilities'}, inplace=True)

    # style
    df = df.style.set_table_styles({"vuln_details" : [
        {
            "selector" :"td",
            "props": "white-space: pre-wrap; text-align:left"
        }
    ]})

    return df
