from modules.reportgen import ReportGen
from modules.utils import LaceworkTime
import os

class ReportGenCSADetailed(ReportGen):

    report_short_name = 'CSA Detailed'
    report_name = 'Detailed Cloud Security Assessment (CIS)'
    report_description = "This is the detailed version of the Lacework Cloud Security Assessment with CIS compliance reporting."
    default_recommendations = """<h2>Recommendations</h2>
            <p>
              Based on the findings of this assessment, Lacework recommends the following action plan and next steps:
            </p>
            <ol>
              <li>Engage with your Lacework account team and partner to review services offerings to prioritize and remediate the findings</li>
              <li>Complete a recurring Cloud Security Assessment once a wider Lacework deployment has been completed to baseline and trend improvements to your cloud security posture.</li>
            </ol>"""

    def __init__(self, basedir, use_cache=False, api_key_file=None, graph_scale=1):
        super().__init__(basedir, use_cache=use_cache, api_key_file=api_key_file, graph_scale=graph_scale)
        self.recommendations = self.default_recommendations
        self.template = self.get_jinja2_template('csa_detailed_report.jinja2')
        self.polygraph_graphic_html = self.file_to_image_tag('assets/polygraph-info.png', 'png')

    def gather_data(self,
                    vulns_start_time: LaceworkTime,
                    vulns_end_time: LaceworkTime,
                    alerts_start_time: LaceworkTime,
                    alerts_end_time: LaceworkTime):


        self.aws_compliance_data=self.gather_compliance_data(cloud_provider='AWS')
        self.azure_compliance_data=self.gather_compliance_data(cloud_provider='AZURE')
        self.gcp_compliance_data=self.gather_compliance_data(cloud_provider='GCP')
        self.host_vulns_data=self.gather_host_vulnerability_data(vulns_start_time.generate_time_string(), vulns_end_time.generate_time_string())
        self.container_vulns_data=self.gather_container_vulnerability_data(vulns_start_time.generate_time_string(), vulns_end_time.generate_time_string())
        self.alerts_data=self.gather_alert_data(alerts_start_time.generate_time_string(), alerts_end_time.generate_time_string())
        self.secrets_data=self.gather_secrets(alerts_start_time.generate_time_string(), alerts_end_time.generate_time_string())

    def render(self, customer, author, pagesize="a3", custom_logo=None):
        if custom_logo and os.path.isfile(custom_logo):
            self.custom_logo_html = self.file_to_image_tag(custom_logo, 'png', align='right')
        else:
            self.custom_logo_html = None
        return self.template.render(
            customer=str(customer),
            date=self.get_current_date(),
            author=str(author),
            custom_logo_html=self.custom_logo_html,
            polygraph_graphic_html=self.polygraph_graphic_html,
            aws_compliance_data=self.aws_compliance_data,
            azure_compliance_data=self.azure_compliance_data,
            gcp_compliance_data=self.gcp_compliance_data,
            host_vulns_data=self.host_vulns_data,
            container_vulns_data=self.container_vulns_data,
            alerts_data=self.alerts_data,
            secrets_data=self.secrets_data,
            recommendations=self.recommendations,
            pagesize=pagesize
        )

    def generate(self,
                 customer: str,
                 author: str,
                 vulns_start_time: LaceworkTime = LaceworkTime('0:25'),
                 vulns_end_time: LaceworkTime = LaceworkTime('0:0'),
                 alerts_start_time: LaceworkTime = LaceworkTime('7:0'),
                 alerts_end_time: LaceworkTime = LaceworkTime('0:0'),
                 custom_logo=None,
                 pagesize="a3"):
        self.gather_data(vulns_start_time,
                         vulns_end_time,
                         alerts_start_time,
                         alerts_end_time)
        return self.render(customer, author, custom_logo=custom_logo, pagesize=pagesize)


