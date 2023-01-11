import pandas as pd
import datapane as dp
import numpy as np

def integrations_config_accounts(integrations, types=["AWS_CFG", "AWS_CT_SQS"]):
    df = pd.json_normalize(integrations)
    df = df[(df['type'] == "AwsCfg") & (df['enabled'] == 1) & (df['state.ok'] == True)]
    if df.empty:
        return []
    return df['data.awsAccountId'].unique().tolist()