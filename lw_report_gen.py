import sys
import os
import argparse

import logzero

from modules.reportgen import ReportGenCSA
from laceworksdk import LaceworkClient


def get_arguments():
    parser = argparse.ArgumentParser(description=
                                     """Tool to generate a Lacework customer security assessment report.
                                     Requires that the Lacework CLI is installed and configured.
                                     https://docs.lacework.com/cli""")
    parser.add_argument("--report-path", help="Filename to save report", default="report.html")
    parser.add_argument("--author", help="Author of report", type=str, required=True)
    parser.add_argument("--customer", help="Customer Name (Company)", type=str, required=True)
    parser.add_argument("--cache", help="Create/use locally cached copies of Lacework data", action='store_true')
    return parser.parse_args()


def main():
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(os.path.abspath(__file__))

    args = get_arguments()
    logzero.loglevel(logzero.INFO)
    logzero.logfile('lw_report_gen.log')
    csa = ReportGenCSA(basedir, use_cache=args.cache)
    report = csa.generate(str(args.customer), str(args.author))
    with open(str(args.report_path), 'w') as file:
        file.write(report)


if __name__ == "__main__":
    main()
