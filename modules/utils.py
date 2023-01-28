from datetime import datetime, timezone, timedelta
import re
import argparse
import sys
import os
from logzero import logger


class LaceworkTime:

    def __init__(self, time_input: str):
        days_and_hours = time_input.split(":")
        self.delta_hours: int = int(days_and_hours[1])
        self.delta_days: int = int(days_and_hours[0])

    def generate_time_string(self) -> str:
        return (datetime.now(timezone.utc) - timedelta(days=self.delta_days, hours=self.delta_hours)).strftime("%Y-%m-%dT%H:%M:%S%Z")


def validate_time_string(time_string: str) -> bool:
    pattern = re.compile(r"\d{1,2}:\d{1,2}")
    if re.fullmatch(pattern, time_string):
        return True
    else:
        return False


def get_arguments():
    parser = argparse.ArgumentParser(description=
                                     """Tool to generate a Lacework customer security assessment report.
                                     
                                     You must provide an author and customer string, all other flags are optional.
                                     
                                     If you do not specify an API Key file (downloaded from the Lacework UI) then
                                     either the default account/creds in your .lacework.toml file will be used OR you can 
                                     specify account/creds in the environmental variables as defined on the github page.
                                     The default query times for vulnerability data and alert data are:
                                     
                                     vulns: start-> 25 hours ago   end -> current time
                                     alerts: start -> 7 days ago   end -> current time
                                     
                                     Examples:
                                     
                                     Short and Sweet: 
                                     lw_report_gen --author 'John D' --customer 'Amce Co.'
                                     
                                     Using Custom Query Times (setting the vulnerabilities query to start 7 days and 2 hours ago): 
                                     lw_report_gen --author 'John D' --customer 'Acme Co.' --vulns-start-time 7:2 
                                     
                                     see the github page for more info:
                                     https://github.com/lacework/extensible-reporting
                                     """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--report-path", type=str, help="Filename to save report", default="report.html")
    parser.add_argument("--author", help="Author of report", type=str, required=True)
    parser.add_argument("--customer", help="Customer Name (Company)", type=str, required=True)
    parser.add_argument("--cache-data", help="Create/use locally cached copies of Lacework data", action='store_true')
    parser.add_argument("--vulns-start-time", type=str, help="The number of days and hours in the past relative to NOW to start the vulnerability report. In the format <D:H>", default="0:25")
    parser.add_argument("--vulns-end-time", type=str,
                        help="The number of days and hours in the past relative to NOW to end the vulnerability report. In the format <D:H> (use 0:0 for now)",
                        default="0:0")
    parser.add_argument("--alerts-start-time", type=str,
                        help="The number of days and hours in the past relative to NOW to start the alert report. In the format <D:H>",
                        default="7:0")
    parser.add_argument("--alerts-end-time", type=str,
                        help="The number of days and hours in the past relative to NOW to end the alert report. In the format <D:H> (use 0:0 for now)",
                        default="0:0")
    parser.add_argument("--api-key-file", type=str, help="Read your credentials from an API key file downloaded from the Lacework UI (JSON formatted).")

    return parser.parse_args()


def get_validated_arguments():
    args = get_arguments()

    if not validate_time_string(args.vulns_start_time):
        logger.error("The vulnerability start time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    elif not validate_time_string(args.vulns_end_time):
        logger.error("The vulnerability end time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    elif not validate_time_string(args.alerts_start_time):
        logger.error("The alerts start time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    elif not validate_time_string(args.alerts_end_time):
        logger.error("The alerts end time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()

    if args.api_key_file:

        if not os.path.isfile(args.api_key_file) or not os.access(args.api_key_file, os.R_OK):
            logger.error("The API key file you specified either does not exist or is not readable. Please check the file and it's permissions.")
            sys.exit()

    return args
