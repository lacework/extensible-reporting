import logging
logger = logging.getLogger(__name__)

from . import lw
from . import LWApiError

import json

def compliance_reports(accounts=[]):
    results = []
    for aws_account in accounts:
        try:
            logger.info('Getting compliance report for aws account: ' + aws_account)
            a = lw().compliance.get_latest_aws_report(aws_account_id=aws_account, file_format="json")
        except LWApiError:
            logger.warning('Could not get compliance report for aws account: ' + aws_account)
        results.extend(a['data'])

    rows = []
  
    for report in results:
        recommendations = report['recommendations']
        reportType = report['reportType']
          
        for row in recommendations:
            row['reportType']= reportType
            rows.append(row)

    return rows
