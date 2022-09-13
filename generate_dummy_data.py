import coloredlogs, logging
logging.basicConfig(level=logging.INFO)
coloredlogs.install(level='INFO',fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

from datetime import datetime, timezone, timedelta
import providers.lacework as p_lw
import providers.lacework_dummy as p_lw_dummy

import transformers.lacework as t_lw

_now = datetime.now(timezone.utc)
_25_hours_ago = _now - timedelta(hours = 25)
_7_days_ago = _now - timedelta(days = 7)

def main():
    # integrations = p_lw.integrations()
    # p_lw_dummy.save_data(integrations, "integrations")

    # aws_config_accounts = t_lw.integrations_config_accounts(integrations)

    # compliance_reports = p_lw.compliance_reports(accounts=aws_config_accounts)
    # p_lw_dummy.save_data(compliance_reports, "compliance_reports")

    # host_vulns = p_lw.host_vulns(_25_hours_ago, _now)
    # p_lw_dummy.save_data(host_vulns, "host_vulns")
    
    events = p_lw.events(_7_days_ago, _now)
    p_lw_dummy.save_data(events, "events")
    
    container_vulns = p_lw.container_vulns(_25_hours_ago, _now)
    p_lw_dummy.save_data(container_vulns, "container_vulns")

main()