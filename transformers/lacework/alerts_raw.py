import pandas as pd
import datapane as dp
import numpy as np
from datetime import *

def alerts_raw(alerts, severities=["Critical", "High"], excluded_alert_types=["CloudTrailDefaultAlert", "CloudActivityLogIngestionFailed", "NewViolations", "ComplianceChanged"], limit=False):
    df = pd.DataFrame(alerts)
    
    # filter out excluded alerts
    df = df[~df['alertType'].isin(excluded_alert_types)]
    
    # sort & filter by sev
    df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
    df = df.sort_values(by=['severity','startTime'],ascending=[True,False])
    df = df[df['severity'].isin(severities)]
    
    # format time
    df['startTime'] = df['startTime'].apply(lambda x: datetime.fromisoformat(x.replace("Z", "+00:00")).strftime("%B %d, %Y %I:%M%p"))
    
    # delete extra columns
    df = df[['alertId', 'severity', 'startTime', 'alertName']]
    
    # rename columns
    df.rename(columns={'alertId': 'Alert ID', 'severity': 'Severity', 'startTime': 'Alert Time', 'alertName': 'Alert Name'}, inplace=True)

    if limit:
        df = df.head(limit)
    
    return df
    