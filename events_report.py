from datetime import datetime, timezone, timedelta
import providers.lacework as p_lw
import providers.lacework_dummy as p_lw_dummy

import transformers.lacework as t_lw

import datapane as dp

_now = datetime.now(timezone.utc)
_25_hours_ago = _now - timedelta(hours = 25)
_7_days_ago = _now - timedelta(days = 7)

def main():

    events = p_lw_dummy.events(_7_days_ago, _now)
    
    report = dp.Report(
        "## Events Raw",
        t_lw.events_raw(events,severities=["Critical", "High", "Medium"])
    )

    report.save(path="events-report.html")
    
main()