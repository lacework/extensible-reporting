#!/usr/bin/env python3

import coloredlogs, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
coloredlogs.install(level='INFO',fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

from datetime import datetime, timezone, timedelta
import os

import argparse

import importlib.machinery
import importlib.util

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-path", help="Path to save report", default="report.html")
    parser.add_argument("--use-dummy-data", help="Use dummy data (if available)", action='store_true')
    parser.add_argument('report_generator', metavar='REPORT_GENERATOR', type=str, nargs=None,
                    help='Path to the report generator (eg: reports/datapane/compliance_report.py')
    args = parser.parse_args()
    
    report_path = os.path.join(os.path.dirname(__file__), args.report_generator)
    if not os.path.exists(report_path):
        logger.error(args.report_generator + ' does not exist')
        exit(1)

    logger.info('Loading report generator ' + report_path)

    # Import report
    loader = importlib.machinery.SourceFileLoader('report', report_path)
    spec = importlib.util.spec_from_loader('report', loader)
    report = importlib.util.module_from_spec(spec)
    loader.exec_module(report)

    class _shared:
        def __init__(self):
            import providers.lacework as p_lw
            import providers.lacework_dummy as p_lw_dummy
            import transformers.lacework as t_lw
            import graphics.lacework.plotly as g_lw_plotly

            self.p_lw = p_lw
            self.p_lw_dummy = p_lw_dummy
            self.t_lw = t_lw
            self.g_lw_plotly = g_lw_plotly 
            self._now = datetime.now(timezone.utc)
            self._25_hours_ago = self._now - timedelta(hours = 25)
            self._7_days_ago = self._now - timedelta(days = 7)
            self.use_dummy_data = args.use_dummy_data

    report.generate_report(_shared(), report_save_path=args.report_path, use_dummy_data=args.use_dummy_data)

main()