import pandas as pd
import datapane as dp
import numpy as np

def integrations_config_accounts_azure(integrations, types=["'AZURE_CFG'", "AZURE_AL_SEQ"]):
    df = pd.json_normalize(integrations)
    df = df[(df['TYPE'] == "AZURE_CFG") & (df['ENABLED'] == 1) & (df['STATE.ok'] == 1)]

    if len(df) != 0 :
         return df['DATA.TENANT_ID'].unique().tolist()
    else :
        return False