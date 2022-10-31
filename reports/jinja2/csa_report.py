import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_cached_data):
    import os
    from datetime import datetime
    import sys
    import jinja2
        
    # detect if in Pyinstaller package and build appropriate base directory path
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir)))
        
        
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    host_vulns_data = gather_host_vulns_data(_shared, lw_provider)
    container_vulns_data = gather_container_vulns_data(_shared, lw_provider)
    compliance_data = gather_compliance_data(_shared, lw_provider)
    event_data = gather_event_data(_shared, lw_provider)

    polygraph_graphic_bytes = _shared.p_local_asset.local_file(os.path.join(basedir, 'assets/lacework/images/polygraph-info.png'))
    polygraph_graphic_html = _shared.common.bytes_to_image_tag(polygraph_graphic_bytes,'png')

    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.join(basedir, "reports/jinja2/"))
    templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True, trim_blocks=True, lstrip_blocks=True)
    TEMPLATE_FILE = "csa_report.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    html = template.render(
        customer                                   = _shared.cli_data['customer'],
        date                                       = datetime.now().strftime("%A %B %d, %Y"),
        author                                     = _shared.cli_data['author'],
        polygraph_graphic_html                     = polygraph_graphic_html,
        compliance_data                            = compliance_data,
        host_vulns_data                            = host_vulns_data,
        container_vulns_data                       = container_vulns_data,
        event_data                                 = event_data
    )

    logger.info('Saving report to: ' + report_save_path)

    with open(report_save_path, 'w') as file:
        file.write(html)

def gather_host_vulns_data(_shared, lw_provider):
    # get host vulns
    host_vulns = lw_provider.host_vulns(_shared._25_hours_ago, _shared._now)
    if not host_vulns:
        return False

    host_vulns_summary_by_host_limit = 25
    host_vulns_summary_by_host = _shared.t_lw.host_vulns_summary_by_host(host_vulns, limit=host_vulns_summary_by_host_limit)
    host_vulns_summary_by_host = host_vulns_summary_by_host.style.set_table_attributes('class="host_vulns_summary_by_host"')
    host_vulns_summary_data = _shared.t_lw.host_vulns_summary(host_vulns)
    critical_vuln_count = host_vulns_summary_data.loc[host_vulns_summary_data['Severity'] == 'Critical','Hosts Affected'].values[0]
    
    # set table classes
    host_vulns_summary = host_vulns_summary_data.style.set_table_attributes('class="host_vulns_summary"')    

    # get graphics
    host_vulns_summary_bar_graphic = _shared.g_lw_plotly.host_vulns_by_severity_bar(host_vulns_summary_data, width=1200)
    host_vulns_summary_bar_graphic = _shared.common.bytes_to_image_tag(host_vulns_summary_bar_graphic,'svg+xml')

    return {
        'hosts_scanned_count': _shared.t_lw.host_vulns_total_evaluated(host_vulns),
        'host_vulns_summary': host_vulns_summary,
        'host_vulns_summary_bar_graphic': host_vulns_summary_bar_graphic,
        'host_vulns_summary_by_host': host_vulns_summary_by_host,
        'critical_vuln_count': critical_vuln_count,
        'host_vulns_summary_by_host_limit': host_vulns_summary_by_host_limit
    }

