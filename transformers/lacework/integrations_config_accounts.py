import pandas as pd
import datapane as dp
import numpy as np

def integrations_config_accounts(integrations, types=["AWS_CFG", "AWS_CT_SQS"]):
    df = pd.json_normalize(integrations)
    df = df[(df['TYPE'] == "AWS_CFG") & (df['ENABLED'] == 1) & (df['STATE.ok'] == 1)]
    return df['DATA.AWS_ACCOUNT_ID'].unique().tolist()