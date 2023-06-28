from modules.reports.reportgen_csa import ReportGenCSA
from marketorestpython.client import MarketoClient
import os
import datetime
import boto3
import pdfkit
import json
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return json.loads(secret)


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

    print(f"lacework instance:{event['lacework_instance']}")
    if 'lacework_subaccount' in event:
        print(f"lacework subaccount:{event['lacework_subaccount']}")
    print(f"last 4 of lacework key:{str(event['key'])[-4:]}")
    print(f"last 4 of lacework secret:{str(event['secret'])[-4:]}")
    print(f"customer:{event['customer']}")
    print(f"author:{event['author']}")
    print(f"email:{event['email']}")
    if 'marketo_email' in event:
        print(f"marketo email:{event['marketo_email']}")
    # set credentials for Lacework
    basedir = os.path.dirname(os.path.abspath(__file__))
    os.environ['LW_ACCOUNT'] = event['lacework_instance']
    if 'lacework_subaccount' in event:
        os.environ['LW_SUBACCOUNT'] = event['lacework_subaccount']
    os.environ['LW_API_KEY'] = event['key']
    os.environ['LW_API_SECRET'] = event['secret']

    # S3 Bucket to write report to
    s3_bucket = os.getenv('S3_BUCKET')
    # aws region we're in
    aws_region = os.getenv('AWS_REGION')

    # Get credentials for marketo
    secret = get_secret("marketo", aws_region)
    marketo_munchkin_id = secret['munchkin_id']
    marketo_client_id = secret['client_id']
    marketo_client_secret = secret['client_secret']



    # create report html
    report_gen = ReportGenCSA(basedir)
    report = report_gen.generate(event['customer'], 'Lacework')
    # generate pdf from html
    pdfkit_config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    print(f"Able to write to /tmp?: {os.access('/tmp', os.W_OK)}")
    pdf_file_name = "/tmp/report.pdf"

    try:
        pdfkit.from_string(report, pdf_file_name, configuration=pdfkit_config, options={"page-size": "A4"})
    except Exception as e:
        return {"statusCode": 502,
                "message": "Failed to create pdf",
                "details": str(e)}
    s3_key_name = f'reports/{event["customer"]}_CSA_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
    try:
        aws_s3_client = boto3.client('s3', region_name=aws_region)
        response = aws_s3_client.upload_file(
            pdf_file_name,
            s3_bucket,
            s3_key_name)
    except Exception as e:
        return {"statusCode": 502,
                "message": "Failed to write pdf to S3",
                "details": str(e)}

    presigned_url_args = {'Bucket': s3_bucket, 'Key': s3_key_name}
    presigned_url = aws_s3_client.generate_presigned_url('get_object', presigned_url_args, 604800)
    marketo_presigned_url = presigned_url.removeprefix('https://')

    if 'marketo_email' in event:
        # find marketo lead and update
        mc = MarketoClient(marketo_munchkin_id, marketo_client_id, marketo_client_secret, None, None,
                           requests_timeout=(3.0, 10.0))
        try:
            leads = mc.execute(method='get_multiple_leads_by_filter_type',
                           filterType='email',
                           filterValues=[event['marketo_email']],
                           fields=['firstName', 'middleName', 'lastName', 'Marketplace_CSA_Alternate_Email_Address__c',
                                   'Marketplace_CSA_Report_Link__c', 'CSA_Program_Member'],
                           batchSize=None)
        except Exception as e:
            return {"statusCode": 502,
                    "message": "Failed to query Marketo. Here is the download link..",
                    "details": str(e),
                    "download_url": presigned_url}

        csa_leads = [lead for lead in leads if lead['CSA_Program_Member']]
        if csa_leads:
            csa_lead = csa_leads[0]
            csa_lead['Marketplace_CSA_Alternate_Email_Address__c'] = event['email']
            csa_lead['Marketplace_CSA_Report_Link__c'] = marketo_presigned_url
            #csa_lead['MktoCompanyNotes'] = marketo_presigned_url
            updated_leads = [csa_lead]
            print("Marketo lead to update:")
            print(json.dumps(updated_leads, indent=4))

            try:
                response = mc.execute(method='create_update_leads', leads=updated_leads, action='updateOnly',
                                      lookupField='id',
                                      asyncProcessing='false', partitionName='Default')
            except Exception as e:
                return {"statusCode": 502,
                        "message": "Found Marketo lead but failed to update it",
                        "details": str(e)}
        else:
            return {"statusCode": 502,
                    "message": "No CSA Marketo lead found. Could not complete workflow. Here's the download URL",
                    "download_url": presigned_url}
        if response[0]['status'] == 'updated':
            return {"statusCode": 200,
                    "message": "Report generated and Marketo lead updated.",
                    "details": response}
        else:
            return {"statusCode": 502,
                    "message": "Report generated but failed to update Marketo lead.",
                    "details": response,
                    "download_url": presigned_url}
    else:
        return {"statusCode": 200,
                "message": "No marketo email provided, here's the report download link",
                "download_url": presigned_url
                }



