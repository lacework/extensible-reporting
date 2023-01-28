import sys
import os
import json
import logzero
from logzero import logger
from modules.utils import get_validated_arguments
from modules.reportgen import ReportGenCSA
from modules.utils import LaceworkTime


def main():

    # Get the base directory where this script is running from
    # Required for Pyinstaller as it temporarily extracts all files to a temp folder before running
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(os.path.abspath(__file__))

    # Set up default logging level
    logzero.loglevel(logzero.INFO)
    logzero.logfile('lw_report_gen.log')

    # Get command line args and process them
    args = get_validated_arguments()
    vulns_start_time = LaceworkTime(args.vulns_start_time)
    vulns_end_time = LaceworkTime(args.vulns_end_time)
    alerts_start_time = LaceworkTime(args.alerts_start_time)
    alerts_end_time = LaceworkTime(args.alerts_end_time)
    api_key_file = None
    if args.api_key_file:
        try:
            with open(args.api_key_file, 'r') as file:
                api_key_file = json.load(file)
        except Exception as e:
            logger.error(f"Failed to read keyfile: {str(e)}")
            sys.exit()




    # Execute the CSA report
    csa = ReportGenCSA(basedir, use_cache=args.cache_data, api_key_file=api_key_file)
    report = csa.generate(args.customer,
                          args.author,
                          vulns_start_time=vulns_start_time,
                          vulns_end_time=vulns_end_time,
                          alerts_start_time=alerts_start_time,
                          alerts_end_time=alerts_end_time)

    # Write out the report file
    with open(str(args.report_path), 'w') as file:
        file.write(report)


if __name__ == "__main__":
    main()
