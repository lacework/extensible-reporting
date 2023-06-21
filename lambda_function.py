from modules.reports.reportgen_csa import ReportGenCSA
from marketorestpython.client import MarketoClient
import os
import datetime
import boto3
import pdfkit

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
        'marketplace_email': Str                            # the email tied to original aws marketplace request (and Marketo Lead)
        'email': Str,                                       # the email to send the download link to

    :param context:
    :return:
    '''

    # set credentials for Lacework
    basedir = os.path.dirname(os.path.abspath(__file__))
    os.environ['LW_ACCOUNT'] = event['lacework_instance']
    os.environ['LW_SUBACCOUNT'] = event['lacework_subaccount']
    os.environ['LW_API_KEY'] = event['key']
    os.environ['LW_API_SECRET'] = event['secret']

    # Get credentials for marketo
    marketo_munchkin_id = os.getenv('MUNCHKIN_ID')
    marketo_client_id = os.getenv('CLIENT_ID')
    marketo_client_secret = os.getenv('CLIENT_SECRET')

    # S3 Bucket to write report to
    s3_bucket = "csareports"
    # create report html
    report_gen = ReportGenCSA(basedir)
    report = report_gen.generate(event['customer'], 'Lacework')
    # generate pdf from html
    pdfkit_config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    pdf_file_name = "report.pdf"
    pdfkit.from_string(report, pdf_file_name, configuration=pdfkit_config)
    s3_key_name = f'reports/{event["customer"]}_CSA_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
    aws_s3_client = boto3.client('s3', region_name='us-east-2')
    response = aws_s3_client.upload_file(
        pdf_file_name,
        s3_bucket,
        s3_key_name)
    # response = aws_s3_client.put_object(
    #     Bucket=s3_bucket,
    #     Body=report,
    #     Key=s3_key_name)
    presigned_url_args = {'Bucket': s3_bucket, 'Key': s3_key_name}
    presigned_url = aws_s3_client.generate_presigned_url('get_object', presigned_url_args, 604800)

    # find marketo lead and update
    mc = MarketoClient(marketo_munchkin_id, marketo_client_id, marketo_client_secret, None, None,
                       requests_timeout=(3.0, 10.0))
    leads = mc.execute(method='get_multiple_leads_by_filter_type',
                       filterType='email',
                       filterValues=[event['marketplace_email']],
                       fields=['firstName', 'middleName', 'lastName', 'Marketplace_CSA_Alternate_Email_Address__c',
                               'Marketplace_CSA_Report_Link__c'],
                       batchSize=None)
    lead = leads[0]
    lead['Marketplace_CSA_Alternate_Email_Address__c'] = event['email']
    lead['Marketplace_CSA_Report_Link__c'] = presigned_url
    updated_leads = []
    updated_leads.append(lead)
    response = mc.execute(method='create_update_leads', leads=updated_leads, action='updateOnly', lookupField='id',
                          asyncProcessing='false', partitionName='Default')
    return response



