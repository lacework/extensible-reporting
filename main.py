from datetime import datetime, timezone, timedelta
import providers.lacework as p_lw
import providers.lacework_dummy as p_lw_dummy

import transformers.lacework as t_lw

import datapane as dp


_now = datetime.now(timezone.utc)
_25_hours_ago = _now - timedelta(hours = 25)
_7_days_ago = _now - timedelta(days = 7)

def main():

    # events = p_lw_dummy.events(_25_hours_ago, _now)
    # print(len(events))
    # print(events['data'][0])

    host_vulns = p_lw_dummy.host_vulns(_25_hours_ago, _now)
    # report = dp.Report(t_lw.host_vulns_full_table(host_vulns))
    report = dp.Report(t_lw.host_vulns_summary(host_vulns))
    #report = dp.Report(t_lw.host_vulns_summary_by_host(host_vulns))
    report.save(path="simple-report.html")

    # container_vulns = p_lw_dummy.container_vulns(_25_hours_ago, _now)
    
main()