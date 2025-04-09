import argparse
import pathlib
import sys
import os
import re
import logzero
from logzero import logger
from modules.utils import LaceworkTime
from pathlib import Path
import json


def validate_time_argument(time_string: str) -> bool:
    pattern = re.compile(r"\d{1,2}:\d{1,2}")
    if re.fullmatch(pattern, time_string):
        return True
    else:
        return False


def get_arguments():
    parser = argparse.ArgumentParser(description=
    """                                     Tool to generate a Lacework report. By default a Cloud Security Assessment report
                                     is generated. 
                                     
                                     To see other report types available (if any are) use the '--list-reports' flag.
                                     To specify a report to run rather than the default use the '--report' flag.
                                     
                                     The '--author' and '--customer' arguments allow you to provide author and customer 
                                     names (strings) that will be inserted into the report. They are not required but are
                                     highly recommended.

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


    parser.add_argument("--report-path", type=str, help="Filename to save report")
    parser.add_argument("--author", help="Author of report", type=str, default="Fortinet")
    parser.add_argument("--customer", help="Customer Name (Company)", type=str, default="customer")
    parser.add_argument("--cache-data", help="Create/use locally cached copies of Lacework data. This is mainly used for dev testing.", action='store_true')
    parser.add_argument("--vulns-start-time", type=str,
                        help="The number of days and hours in the past relative to NOW to start the vulnerability report. In the format <D:H>",
                        default="0:25")
    parser.add_argument("--vulns-end-time", type=str,
                        help="The number of days and hours in the past relative to NOW to end the vulnerability report. In the format <D:H> (use 0:0 for now)",
                        default="0:0")
    parser.add_argument("--alerts-start-time", type=str,
                        help="The number of days and hours in the past relative to NOW to start the alert report. In the format <D:H>",
                        default="7:0")
    parser.add_argument("--alerts-end-time", type=str,
                        help="The number of days and hours in the past relative to NOW to end the alert report. In the format <D:H> (use 0:0 for now)",
                        default="0:0")
    parser.add_argument("--api-key-file", type=str,
                        help="Read your credentials from an API key file downloaded from the Lacework UI (JSON formatted).")
    parser.add_argument("--v", help="Set Verbose Logging", action='store_true')
    parser.add_argument("--vv", help="Set Extremely Verbose Logging", action='store_true')
    parser.add_argument("--report", help="Choose which report to execute. Default is 'CSA_Detailed'", default="CSA_Detailed")
    parser.add_argument("--report-format", help="Specify output format, HTML or PDF. Default is HTML", default="HTML")
    parser.add_argument("--gui", help="Run this tool in GUI mode, which provides additional customization options.", action='store_true')
    parser.add_argument("--logo", type=str, help="Specify a custom logo (PNG file) to add to the report.")
    parser.add_argument("--list-reports", help="List the available reports to generate. Default is 'CSA'", action='store_true')

    return parser.parse_args()


def get_validated_arguments():
    args = get_arguments()

    if not validate_time_argument(args.vulns_start_time):
        logger.error(
            "The vulnerability start time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    elif not validate_time_argument(args.vulns_end_time):
        logger.error(
            "The vulnerability end time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    elif not validate_time_argument(args.alerts_start_time):
        logger.error(
            "The alerts start time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    elif not validate_time_argument(args.alerts_end_time):
        logger.error(
            "The alerts end time string is not formatted correctly. Use <days>:<hours>. For example '7:0' for 7 days, 0 hours in the past.")
        sys.exit()
    if args.logo:
        if "~" in args.logo:
            args.logo = args.logo.replace("~", os.path.expanduser("~"))
        if not os.path.isfile(args.logo) or not os.access(args.logo, os.R_OK):
            logger.error(
                "The logo file either does not exist or cannot be read. Please check the file and it's permissions."
            )
            sys.exit()
        elif str(pathlib.Path(args.logo).suffix).lower() != ".png":
            logger.error(
                "The logo file specified does not appear to be a PNG file. When specifying a logo it must be a PNG file."
            )
            sys.exit()
    if args.api_key_file:
        if "~" in args.api_key_file:
            args.api_key_file = args.api_key_file.replace("~", os.path.expanduser("~"))
        if not os.path.isfile(args.api_key_file) or not os.access(args.api_key_file, os.R_OK):
            logger.error(
                "The API key file you specified either does not exist or is not readable. Please check the file and it's permissions.")
            sys.exit()
    if args.report_format not in ["HTML", "PDF"]:
        logger.error("Please specify a valid report format of either HTML or PDF.")
        sys.exit()
        
    return args



def pre_process_args(args, available_reports):

    # Print out available reports to run if the "--list-reports" flag was used
    if args.list_reports:
        print(f'\nAvailable Reports (use the "ID" with the "--report" flag to specify one):\n')
        for available_report in available_reports:
            print(f"{'(*Default) ' if available_report['report_short_name'] == 'CSA_Detailed' else ''}ID:{available_report['report_short_name']}", end=" ")
            print(f"Name:{available_report['report_name']}", end=" ")
            print(f"Description: {available_report['report_description']}")
        print('')
        sys.exit()

    # Set loglevel for standard out based on verbosity arg
    if args.v:
        logzero.loglevel(logzero.INFO)
    elif args.vv:
        logzero.loglevel(logzero.DEBUG)

    # Convert query time args to a date format the Lacework API understands
    vulns_start_time = LaceworkTime(args.vulns_start_time)
    vulns_end_time = LaceworkTime(args.vulns_end_time)
    alerts_start_time = LaceworkTime(args.alerts_start_time)
    alerts_end_time = LaceworkTime(args.alerts_end_time)

    # Check to see if creds were provided
    api_key_file = None
    lacework_toml_exists = Path(str(Path.home()) + '/.lacework.toml').exists()
    env_var_creds_exist = (bool(os.environ.get('LW_ACCOUNT')) and\
        bool(os.environ.get('LW_API_KEY')) and\
        bool(os.environ.get('LW_API_SECRET'))) or bool(os.environ.get('LW_API_TOKEN'))
    # If there's an API keyfile specified, try to use it, else exit
    if args.api_key_file:
        try:
            with open(args.api_key_file, 'r') as file:
                api_key_file = json.load(file)
        except Exception as e:
            logger.error(f"Failed to read keyfile: {str(e)}")
            sys.exit()
    elif not lacework_toml_exists and not env_var_creds_exist:
        logger.error("You have failed to provide Lacework API credentials")
        logger.error("Please read the github page for instructions.")
        logger.error("https://github.com/lacework/extensible-reporting")
        sys.exit()
    # search the list of available reports for the one specified on the command line. CSA is the default arg
    report_to_run = [report['report_class'] for report in available_reports if report['report_short_name'] == args.report][0]
    processed_args = {'vulns_start_time': vulns_start_time,
                      'vulns_end_time': vulns_end_time,
                      'alerts_start_time': alerts_start_time,
                      'alerts_end_time': alerts_end_time,
                      'api_key_file': api_key_file,
                      'report_to_run': report_to_run}
    return processed_args

