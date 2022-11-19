import logging
logger = logging.getLogger(__name__)

from . import lw
from . import LWApiError

import json

def compliance_reports(accounts=[],report_types=['AWS_CIS_S3', 'AWS_CIS_14']): # select both legacy & new CIS report
    results = {}
    for aws_account in accounts:
        results[aws_account] = []
        for report_type in report_types:
            try:
                logger.info('Getting ' + report_type + ' compliance report for aws account: ' + aws_account)
                a = lw().reports.get(
                    primary_query_id=aws_account,
                    type="COMPLIANCE",
                    report_type=report_type, # AWS_SOC_Rev2, # AWS_SOC_Rev2, # AWS_CIS_14, # AWS_CIS_S3
                    format="json",
                    latest=True
                )

                report = a['data'][0]
                recommendations = report['recommendations']
                reportType = report['reportType']
                
                rows = []
                for row in recommendations:
                    row['reportType']= reportType
                    rows.append(row)

                results[aws_account].append(rows)
                
            except LWApiError:
                logger.warning('Could not get compliance report')
                continue

    return results

def compliance_reports_azure(azure_tenant_ids ='',lw_provider={}):
    results = {}
    
    for tenant in azure_tenant_ids:
        # get Azure subscriptions
        azure_subscriptions = lw_provider.azure_subscriptions(tenant_id=tenant)

        for azure_subscription in azure_subscriptions:
            sub_id = azure_subscription[:36]
            results[sub_id] = []
            try:
                logger.info('Getting compliance report for Azure subscription: ' + azure_subscription)
                a = lw().reports.get(
                    primary_query_id=tenant,
                    secondary_query_id=sub_id,
                    type="COMPLIANCE",
                    report_type="AZURE_CIS", # AZURE_CIS, # AZURE_CIS_131"
                    format="json",
                    latest=True
                )

                report = a['data'][0]
                recommendations = report['recommendations']
                reportType = report['reportType']
            
                rows = []
                for row in recommendations:
                    row['reportType']= reportType
                    rows.append(row)

                results[sub_id].append(rows)
            
            except LWApiError:
                logger.warning('Could not get compliance report for Azure subscription: ' + azure_subscription)
                continue
       
    return results