def gather_container_vulns_data(_shared, lw_provider):
    # get container vulns
    container_vulns = lw_provider.container_vulns(_shared._25_hours_ago,_shared._now)
    if not container_vulns:
        return False

    container_vulns_summary_by_image_limit = 25
    container_vulns_summary_by_image = _shared.t_lw.container_vulns_summary_by_image(container_vulns, limit=container_vulns_summary_by_image_limit)
    container_vulns_summary_by_image = container_vulns_summary_by_image.style.set_table_attributes('class="container_vulns_summary_by_image"')
    container_vulns_summary = _shared.t_lw.container_vulns_summary(container_vulns)
    critical_vuln_count = container_vulns_summary.loc[container_vulns_summary['Severity'] == 'Critical','Images Affected'].values[0]

    # set table classes
    container_vulns_summary = container_vulns_summary.style.set_table_attributes('class="container_vulns_summary"')

    # get graphics
    container_vulns_summary_by_package = _shared.t_lw.container_vulns_summary_by_package(container_vulns)
    container_vulns_summary_by_package['Package Info'] = container_vulns_summary_by_package['Package Info'].str.replace("\n",'<br>')
    
    container_vulns_summary_by_package_bar_graphic = _shared.g_lw_plotly.container_vulns_top_packages_bar(container_vulns_summary_by_package.head(10), width=1200)
    container_vulns_summary_by_package_bar_graphic = _shared.common.bytes_to_image_tag(container_vulns_summary_by_package_bar_graphic, 'svg+xml')
    
    return {
        'containers_scanned_count': _shared.t_lw.container_vulns_total_evaluated(container_vulns),
        'container_vulns_summary': container_vulns_summary,
        'container_vulns_summary_by_package_bar_graphic': container_vulns_summary_by_package_bar_graphic,
        'container_vulns_summary_by_image': container_vulns_summary_by_image,
        'critical_vuln_count': critical_vuln_count,
        'container_vulns_summary_by_image_limit': container_vulns_summary_by_image_limit
    }

def gather_compliance_data(_shared, lw_provider):
    # get aws accounts
    integrations = lw_provider.integrations()

    aws_config_accounts = _shared.t_lw.integrations_config_accounts(integrations)
    if not aws_config_accounts:
        return False

    # get compliance reports
    compliance_reports = lw_provider.compliance_reports(accounts=aws_config_accounts)
    compliance_reports = _shared.t_lw.compliance_reports_select_most_noncompliant(compliance_reports)
    cloud_accounts_count = len(compliance_reports.keys())

    #flatten
    compliance_reports = sum(map(lambda kv: kv[1], compliance_reports.items()), [])

    if not compliance_reports:
        return False

    # set table classes
    compliance_detail = _shared.t_lw.compliance_reports_raw(compliance_reports)
    compliance_detail = compliance_detail.style.set_table_attributes('class="compliance_detail"')
    compliance_summary = _shared.t_lw.compliance_reports_summary(compliance_reports)
    compliance_summary = compliance_summary.style.set_table_attributes('class="compliance_summary"')

    # get graphics
    compliance_findings_summary_for_graphic = _shared.t_lw.compliance_reports_summary_for_graphic(compliance_reports)

    compliance_findings_by_account_bar_graphic = _shared.g_lw_plotly.compliance_findings_summary_by_account_bar(compliance_findings_summary_for_graphic, width=1200)
    compliance_findings_by_account_bar_graphic = _shared.common.bytes_to_image_tag(compliance_findings_by_account_bar_graphic, 'svg+xml')
    
    compliance_reports_summary_by_service_for_graphic = _shared.t_lw.compliance_reports_summary_by_service_for_graphic(compliance_reports)
    
    compliance_findings_summary_by_service_bar_graphic = _shared.g_lw_plotly.compliance_findings_summary_by_service_bar(compliance_reports_summary_by_service_for_graphic, width=1200)
    compliance_findings_summary_by_service_bar_graphic = _shared.common.bytes_to_image_tag(compliance_findings_summary_by_service_bar_graphic, 'svg+xml')
    
    if 'Critical' in compliance_findings_summary_for_graphic.columns:
        critical_finding_count = compliance_findings_summary_for_graphic['Critical'].sum()
    else:
        critical_finding_count = 0

    return {
        'cloud_accounts_count': cloud_accounts_count,
        'compliance_summary': compliance_summary,
        'compliance_findings_by_service_bar_graphic': compliance_findings_summary_by_service_bar_graphic,
        'compliance_findings_by_account_bar_graphic': compliance_findings_by_account_bar_graphic,
        'compliance_detail': compliance_detail,
        'critical_finding_count': critical_finding_count
    }

def gather_event_data(_shared, lw_provider):
    events = lw_provider.events(_shared._7_days_ago,_shared._now)
    if not events:
        return False

    events_raw = _shared.t_lw.events_raw(events, limit=25)

    
    high_critical_finding_count = len(events_raw[events_raw['Severity'].isin(['Critical','High'])])

    return {
        'events_raw': events_raw,
        'high_critical_finding_count': high_critical_finding_count
    }