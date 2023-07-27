import json

import pandas as pd
from logzero import logger


class ContainerVulnerabilities:

    def __init__(self, raw_data):
        self.data = raw_data

    def total_evaluated(self):
        df = pd.DataFrame(self.data)
        unique_containers = df['imageId'].nunique()
        return unique_containers

    def summary_by_image(self, severities=["Critical", "High", "Medium", "Low"], limit=False):
        df = pd.json_normalize(self.data, meta=[['evalCtx', 'image_info', 'repo'], ['evalCtx', 'image_info', 'tags'],
                                                      ['featureKey', 'name'], ['fixInfo', 'fix_available'], 'vulnId',
                                                      'severity', 'imageId'])

        # delete extra columns
        df = df[['evalCtx.image_info.repo', 'evalCtx.image_info.tags', 'featureKey.name', 'fixInfo.fix_available', 'vulnId',
                 'severity', 'imageId']]

        # filter
        df = df[df['severity'].isin(severities)]

        # combine repo and tags into newline separated repo_tag
        df['repo_tags'] = df.apply(
            lambda y: "\n".join(list(map(lambda x: y['evalCtx.image_info.repo'] + ':' + x, y['evalCtx.image_info.tags']))),
            axis=1)
        df.drop(columns=['evalCtx.image_info.tags'], inplace=True)
        df.drop_duplicates(inplace=True)

        # assemble multiple repos / tags into one line per imageid
        df = df.groupby(['imageId', 'vulnId', 'featureKey.name']).agg(repositories=('repo_tags', f"\n".join),
                                                                      fix_available=('fixInfo.fix_available', 'first'),
                                                                      severity=('severity', 'first')).reset_index()

        # count by severity
        df = df.groupby(['imageId', 'severity']).agg(repositories=('repositories', 'first'),
                                                     count=('vulnId', 'count')).reset_index()

        # sort and concat severities
        df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
        df['sev_merged'] = df['severity'].astype('string') + ": " + df['count'].astype('string')
        df = df.sort_values(by=['severity', 'count'], ascending=[True, False])
        df = df.groupby('imageId', sort=False).agg(repositories=('repositories', 'first'),
                                                   severities=('sev_merged', f"\n".join)).reset_index()

        # reorder
        df = df[['repositories', 'severities', 'imageId']]

        # clean names
        df.rename(columns={'imageId': 'Image ID', 'repositories': 'Repository / Tag', 'severities': 'CVE Count'},
                  inplace=True)

        if limit:
            df = df.head(limit)
        return df

    def fixable_vulns(self, severities=("Critical", "High"), limit=False):
        df = pd.json_normalize(self.data,
                               meta=[['evalCtx', 'image_info', 'repo'],
                                     'imageId',
                                     ['featureKey', 'name'],
                                     'vulnId',
                                     'severity',
                                     ['fixInfo', 'fix_available'],
                                     ['fixInfo', 'fixed_version'],
                                     ['featureKey', 'version']])
        if 'severity' not in df:
            df['severity'] = False
        df = df[df['severity'].isin(severities)]
        df = df[df['fixInfo.fix_available'] == 1]
        if not df.empty:
            df = df[['evalCtx.image_info.repo', 'imageId', 'severity', 'featureKey.name', 'featureKey.version', 'vulnId', 'fixInfo.fixed_version']]
            df = df.groupby(['evalCtx.image_info.repo', 'imageId', 'severity', 'featureKey.name', 'featureKey.version', 'vulnId'],
                            as_index=False).agg(pd.unique).applymap(lambda x: x[0] if len(x) == 1 else x)
            df = df.groupby(['evalCtx.image_info.repo', 'imageId', 'severity', 'featureKey.name', 'fixInfo.fixed_version', 'featureKey.version'], as_index=False).agg({'vulnId': ', '.join})

            df.rename(columns={'evalCtx.image_info.repo': 'Repository',
                               'imageId': 'Image ID',
                               'severity': 'Severity',
                               'vulnId': 'CVE',
                               'featureKey.name': 'Package Name',
                               "fixInfo.fixed_version": "Fixed Version(s)",
                               'featureKey.version': "Installed Version"},
                      inplace=True)
            # re-order the columns
            df = df[['Repository', 'Image ID', 'CVE', 'Severity', 'Package Name', 'Installed Version', 'Fixed Version(s)']]
        return df

    def summary(self, severities=["Critical", "High", "Medium", "Low"]):
        df = pd.json_normalize(self.data,
                               meta=[['evalCtx', 'image_info', 'repo'], ['featureKey', 'name'], 'vulnId', 'severity',
                                     'imageId'])

        # filter
        df = df[df['severity'].isin(severities)]

        # delete extra columns
        df = df[['imageId', 'severity', 'vulnId', 'featureKey.name']]
        df.drop_duplicates(inplace=True)

        # count severities by host & total sum
        df = df.groupby(['severity'])['imageId'].agg(['count', 'nunique'])
        for severity in severities:
            if not severity in df.index: df = pd.concat(
                [df, pd.DataFrame([{'severity': severity, 'count': 0, 'nunique': 0}]).set_index('severity')])

        df = df.reset_index()

        # sort
        df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
        df = df.sort_values(by=['severity'])

        # rename columns
        df.rename(columns={'severity': 'Severity', 'count': 'Total CVEs', 'nunique': 'Images Affected'}, inplace=True)
        df = df.reset_index(drop=True)

        return df

    def summary_by_package(self, severities=["Critical", "High", "Medium", "Low"]):
        df = pd.json_normalize(self.data, meta=[['featureKey', 'name'], 'vulnId', 'severity', 'imageId'])

        # clean and santiize
        df.rename(columns={'featureKey.name': 'packageName'}, inplace=True)
        df = df[['packageName', 'imageId', 'vulnId', 'severity']]
        df.drop_duplicates(inplace=True)

        # filter
        df = df[df['severity'].isin(severities)]

        # add image count by package
        df_image_count_by_package = df.loc[:, ('imageId', 'packageName')]
        df_image_count_by_package.drop_duplicates(inplace=True)
        df_image_count_by_package = df_image_count_by_package.groupby(['packageName']).agg(
            imageCount=('imageId', 'count')).reset_index()

        df = df.groupby(['packageName', 'severity']).agg(cveCount=('vulnId', 'count')).reset_index()

        # sort by critical
        df['severity'] = pd.Categorical(df['severity'], ["Critical", "High", "Medium", "Low", "Info"])
        df = df.sort_values(by=['severity', 'cveCount'], ascending=[True, False])

        # add combined column
        df['sev_merged'] = df['severity'].astype('string') + ": " + df['cveCount'].astype('string')

        # group by package and count total cves
        df = df.groupby('packageName', sort=False).agg(severities=('sev_merged', f", ".join)).reset_index()

        # combine package and severities
        df['Package Info'] = df['packageName'].astype('string') + "\n" + df['severities'].astype('string')

        df = df.merge(df_image_count_by_package, how='left')
        df.rename(columns={'imageCount': 'Count'}, inplace=True)

        # reorder and strip unneeded columns
        df = df[['Package Info', 'Count']]
        df['Package Info'] = df['Package Info'].str.replace("\n",'<br>')

        return df

    def top_packages_bar(self, width=600, height=350, format='svg', limit: int = 10):
        df = self.summary_by_package().head(limit)
        import plotly.graph_objects as go

        # Use textposition='auto' for direct text
        fig = go.Figure(data=[go.Bar(x=df['Package Info'], y=df['Count'])])
        fig.update_layout(
            title='High Priority Packages to Patch (by CVE Count)',
            yaxis=dict(
                title='Number of Affected Images'
            ),
            xaxis_tickangle=45
        )
        img_bytes = fig.to_image(format=format, width=width, height=height)
        return img_bytes