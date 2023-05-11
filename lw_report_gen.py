import sys
import os
import logzero
import datetime
import traceback
from logzero import logger
from modules.process_args import get_validated_arguments, pre_process_args
from modules.gui_main import ExtensibleReportingGUI
from modules.utils import get_available_reports
from modules.utils import alert_new_release
from modules.reportgen import ReportGen # do not remove, needed by pyinstaller


def main():

    # Get the base directory where this script is running from
    # Required for Pyinstaller as it temporarily extracts all files to a temp folder before running
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(os.path.abspath(__file__))

    # Set up default logging level
    logzero.loglevel(logzero.WARNING)
    # Setup up log file, always write verbose logs
    logzero.logfile('lw_report_gen.log', loglevel=logzero.DEBUG)

    # check github for updates
    alert_new_release()

    # Dynamically import report classes from "modules/reports" subdirectory
    available_reports: list = get_available_reports(basedir)
    if len(available_reports) == 0:
        logger.debug('No available reports to run. You should not get this error since there is a default report.')
        logger.debug('If you are running from source, did you delete the contents of modules/reports? ')
        logger.debug('If you are running the binary, please report this error on the github page:')
        logger.debug('https://github.com/lacework/extensible-reporting')
        sys.exit()
    # Get command line args and process them
    args = get_validated_arguments()
    pre_processed_args = pre_process_args(args, available_reports)

    if args.gui:
        # Bring up the GUI interface
        report_gui = ExtensibleReportingGUI(args, pre_processed_args, available_reports, basedir)
        report_gui.exec()
    else:
        # Execute the selected report from command line (no GUI)
        try:
            report_generator = pre_processed_args['report_to_run'](basedir, use_cache=args.cache_data, api_key_file=pre_processed_args['api_key_file'])
            if args.logo:
                custom_logo = args.logo
            else:
                custom_logo = None
            report = report_generator.generate(args.customer,
                                               args.author,
                                               vulns_start_time=pre_processed_args['vulns_start_time'],
                                               vulns_end_time=pre_processed_args['vulns_end_time'],
                                               alerts_start_time=pre_processed_args['alerts_start_time'],
                                               alerts_end_time=pre_processed_args['alerts_end_time'],
                                               custom_logo=custom_logo
                                               )
        except Exception as e:
            logger.error(f"Report Generation failed for report {args.report}, did you specify one that exists? Check what's available with the '--list-reports' flag.")
            logger.error("Exiting....")
            logger.error(str(e))
            logger.error(traceback.format_exc())
            sys.exit()

        # Generate a filename if one was not specified
        if not args.report_path:
            report_file_name = f'{args.customer}_{args.report}_{datetime.datetime.now().strftime("%Y%m%d")}.html'
        else:
            report_file_name = args.report_path
        # Write out the report file
        logger.info(f'Writing report to {report_file_name}')
        try:
            with open(str(report_file_name), 'w') as file:
                file.write(report)
        except Exception as e:
            logger.error(f'Failed writing report file {report_file_name}: {str(e)}')
            sys.exit()


if __name__ == "__main__":
    main()
