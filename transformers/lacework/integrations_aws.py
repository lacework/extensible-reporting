import pandas as pd
import datapane as dp
import numpy as np

def integrations_aws(integrations, types=["AWS_CFG", "AWS_CT_SQS"]):
    df = pd.json_normalize(integrations)
    df = df[df['TYPE'].isin(types)]
    df = df[['NAME', 'TYPE', 'ENABLED', 'STATE.ok', 'DATA.AWS_ACCOUNT_ID']]
    return df