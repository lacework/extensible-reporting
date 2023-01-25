import os
import jinja2
import base64
from modules.lacework_interface import LaceworkInterface
from datetime import datetime, timezone, timedelta
from logzero import logger


class ReportGen:

    def __init__(self, basedir, use_cache=False):
        self.basedir = basedir
        self.use_cache = False
        self.lacework_interface = LaceworkInterface(use_cache=use_cache)

    def bytes_to_image_tag(self, img_bytes: bytes, file_format: str) -> str:
        b64content = base64.b64encode(img_bytes).decode('utf-8')
        return f"<img src='data:image/{file_format};base64,{b64content}'/>"

    def generate_time_string(self, days=0, hours=0) -> str:
        return (datetime.now(timezone.utc) - timedelta(days=days, hours=hours)).strftime("%Y-%m-%dT%H:%M:%S%Z")

    def load_binary_file(self, path: str) -> bytes:
        full_path = os.path.join(self.basedir, path)
        with open(full_path, "rb") as in_file:
            file_bytes = in_file.read()
        return file_bytes


class ReportGenCSA(ReportGen):

    def __init__(self, basedir, use_cache=False):
        super().__init__(basedir, use_cache=use_cache)
        self.time_now = self.generate_time_string()
        self.time_minus_25h = self.generate_time_string(hours=25)
        self.time_minus_7d = self.generate_time_string(days=7)

    def gather_host_vulnerability_data(self, begin_time: str, end_time: str, host_limit: int = 25):
        host_vulnerabilities = self.lacework_interface.get_host_vulns(begin_time, end_time)
        if not host_vulnerabilities:
            logger.error("No host vulnerabilities were returned by Lacework.")
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
        container_vulnerabilities = self.lacework_interface.get_container_vulns(begin_time, end_time)
        if not container_vulnerabilities:
            logger.error("No container vulnerabilities were returned by Lacework.")
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

    def gather_compliance_data(self):
        return False

    def gather_event_data(self, begin_time: str, end_time: str):
        events = self.lacework_interface.get_events(begin_time, end_time)
        processed_events = events.processed_events(limit=25)
        high_critical_finding_count = len(processed_events[processed_events['Severity'].isin(['Critical', 'High'])])
        return {
            'events_raw': processed_events,
            'high_critical_finding_count': high_critical_finding_count
        }

    def generate(self, customer: str, author: str):
        polygraph_graphic_bytes = self.load_binary_file('assets/polygraph-info.png')
        polygraph_graphic_html = self.bytes_to_image_tag(polygraph_graphic_bytes, 'png')
        template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(self.basedir, "templates/"))
        template_env = jinja2.Environment(loader=template_loader, autoescape=True, trim_blocks=True, lstrip_blocks=True)
        template_file = "csa_report.html"
        template = template_env.get_template(template_file)
        html = template.render(
            customer=str(customer),
            date=datetime.now().strftime("%A %B %d, %Y"),
            author=str(author),
            polygraph_graphic_html=polygraph_graphic_html,
            compliance_data=self.gather_compliance_data(),
            host_vulns_data=self.gather_host_vulnerability_data(self.time_minus_25h, self.time_now),
            container_vulns_data=self.gather_container_vulnerability_data(self.time_minus_25h, self.time_now),
            event_data=self.gather_event_data(self.time_minus_7d, self.time_now)
        )
        return html


