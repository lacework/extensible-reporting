import pandas as pd
import plotly.graph_objects as go
from logzero import logger


class Compliance:

    def __init__(self, data: dict):
        self.cloud_provider = data['cloud_provider']
        self.report_type = data['report_type']
        self.reports = data['reports']
        self.all_recommendations = self.get_all_recommendations()
        if self.cloud_provider == 'AWS':
            self.account_id_string = 'ACCOUNT_ID'
            self.account_id_rename_string = 'Account ID'
        if self.cloud_provider == 'AZURE':
            self.account_id_string = 'TENANT_ID'
            self.account_id_rename_string = 'Tenant ID'
        if self.cloud_provider == 'GCP':
            self.account_id_string = 'PROJECT_ID'
            self.account_id_rename_string = 'Project ID'

    def get_all_recommendations(self):
        results = []
        for entry in self.reports:
            report_type = entry['reportType']
            for recommendation in entry['recommendations']:
                results.append({**{'reportType': report_type}, **recommendation})
        return results

    def get_total_accounts_evaluated(self):
        df = pd.DataFrame(self.all_recommendations)
        unique_accounts = df[self.account_id_string].nunique()
        return unique_accounts

    def get_compliance_details(self, severities=["Critical", "High"]):
        df = pd.DataFrame(self.all_recommendations)
        df = df[df['STATUS'].isin(["NonCompliant"])]

        df['RESOURCE_COUNT'] = (df['VIOLATIONS'].str.len())

        df = df.sort_values(by=['SEVERITY', 'RESOURCE_COUNT'], ascending=[True, False])

        df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
        df = df[df['SEVERITY'].isin(severities)]

        df = df.reset_index()

        df['Resources'] = df['RESOURCE_COUNT'].astype('string') + " / " + df['ASSESSED_RESOURCE_COUNT'].astype('string')

        df = df[[self.account_id_string, 'CATEGORY', 'TITLE', 'SEVERITY', 'Resources']]
        df.rename(columns={self.account_id_string: self.account_id_rename_string, 'CATEGORY': 'Category',
                           'TITLE': 'Title', 'SEVERITY': 'Severity'},
                  inplace=True)

        return df

    def get_compliance_summary(self, severities=["Critical", "High"]):
        df = pd.DataFrame(self.all_recommendations)
        df = df[df['STATUS'].isin(["NonCompliant"])]

        df['RESOURCE_COUNT'] = (df['VIOLATIONS'].str.len())

        df = df.sort_values(by=['SEVERITY', 'RESOURCE_COUNT'], ascending=[True, False])

        df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
        df = df[df['SEVERITY'].isin(severities)]

        df = df.groupby([self.account_id_string, 'SEVERITY']).agg(count=('SEVERITY', 'count'),
                                                        resources=('RESOURCE_COUNT', 'sum'),
                                                        assessed=('ASSESSED_RESOURCE_COUNT',
                                                                  'sum')).reset_index()  # .size().reset_index(name='count')
        df['sev_merged'] = df['SEVERITY'].astype('string') + ": " + df['count'].astype('string')

        df = df.groupby(self.account_id_string).agg(
            {'sev_merged': f"\n".join, 'resources': 'sum', 'assessed': 'sum'}).reset_index()
        df.rename(
            columns={self.account_id_string: self.account_id_rename_string, 'sev_merged': 'Severity Count',
                     'resources': 'Non-compliant Resources','assessed': 'Total Assessed Resources'},
            inplace=True)


        return df

    def get_summary_by_account(self, severities=["Critical", "High", "Medium", "Low"]):
        df = pd.DataFrame(self.all_recommendations)
        df = df[df['STATUS'].isin(["NonCompliant"])]
        df['RESOURCE_COUNT'] = (df['VIOLATIONS'].str.len())
        # sort to determine account order, while we still have the severity & resource count data
        df = df.sort_values(by=['SEVERITY', 'RESOURCE_COUNT'], ascending=[True, False])
        account_order = df[self.account_id_string].unique()


        # group
        df = df.groupby([self.account_id_string, 'SEVERITY']).agg(failed_control_count=('SEVERITY', 'count'),
                                                        failed_resources=('RESOURCE_COUNT', 'sum')).reset_index()

        # sort by accounts with most criticals, followed by most highs
        df[self.account_id_string] = pd.Categorical(df[self.account_id_string], account_order)
        df.sort_values(by=[self.account_id_string, 'SEVERITY'], ascending=True)

        # convert int and filter severities
        df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
        df = df[df['SEVERITY'].isin(severities)]

        # rename
        df.rename(
            columns={self.account_id_string: self.account_id_rename_string, 'SEVERITY': 'Severity', 'failed_resources': 'Non-compliant Resources',
                     'failed_control_count': 'Failed controls'}, inplace=True)

        # pivot and preseve severity order (pivot breaks this)
        severity_order = df['Severity'].unique()
        df = pd.pivot_table(df, values='Non-compliant Resources', index=self.account_id_rename_string, columns='Severity', sort=False)
        df = df.reindex(severity_order, axis=1)

        return df

    def get_summary_by_service(self, severities=["Critical", "High", "Medium", "Low"]):
        df = pd.DataFrame(self.all_recommendations)
        df = df[df['STATUS'].isin(["NonCompliant"])]
        df = df.replace({'SEVERITY': {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Info"}})
        df = df[df['SEVERITY'].isin(severities)]

        df['RESOURCE_COUNT'] = (df['VIOLATIONS'].str.len())

        df = df.reset_index()

        df = df[[self.account_id_string, 'CATEGORY', 'SEVERITY', 'RESOURCE_COUNT']]

        # group by acct id, category
        df = df.groupby([self.account_id_string, 'CATEGORY']).agg(count=('RESOURCE_COUNT', 'sum')).reset_index()

        # determine category order
        df_category_order = df.groupby(['CATEGORY']).agg(count=('count', 'sum')).reset_index()
        df_category_order.sort_values('count', ascending=False, inplace=True)
        df_category_order = df_category_order['CATEGORY'].unique()
        df = df.astype({'CATEGORY': pd.CategoricalDtype(df_category_order, ordered=True)})

        # create pivot table
        df = pd.pivot_table(df, values='count', index=self.account_id_string, columns='CATEGORY', sort=False)
        return df

    def get_summary_by_account_bar_graph(self, width=600, height=350, format='svg'):
        df = self.get_summary_by_account()
        colors = [
            'crimson',
            'darkorange',
            'gold',
            'lightskyblue',
            'powderblue'
        ]
        unique_accounts = len(df.index)
        # acct_id, criticals, highs, mediums, lows, infos

        if unique_accounts == 1:
            fig = go.Figure(go.Bar(name="asdf", x=df.columns, y=df.iloc[0], marker_color=colors))
            fig.update_layout(
                title='Compliance Severities Found',
                yaxis=dict(
                    title='Failed resources'
                )
            )
        else:
            severities = df.columns
            graph_data = []

            for idx, sev in enumerate(severities):
                bar = go.Bar(name=sev, x=df.index, y=df[sev], marker_color=colors[idx])
                graph_data.append(bar)

            fig = go.Figure(
                data=graph_data[::-1]
            )

            fig.update_layout(
                title='Compliance Severities by Account',
                yaxis=dict(
                    title='Failed resources'
                ),
                barmode='stack'
            )

        img_bytes = fig.to_image(format=format, width=width, height=height)
        return img_bytes

    def get_summary_by_service_bar_graph(self, width=600, height=350, format='svg'):
        df = self.get_summary_by_service()
        # colors = [
        # 	'crimson',
        # 	'darkorange',
        # 	'gold',
        # 	'lightskyblue',
        # 	'powderblue'
        # ]
        categories = df.columns
        graph_data = []
        for acct, data in df.iterrows():
            bar = go.Bar(name=acct, x=categories, y=data)
            graph_data.append(bar)

        fig = go.Figure(
            data=graph_data
        )
        fig.update_layout(
            title='Compliance Severities by Service',
            yaxis=dict(
                title='Failed resources'
            ),
            barmode='group'
        )
        img_bytes = fig.to_image(format=format, width=width, height=height)
        return img_bytes