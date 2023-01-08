import pandas as pd
import datapane as dp
import numpy as np

def compliance_reports_total_accounts_evaluated(compliance_reports):
    df = pd.DataFrame(compliance_reports)

    unique_accounts = df['ACCOUNT_ID'].nunique()

    return unique_accounts

def compliance_reports_total_accounts_evaluated_azure(compliance_reports):
    df = pd.DataFrame(compliance_reports)

    unique_accounts = df['SUBSCRIPTION_ID'].nunique()

    return unique_accounts
