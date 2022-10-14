import pandas as pd
import datapane as dp
import numpy as np

def compliance_reports_summary_by_service_for_graphic(compliance_reports, severities=["Critical", "High", "Medium", "Low"]):

    df = pd.DataFrame(compliance_reports)
    df = df[df['STATUS'].isin(["NonCompliant"])]
    
    df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
    df = df[df['SEVERITY'].isin(severities)]
    
    df = df.reset_index()

    df = df[['ACCOUNT_ID', 'CATEGORY', 'SEVERITY', 'RESOURCE_COUNT']]
    
    # group by acct id, category
    df = df.groupby(['ACCOUNT_ID', 'CATEGORY']).agg(count=('RESOURCE_COUNT', 'sum')).reset_index()
    
    # determine category order
    df_category_order = df.groupby(['CATEGORY']).agg(count=('count', 'sum')).reset_index()
    df_category_order.sort_values('count', ascending=False, inplace=True)
    df_category_order = df_category_order['CATEGORY'].unique()
    df = df.astype({'CATEGORY' : pd.CategoricalDtype(df_category_order, ordered = True)})
    
    # create pivot table
    df = pd.pivot_table(df, values='count', index='ACCOUNT_ID', columns='CATEGORY', sort=False)
    
    return df
