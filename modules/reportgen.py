import os
import sys

import jinja2
import base64
from datetime import datetime
from logzero import logger
from modules.lacework_interface import LaceworkInterface
from modules.compliance import Compliance
from modules.alerts import Alerts
from modules.host_vulnerabilities import HostVulnerabilities
from modules.container_vulnerabilities import ContainerVulnerabilities
from modules.utils import LaceworkTime


class ReportGen:

    report_short_name = 'Base'
    report_name = "Base Report Class"
    report_description = "This is the base report class, it should be inherited from, not imported directly."
    def __init__(self, basedir, use_cache=False, api_key_file=None):
        self.basedir = basedir
        self.use_cache = False
        self.lacework_interface = LaceworkInterface(use_cache=use_cache, api_key_file=api_key_file)

    def bytes_to_image_tag(self, img_bytes: bytes, file_format: str) -> str:
        b64content = base64.b64encode(img_bytes).decode('utf-8')
        return f"<img src='data:image/{file_format};base64,{b64content}'/>"

    def load_binary_file(self, path: str) -> bytes:
        full_path = os.path.join(self.basedir, path)
        with open(full_path, "rb") as in_file:
            file_bytes = in_file.read()
        return file_bytes

    def get_jinja2_template(self, file_name: str) -> jinja2.Template:
        template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(self.basedir, "templates/"))
        template_env = jinja2.Environment(loader=template_loader, autoescape=True, trim_blocks=True, lstrip_blocks=True)
        template_file = file_name
        try:
            return template_env.get_template(template_file)
        except Exception as e:
            logger.error(f'Could not load html template {str(file_name)}, EXITING: {str(e)}')
            sys.exit()

    def get_current_date(self) -> str:
        return datetime.now().strftime("%A %B %d, %Y")

    def gather_host_vulnerability_data(self, begin_time: str, end_time: str, host_limit: int = 25):
        print('Gathering vulnerability data for hosts.')
        try:
            host_vulnerabilities: HostVulnerabilities = self.lacework_interface.get_host_vulns(begin_time, end_time)
        except Exception as e:
            logger.error(
                f'Failed to retrieve host vulnerability data from Lacework, omitting it from the report.')
            logger.error(f"Exception: {str(e)}")
            return False
        if not host_vulnerabilities.data:
            logger.error("No host vulnerability data was returned by Lacework, omitting it from the report.")
            return False
        total_evaluated = host_vulnerabilities.total_evaluated()
        summary_by_host = host_vulnerabilities.summary_by_host(limit=host_limit)
        summary_by_host.style.set_table_attributes('class="host_vulns_summary_by_host"')
        summary = host_vulnerabilities.summary()
        summary.style.set_table_attributes('class="host_vulns_summary"')
        critical_vulnerability_count = summary.loc[summary['Severity'] == 'Critical', 'Hosts Affected'].values[0]
        summary_bar_graphic = host_vulnerabilities.host_vulns_by_severity_bar(width=1200)
        summary_bar_graphic_encoded = self.bytes_to_image_tag(summary_bar_graphic, "svg+xml")
        return {
            'hosts_scanned_count': total_evaluated,
            'host_vulns_summary': summary,
            'host_vulns_summary_bar_graphic': summary_bar_graphic_encoded,
            'host_vulns_summary_by_host': summary_by_host,
            'critical_vuln_count': critical_vulnerability_count,
            'host_vulns_summary_by_host_limit': host_limit
        }

    def gather_container_vulnerability_data(self, begin_time: str, end_time: str, container_limit: int = 25):
        print('Gathering vulnerability data for containers.')
        try:
            container_vulnerabilities: ContainerVulnerabilities = self.lacework_interface.get_container_vulns(begin_time, end_time)
        except Exception as e:
            logger.error(
                f'Failed to retrieve container vulnerability data from Lacework, omitting it from the report.')
            logger.error(f"Exception: {str(e)}")
            return False
        if not container_vulnerabilities.data:
            logger.error("No container vulnerability data was returned by Lacework, omitting it from the report.")
            return False
        total_evaluated = container_vulnerabilities.total_evaluated()
        summary_by_image = container_vulnerabilities.summary_by_image(limit=container_limit)
        summary_by_image.style.set_table_attributes('class="container_vulns_summary_by_image"')
        summary = container_vulnerabilities.summary()
        summary.style.set_table_attributes('class="container_vulns_summary"')
        critical_vulnerability_count = summary.loc[summary['Severity'] == 'Critical', 'Images Affected'].values[0]
        summary_by_package_bar = container_vulnerabilities.top_packages_bar(width=1200)
        summary_by_package_bar_encoded = self.bytes_to_image_tag(summary_by_package_bar, 'svg+xml')

        return {
            'containers_scanned_count': total_evaluated,
            'container_vulns_summary': summary,
            'container_vulns_summary_by_package_bar_graphic': summary_by_package_bar_encoded,
            'container_vulns_summary_by_image': summary_by_image,
            'critical_vuln_count': critical_vulnerability_count,
            'container_vulns_summary_by_image_limit': container_limit
        }

    def gather_compliance_data(self, cloud_provider='AWS', report_type='CIS' ):
        print(f'Getting {report_type} compliance reports for {cloud_provider}')
        try:
            compliance_reports: Compliance = self.lacework_interface.get_compliance_reports(cloud_provider=cloud_provider, report_type=report_type)
        except Exception as e:
            logger.error(f'Failed to retrieve {report_type} report(s) for {cloud_provider}, omitting them from the report.')
            logger.error(f"Exception: {str(e)}")
            return False
        if not compliance_reports.reports:
            logger.error(f'Reports of type {report_type} from {cloud_provider} came back empty. Omitting them from the report.')
            return False
        # set table classes
        details = compliance_reports.get_compliance_details()
        details.style.set_table_attributes('class="compliance_detail"')
        summary = compliance_reports.get_compliance_summary()
        summary.style.set_table_attributes('class="compliance_summary"')
        # get graphics
        findings_by_account_bar_graph = compliance_reports.get_summary_by_account_bar_graph(width=1200)
        findings_by_account_bar_graph_encoded = self.bytes_to_image_tag(findings_by_account_bar_graph, 'svg+xml')

        findings_summary_by_service_bar_graph = compliance_reports.get_summary_by_service_bar_graph(width=1200)
        findings_summary_by_service_bar_graph_encoded = self.bytes_to_image_tag(findings_summary_by_service_bar_graph, 'svg+xml')

        summary_by_account = compliance_reports.get_summary_by_account()
        if 'Critical' in summary_by_account.columns:
            critical_finding_count = summary_by_account['Critical'].sum()
        else:
            critical_finding_count = 0

        return {
            'cloud_accounts_count': compliance_reports.get_total_accounts_evaluated(),
            'compliance_summary': summary,
            'compliance_findings_by_service_bar_graphic': findings_summary_by_service_bar_graph,
            'compliance_findings_by_account_bar_graphic': findings_by_account_bar_graph,
            'compliance_detail': details,
            'critical_finding_count': critical_finding_count
        }

    def gather_alert_data(self, begin_time: str, end_time: str):
        print('Getting alert data...')
        alerts: Alerts = self.lacework_interface.get_alerts(begin_time, end_time)
        print(f'Found {alerts.count_alerts()} total alerts.')
        processed_alerts = alerts.processed_alerts(limit=25)
        high_critical_finding_count = len(processed_alerts[processed_alerts['Severity'].isin(['Critical', 'High'])])
        print(f'Found {high_critical_finding_count} high and critical alerts.')
        return {
            'alerts_raw': processed_alerts,
            'high_critical_finding_count': high_critical_finding_count
        }

    def generate(self,
                 customer: str,
                 author: str,
                 vulns_start_time: LaceworkTime,
                 vulns_end_time: LaceworkTime,
                 alerts_start_time: LaceworkTime,
                 alerts_end_time: LaceworkTime):
        pass



