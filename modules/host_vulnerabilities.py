import pandas as pd
import plotly.graph_objects as go
from logzero import logger
import json


class HostVulnerabilities:

    def __init__(self, raw_data):
        self.data = raw_data

    def total_evaluated(self):
        df = pd.DataFrame(self.data)
        # count severities by host & total sum
        unique_hosts = df.mid.nunique()
        return unique_hosts

    def summary_by_host(self, severities=("Critical", "High", "Medium", "Low"), limit=False):
        df = pd.json_normalize(self.data,
                               meta=[['cveProps', 'metadata'], ['evalCtx', 'hostname'], ['featureKey', 'name'],
                                     'vulnId', 'severity', 'mid'])

        if 'severity' not in df:
            df['severity'] = False

        # filter
        df = df[df['severity'].isin(severities)]

        # delete extra columns
        df = df[['evalCtx.hostname', 'mid', 'severity']]

        # count severities by MID
        df = df.groupby(['mid', 'severity', 'evalCtx.hostname']).size().reset_index(name='count')

        # summarize severities onto one column (and sort)
        df['sev_merged'] = df['severity'].astype('string') + ": " + df['count'].astype('string')
        df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
        df = df.sort_values(by=['severity', 'count'], ascending=[True, False])
        df = df.groupby('mid', sort=False, as_index=False).agg(
            {'mid': 'first', 'evalCtx.hostname': 'first', 'sev_merged': f"\n".join})

        # clean names
        df.rename(columns={'mid': 'Machine ID', 'evalCtx.hostname': 'Hostname', 'sev_merged': 'Severity Count'},
                  inplace=True)
        df = df.drop(columns=['Machine ID'])

        if limit:
            df = df.head(limit)
        return df

    def fixable_vulns(self, severities=("Critical", "High"), limit=False):
        df = pd.json_normalize(self.data,
                               meta=[['evalCtx', 'hostname'],
                                     ['featureKey', 'name'],
                                     'vulnId',
                                     'severity',
                                     ['fixInfo', 'fix_available'],
                                     ['fixInfo', 'fixed_version'],
                                     ['featureKey', 'version_installed']])
        if 'severity' not in df:
            df['severity'] = False
        df = df[df['severity'].isin(severities)]
        df = df[df['fixInfo.fix_available'] == '1']
        if not df.empty:
            #cve_count = df.groupby('evalCtx.hostname')['vulnId'].nunique()
            #print(cve_count)
            df = df[['evalCtx.hostname', 'severity', 'vulnId', 'featureKey.name', 'featureKey.version_installed', 'fixInfo.fixed_version']]
            # df = df.groupby(['evalCtx.hostname', 'featureKey.name', 'featureKey.version_installed', 'severity', 'vulnId'],
            #                 as_index=False).agg({'fixInfo.fixed_version': ', '.join})
            df = df.groupby(['evalCtx.hostname', 'severity', 'vulnId', 'featureKey.name', 'featureKey.version_installed'],
                            as_index=False).agg(pd.unique).applymap(lambda x: x[0] if len(x) == 1 else x)
            print(df)
            df = df.groupby(['evalCtx.hostname', 'severity', 'featureKey.name', 'fixInfo.fixed_version','featureKey.version_installed' ], as_index=False).agg({'vulnId': ', '.join})
            # rename columns
            df.rename(columns={'evalCtx.hostname': 'Hostname',
                               'severity': 'Severity',
                               'vulnId': 'CVE',
                               'featureKey.name': 'Package Name',
                               "fixInfo.fixed_version": "Fixed Version(s)",
                               'featureKey.version_installed': "Installed Version"},
                      inplace=True)
            df = df[['Hostname', 'CVE', 'Severity', 'Package Name', 'Installed Version', 'Fixed Version(s)']]
        return df

    def summary(self, severities=("Critical", "High", "Medium", "Low")):
        df = pd.json_normalize(self.data,
                               meta=[['evalCtx', 'hostname'], ['featureKey', 'name'], 'vulnId', 'severity', 'mid'])

        if 'severity' not in df:
            df['severity'] = False

        # filter
        df = df[df['severity'].isin(severities)]

        # delete extra columns
        df = df[['evalCtx.hostname', 'mid', 'severity']]

        # count severities by host & total sum
        df = df.groupby(['severity'], as_index=False)['mid'].agg(['count', 'nunique'])

        for severity in severities:
            if not severity in df.index: df = pd.concat(
                [df, pd.DataFrame([{'severity': severity, 'count': 0, 'nunique': 0}]).set_index('severity')])

        df = df.reset_index()

        # sort
        df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
        df = df.sort_values(by=['severity'])
        df = df.reset_index()
        df = df.drop(columns=['index'])

        # rename columns
        df.rename(columns={'severity': 'Severity', 'count': 'Total CVEs', 'nunique': 'Hosts Affected'}, inplace=True)

        return df

    def host_vulns_by_severity_bar(self, severities=["Critical", "High", "Medium", "Low"], width=600, height=350, format='svg'):
        df = self.summary(severities=severities)

        colors = [
            'crimson',
            'darkorange',
            'gold',
            'lightskyblue'
        ]

        # Use textposition='auto' for direct text
        fig = go.Figure(data=[go.Bar(x=df['Severity'], y=df['Total CVEs'], marker_color=colors)])

        fig.update_layout(
            title='Host Severities by CVE',
            yaxis=dict(
                title='Number of CVEs'
            )
        )

        img_bytes = fig.to_image(format=format, width=width, height=height)
        return img_bytes