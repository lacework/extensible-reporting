#!/usr/bin/env python3
import datapane
import coloredlogs, logging, os
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger()
coloredlogs.install(level=LOGLEVEL,fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

from common import alert_new_release
alert_new_release()

from datetime import datetime, timezone, timedelta
import os
import sys
import argparse

import importlib.machinery
import importlib.util

# detect if in Pyinstaller package and build appropriate base directory path
if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
    
def main():
    parser = argparse.ArgumentParser(description=
    """Tool to generate a Lacework customer security assessment report.
    Requires that the Lacework CLI is installed and configured.
    https://docs.lacework.com/cli""")
    #parser.add_argument("--report-path", help="Filename to save report", default="report.html")
    parser.add_argument("--use-cached-data", help="Use cached data (if available)", action='store_true')
    parser.add_argument("--author", help="Author of report", type=str, required=True)
    parser.add_argument("--customer", help="Customer Name (Company)", type=str, required=True)
    args = parser.parse_args()
    # Hardcode the report
    csa_report = "reports/jinja2/csa_report.py"
    
    #generate a save file name for the report output html
    date = datetime.now().strftime("%m-%d-%y")
    report_save_path = f"CSA_Report_{str(args.customer).replace(' ', '_')}_{date}.html"
    print(f"Report will be saved to filename {report_save_path}")
    
    #generate a path to the report generator python
    report_path = os.path.join(basedir, csa_report)
    if not os.path.exists(report_path):
        logger.error(csa_report + ' does not exist')
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
            import providers.lacework_cached as p_lw_cached
            import providers.local_asset as p_local_asset
            import transformers.lacework as t_lw
            import graphics.lacework.plotly as g_lw_plotly
            import providers.local_asset as p_local_asset
            import common
            
            self.p_lw = p_lw
            self.p_lw_cached = p_lw_cached
            self.p_local_asset = p_local_asset
            self.t_lw = t_lw
            self.g_lw_plotly = g_lw_plotly
            self.common = common
            self._now = datetime.now(timezone.utc)
            self._25_hours_ago = self._now - timedelta(hours = 25)
            self._7_days_ago = self._now - timedelta(days = 7)
            self.use_cached_data = args.use_cached_data
            self.cli_data = {
                'customer': args.customer,
                'author': args.author
            }

    report.generate_report(_shared(), report_save_path=report_save_path, use_cached_data=args.use_cached_data)

if __name__ == "__main__":
    main()
