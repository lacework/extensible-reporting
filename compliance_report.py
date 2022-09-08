from datetime import datetime, timezone, timedelta
import providers.lacework as p_lw
import providers.lacework_dummy as p_lw_dummy

import transformers.lacework as t_lw

import datapane as dp

_now = datetime.now(timezone.utc)
_25_hours_ago = _now - timedelta(hours = 25)
_7_days_ago = _now - timedelta(days = 7)

def main():

    compliance_reports = p_lw_dummy.compliance_reports(accounts=['181778024219','580771763063'])
    report = dp.Report(
        "## Compliance Report Raw",
        t_lw.compliance_reports_raw(compliance_reports)
    )

    report.save(path="compliance-report.html")
    
main()