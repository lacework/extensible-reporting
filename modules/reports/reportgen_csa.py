from modules.reportgen import ReportGen
from modules.utils import LaceworkTime


class ReportGenCSA(ReportGen):

    report_short_name = 'CSA'
    report_name = 'Cloud Security Assessment (CIS)'
    report_description = "This is the Lacework provided Cloud Security Assessment with CIS compliance reporting."

    def __init__(self, basedir, use_cache=False, api_key_file=None):
        super().__init__(basedir, use_cache=use_cache, api_key_file=api_key_file)

    def generate(self,
                 customer: str,
                 author: str,
                 vulns_start_time: LaceworkTime,
                 vulns_end_time: LaceworkTime,
                 alerts_start_time: LaceworkTime,
                 alerts_end_time: LaceworkTime):
        polygraph_graphic_bytes = self.load_binary_file('assets/polygraph-info.png')
        polygraph_graphic_html = self.bytes_to_image_tag(polygraph_graphic_bytes, 'png')
        template = self.get_jinja2_template('csa_report.jinja2')
        html = template.render(
            customer=str(customer),
            date=self.get_current_date(),
            author=str(author),
            polygraph_graphic_html=polygraph_graphic_html,
            aws_compliance_data=self.gather_compliance_data(cloud_provider='AWS'),
            azure_compliance_data=self.gather_compliance_data(cloud_provider='AZURE'),
            gcp_compliance_data=self.gather_compliance_data(cloud_provider='GCP'),
            host_vulns_data=self.gather_host_vulnerability_data(vulns_start_time.generate_time_string(), vulns_end_time.generate_time_string()),
            container_vulns_data=self.gather_container_vulnerability_data(vulns_start_time.generate_time_string(), vulns_end_time.generate_time_string()),
            alerts_data=self.gather_alert_data(alerts_start_time.generate_time_string(), alerts_end_time.generate_time_string())
        )
        return html