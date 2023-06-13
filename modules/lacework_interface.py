import json

from laceworksdk import LaceworkClient
from laceworksdk import exceptions
from logzero import logger
from modules.host_vulnerabilities import HostVulnerabilities
from modules.container_vulnerabilities import ContainerVulnerabilities
from modules.alerts import Alerts
from modules.compliance import Compliance
from modules.utils import cache_results


class LaceworkInterface:

    def __init__(self, api_key_file=None, use_cache=False):
        if api_key_file:
            if 'subAccount' in api_key_file:
                self.lacework = LaceworkClient(account=api_key_file['account'],
                                               subaccount=api_key_file['subAccount'],
                                               api_key=api_key_file['keyId'],
                                               api_secret=api_key_file['secret']
                                               )
            else:
                self.lacework = LaceworkClient(account=api_key_file['account'],
                                               api_key=api_key_file['keyId'],
                                               api_secret=api_key_file['secret']
                                               )
        else:
            self.lacework = LaceworkClient()
        self.use_cache = use_cache
        self.compliance_provider_lookup = {'AWS': 'AwsCfg',
                                           'GCP': 'GcpCfg',
                                           'AZURE': 'AzureCfg'}
        self.compliance_report_lookup = {'AwsCfg':
                                             {'CIS': 'AWS_CIS_14',
                                              'PCI': 'AWS_PCI_DSS_3.2.1',
                                              },
                                         'AzureCfg':
                                             {'CIS': 'AZURE_CIS_1_5',
                                              'PCI': 'AZURE_PCI_DSS_3_2_1_CIS_1_5',
                                              },
                                         'GcpCfg':
                                             {'CIS': 'GCP_CIS13',
                                              'PCI': 'GCP_PCI_Rev2',
                                              }
                                         }

    def write_json_file(self, obj, name):
        with open(name, 'w') as f:
            json.dump(obj, f)

    @cache_results
    def get_cfg_account_ids(self):
        try:
            accounts = self.lacework.cloud_accounts.get()['data']
        except Exception as e:
            logger.error(f"Failed to retrieve list of cloud accounts from Lacework API:{str(e)}")
            raise e
        account_details = []
        config_accounts = [account for account in accounts if ("Cfg" in account['type'] and account['enabled'] == 1 and account['state']['ok'] is True)]
        for config_account in config_accounts:
            logger.debug(f"Found Account: {json.dumps(config_account['data'])}")
            if config_account['type'] == 'GcpCfg':
                #project_data = self.lacework.configs.gcp_projects.get()
                account_details.append({'name': config_account['name'],
                                        'type': config_account['type'],
                                        'primary_query_id': None,
                                        'secondary_query_id': config_account['data']['id'],
                                        })
            elif config_account['type'] == 'AzureCfg':
                tenant_data = self.lacework.configs.azure_subscriptions.get(tenantId=config_account['data']['tenantId'])['data']
                for subscription in tenant_data[0]['subscriptions']:
                    #logger.info(f"Adding tenant:{config_account['data']['tenantId']} Subscription:{str(subscription).split(' ')[0]}")
                    account_details.append({'name': config_account['name'],
                                            'type': config_account['type'],
                                            'primary_query_id': config_account['data']['tenantId'],
                                            'secondary_query_id': str(subscription).split(' ')[0],
                                            })
            elif config_account['type'] == 'AwsCfg':
                arn_elements = config_account['data']['crossAccountCredentials']['roleArn'].split(':')
                account_details.append({'name': config_account['name'],
                                        'type': config_account['type'],
                                        'primary_query_id': arn_elements[4],
                                        'secondary_query_id': None,
                                        })
        return account_details

    @cache_results
    def get_alerts(self, start_time, end_time):
        logger.debug(f'Getting alerts from {start_time} to {end_time}:')
        alerts_list = []
        try:
            raw_results = self.lacework.alerts.get(start_time=start_time, end_time=end_time)
        except Exception as e:
            logger.error(f"Failed to retrieve list of alerts from Lacework API:{str(e)}")
            raise e
        while True:
            alerts_list.extend(raw_results['data'])
            next_page_url = raw_results['paging']['urls']['nextPage']
            if next_page_url:
                raw_results = self.lacework._session.get(next_page_url).json()
            else:
                break
        logger.info(f'{len(alerts_list)} alerts returned.')
        alerts = Alerts(alerts_list)
        return alerts

    @cache_results
    def get_host_vulns(self, start_time, end_time, severities=("Critical", "High", "Medium")):
        results = []
        for severity in severities:
            filters = {
                "timeFilter": {
                    "startTime": start_time,
                    "endTime": end_time
                },
                "filters":
                    [
                        {
                            "field": "severity",
                            "expression": "eq",
                            "value": str(severity)
                        }
                    ]
                }
            logger.debug(f'Getting Host Vulns with following filters:{filters}')

            try:
                host_vulns = self.lacework.vulnerabilities.hosts.search(json=filters)
            except Exception as e:
                logger.error(f"Failed to retrieve list of host vulnerabilities from Lacework API:{str(e)}")
                raise e

            i = 1
            for page in host_vulns:
                logger.info('Saving page ' + str(i))
                i = i + 1
                results.extend(page['data'])
            if i > 100:
                logger.warning(
                    "Lacework API returned maximum pages of host vuln results (100 pages). Processed dataset is likely incomplete.")

        host_vulns = HostVulnerabilities(results)
        return host_vulns

    @cache_results
    def get_container_vulns(self, start_time, end_time, severities=("Critical", "High", "Medium")):
        results = []
        for severity in severities:
            filters = {
                "timeFilter": {
                    "startTime": start_time,
                    "endTime": end_time
                },
            "filters":
            [
                {
                    "field": "severity",
                    "expression": "eq",
                    "value": severity
                }
            ]
        }
            logger.debug(f'Getting Container Vulnerabilities with following filters:{filters}')
            try:
                container_vulns = self.lacework.vulnerabilities.containers.search(json=filters)
            except Exception as e:
                logger.error(f"Failed to retrieve list of container vulnerabilities from Lacework API:{str(e)}")
                raise e

            # logger.info('Found ' + len(container_vulns) + ' pages of data')
            i = 1
            for page in container_vulns:
                logger.info('Saving page ' + str(i))
                i = i + 1
                results.extend(page['data'])
            if i > 100:
                logger.warning(
                    "Lacework API returned maximum pages of container vuln results (100 pages). Processed dataset is likely incomplete.")

        container_vulns = ContainerVulnerabilities(results)
        return container_vulns

    @cache_results
    def get_compliance_reports(self, cloud_provider='AWS', report_type='CIS'):
        '''Retrieve all reports of specified type for specified cloud provider.
            Valid Cloud Providers are: AWS, GCP, AZURE
            Valid Report Types are: CIS, PCI
            '''
        compliance_reports = []
        compliance_provider = self.compliance_provider_lookup[str(cloud_provider).upper()]
        compliance_accounts = self.get_cfg_account_ids()
        for compliance_account in compliance_accounts:
            if compliance_account['type'] == compliance_provider:
                report_query_string = self.compliance_report_lookup[compliance_account['type']][report_type]
                logger.debug(f"Getting {report_query_string} report for {compliance_account}")
                try:
                    report = self.lacework.reports.get(primary_query_id=compliance_account['primary_query_id'],
                                                       secondary_query_id=compliance_account['secondary_query_id'],
                                                       format="json",
                                                       latest=True,
                                                       report_type=report_query_string)
                except Exception as e:
                    logger.error(f"Failed to retrieve {report_type} report for {cloud_provider} from Lacework API:{str(e)}")
                    raise e

                logger.info(f"{cloud_provider}:{report_type}:{compliance_account['primary_query_id']}:{compliance_account['secondary_query_id']}:"
                            f"Compliance Results:{len(report['data'][0]['recommendations']) if report['data'] else 0}")
                if report['data']:
                    compliance_reports.append(report['data'][0])
        results = Compliance({'cloud_provider': cloud_provider,
                              'report_type': report_type,
                              'reports': compliance_reports})
        return results






