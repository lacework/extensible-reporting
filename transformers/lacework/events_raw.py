import pandas as pd
import datapane as dp
import numpy as np

def events_raw(events, severities=["Critical", "High"], excluded_event_types=["CloudTrailDefaultAlert", "CloudActivityLogIngestionFailed", "NewViolations", "ComplianceChanged"]):
    df = pd.DataFrame(events)
    df = df.sort_values(by=['SEVERITY','START_TIME'],ascending=[True,False])
    df = df.replace({'SEVERITY': {"1": "Critical", "2": "High", "3": "Medium", "4": "Low", "5": "Info"}})
    df = df[df['SEVERITY'].isin(severities)]
    df = df[~df['EVENT_TYPE'].isin(excluded_event_types)]
    return dp.Table(df)