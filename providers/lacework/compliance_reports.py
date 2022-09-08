from . import lw
import json

def compliance_reports(accounts=[]):
    results = []
    for aws_account in accounts:
        a = lw.compliance.get_latest_aws_report(aws_account_id=aws_account, file_format="json")
        results.extend(a['data'])
    return results
