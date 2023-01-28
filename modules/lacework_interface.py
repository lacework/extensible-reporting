from laceworksdk import LaceworkClient
from laceworksdk import exceptions
from logzero import logger
from modules.host_vulnerabilities import HostVulnerabilities
from modules.container_vulnerabilities import ContainerVulnerabilities
from modules.alerts import Alerts
from modules.compliance import Compliance
import functools
import pickle
import requests
from pathlib import Path
import json


def cache_results(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        use_cache = args[0].use_cache
        if use_cache:
            func_name = func.__name__
            file_path = Path(f"lw_csa_{func_name}.cache")
            if file_path.is_file():
                try:
                    logger.info(f"Reading cache file {str(file_path)}")
                    with file_path.open("rb") as f:
                        result = pickle.load(f)
                except Exception as e:
                    logger.error(f"Cache file {str(file_path)} exists but could not be loaded: {str(e)}")
                    result = func(*args, **kwargs)
                    with file_path.open("wb") as f:
                        pickle.dump(result, f)
            else:
                result = func(*args, **kwargs)
                logger.info(f"Writing cache file {str(file_path)}. You must delete this file manually to generate a new cache.")
                with file_path.open("wb") as f:
                    pickle.dump(result, f)
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper


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
        self.compliance_report_lookup = {'AwsCfg':
                                             {'CIS': 'AWS_CIS_14',
                                              'PCI': 'AWS_PCI_DSS_3.2.1',
                                              },
                                         'AzureCfg':
                                             {'CIS': 'AZURE_CIS_1_5',
                                              'PCI': 'AZURE_PCI_DSS_3_2_1_CIS_1_5',
                                              },
                                         'GcpCfg':
                                             {'CIS': 'GCP_CIS',
                                              'PCI': 'GCP_PCI_Rev2',
                                              }
                                         }

    @cache_results
    def get_cfg_account_ids(self):
        accounts = self.lacework.cloud_accounts.get()['data']
        account_details = []
        config_accounts = [account for account in accounts if ("Cfg" in account['type'] and account['enabled'] == 1 and account['state']['ok'] is True)]
        for config_account in config_accounts:
            if config_account['type'] == 'GcpCfg':
                account_details.append({'name': config_account['name'],
                                        'type': config_account['type'],
                                        'primary_query_id': None,
                                        'secondary_query_id': config_account['data']['id'],
                                        })
            elif config_account['type'] == 'AzureCfg':
                tenant_data = self.lacework.configs.azure_subscriptions.get(tenantId=config_account['data']['tenantId'])['data']
                for subscription in tenant_data[0]['subscriptions']:
                    logger.info(f"Adding tenant:{config_account['data']['tenantId']} Subscription:{str(subscription).split(' ')[0]}")
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
        logger.info(f'Getting alerts from {start_time} to {end_time}:')
        alerts_list = []
        raw_results = self.lacework.alerts.get(start_time=start_time, end_time=end_time)
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
    def get_host_vulns(self, start_time, end_time):
        filters = {
            "timeFilters": {
                "startTime": start_time,
                "endTime": end_time
            }
        }
        logger.info('Getting Host Vulns with following filters:')
        logger.info(filters)
        host_vulns = self.lacework.vulnerabilities.hosts.search(json=filters)
        results = []
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
    def get_container_vulns(self, start_time, end_time, severities=["Critical", "High"]):
        filters = {
            "timeFilters": {
                "startTime": start_time,
                "endTime": end_time
            },
            "filters": [
                {"field": "status", "expression": "eq", "value": "VULNERABLE"},
                {
                    "field": "severity",
                    "expression": "in",
                    "values": severities,
                }
            ]
        }
        logger.info('Getting Container Vulnerabilities with following filters:')
        logger.info(filters)
        container_vulns = self.lacework.vulnerabilities.containers.search(json=filters)
        results = []
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
    def get_compliance_reports(self, report_type='CIS'):
        compliance_reports = []
        compliance_accounts = self.get_cfg_account_ids()
        for compliance_account in compliance_accounts:
            # skipping Azure and GCP for now due to API issues
            if compliance_account['type'] == "AzureCfg" or compliance_account['type'] == "GcpCfg": continue
            #if compliance_account['type'] == "GcpCfg": continue
            report_query_string = self.compliance_report_lookup[compliance_account['type']][report_type]
            logger.info(f"Getting {report_query_string} report for {compliance_account}")
            report = self.lacework.reports.get(primary_query_id=compliance_account['primary_query_id'],
                                               secondary_query_id=compliance_account['secondary_query_id'],
                                               format="json",
                                               latest=True,
                                               report_type=report_query_string)
            if report['data']:
                compliance_reports.append(report['data'][0])
                # compliance_reports.append({'type': compliance_account['type'],
                #                            'primary_query_id': compliance_account['primary_query_id'],
                #                            'secondary_query_id': compliance_account['secondary_query_id'],
                #                            'report': report
                #                            })
        compliance_reports = Compliance(compliance_reports)
        return compliance_reports






