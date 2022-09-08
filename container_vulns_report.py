from datetime import datetime, timezone, timedelta
import providers.lacework as p_lw
import providers.lacework_dummy as p_lw_dummy

import transformers.lacework as t_lw

import pandas as pd
import datapane as dp

_now = datetime.now(timezone.utc)
_25_hours_ago = _now - timedelta(hours = 25)
_7_days_ago = _now - timedelta(days = 7)

def main():

    container_vulns = p_lw_dummy.container_vulns(_25_hours_ago,_now)
    report = dp.Report(
        "## Summary by Severity",
        t_lw.container_vulns_summary(container_vulns),
        "## Breakdown by Image",
        t_lw.container_vulns_summary_by_image(container_vulns),
    )

    report.save(path="container-vulns-report.html")
    
main()