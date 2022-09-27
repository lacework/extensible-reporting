#!/usr/bin/env python3

import coloredlogs, logging
logging.basicConfig(level=logging.INFO)
coloredlogs.install(level='INFO',fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

from datetime import datetime, timezone, timedelta
import providers.lacework as p_lw
import providers.lacework_cached as p_lw_cached

import transformers.lacework as t_lw

import argparse

_now = datetime.now(timezone.utc)
_25_hours_ago = _now - timedelta(hours = 25)
_7_days_ago = _now - timedelta(days = 7)

def main():
    sources = [
        'lw_compliance_reports',
        'lw_host_vulns',
        'lw_container_vulns',
        'lw_events',
        []
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument('sources', metavar='SOURCES', type=str, nargs='*', choices=sources, default=[], help='optional sources (lw_compliance_reports, lw_host_vulns, lw_container_vulns, lw_events)')
    args = parser.parse_args()

    args.sources = args.sources if args.sources else sources # lol

    if 'lw_compliance_reports' in args.sources:
        integrations = p_lw.integrations()
        p_lw_cached.save_data(integrations, "integrations")

        aws_config_accounts = t_lw.integrations_config_accounts(integrations)

        compliance_reports = p_lw.compliance_reports(accounts=aws_config_accounts)
        p_lw_cached.save_data(compliance_reports, "compliance_reports")

    if 'lw_host_vulns' in args.sources:
        host_vulns = p_lw.host_vulns(_25_hours_ago, _now)
        p_lw_cached.save_data(host_vulns, "host_vulns")
    
    if 'lw_container_vulns' in args.sources:
        container_vulns = p_lw.container_vulns(_25_hours_ago, _now)
        p_lw_cached.save_data(container_vulns, "container_vulns")

    if 'lw_events' in args.sources:
        events = p_lw.events(_7_days_ago, _now)
        p_lw_cached.save_data(events, "events")

    
main()