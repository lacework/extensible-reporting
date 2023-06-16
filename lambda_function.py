from modules.reports.reportgen_csa import ReportGenCSA
import os
import datetime
import boto3


def lambda_handler(event, context):
    '''
    Connect to a Lacework Instance and generate a CSA Report which is then saved to an S3 bucket and a download link
    is emailed to the email address provided

    :param event: A dict with the following format:
        {'lacework_account': Str,                          # the fqdn of the lacework instance
        'lacework_subaccount': Str | None,                  # the Lacework subaccount if it exists, otherwise pass Null/None
        'key': Str,                                         # the Lacework API key
        'secret': Str,                                      # the Lacework API secret
        'customer': Str,                                    # the name of the Customer
        'email': Str,                                       # the email to send the download link to

    :param context:
    :return:
    '''

    basedir = os.path.dirname(os.path.abspath(__file__))
    os.environ['LW_ACCOUNT'] = event['lacework_account']
    os.environ['LW_SUBACCOUNT'] = event['lacework_subaccount']
    os.environ['LW_API_KEY'] = event['key']
    os.environ['LW_API_SECRET'] = event['secret']

    # S3 Bucket to write report to
    s3_bucket = "csareports"
    report_gen = ReportGenCSA(basedir)
    report = report_gen.generate(event['customer'], 'Lacework')

    s3_key_name = f'{event["customer"]}_CSA_{datetime.datetime.now().strftime("%Y%m%d")}.html'
    aws_s3_client = boto3.client('s3')
    response = aws_s3_client.put_object(
        Bucket=s3_bucket,
        Body=report,
        Key=s3_key_name
    )



