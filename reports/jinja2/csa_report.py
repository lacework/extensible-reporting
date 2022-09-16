import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_dummy_data):
    import os
    from datetime import datetime

    import jinja2
    
    lw_provider = _shared.p_lw_dummy if use_dummy_data else _shared.p_lw

    host_vulns_data = gather_host_vulns_data(_shared, lw_provider)
    container_vulns_data = gather_container_vulns_data(_shared, lw_provider)
    compliance_data = gather_compliance_data(_shared, lw_provider)

    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
    TEMPLATE_FILE = "csa_report.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    html = template.render(
        customer                                   = _shared.cli_data['customer'],
        date                                       = datetime.now().strftime("%A %B %d, %Y"),
        author                                     = _shared.cli_data['author'],
        cloud_accounts_count                       = str(compliance_data['cloud_accounts_count']),
        hosts_scanned_count                        = str(host_vulns_data['hosts_scanned_count']),
        containers_scanned_count                   = str(container_vulns_data['containers_scanned_count']),
        active_images_count                        = str(container_vulns_data['active_images_count']),
        host_vulns_summary                         = host_vulns_data['host_vulns_summary'],
        host_vulns_summary_bar_graphic             = host_vulns_data['host_vulns_summary_bar_graphic'],
        container_vulns_summary                    = container_vulns_data['container_vulns_summary'],
        container_vulns_summary_bar_graphic        = container_vulns_data['container_vulns_summary_bar_graphic'],
        host_vulns_summary_by_host                 = host_vulns_data['host_vulns_summary_by_host'],
        container_vulns_summary_by_image           = container_vulns_data['container_vulns_summary_by_image'],
        compliance_summary                         = compliance_data['compliance_summary'],
        compliance_findings_by_service_bar_graphic = compliance_data['compliance_findings_by_service_bar_graphic'],
        compliance_findings_by_account_bar_graphic = compliance_data['compliance_findings_by_account_bar_graphic'],
        compliance_detail                          = compliance_data['compliance_detail']
    )

    logger.info('Saving report to: ' + report_save_path)

    with open(report_save_path, 'w') as file:
        file.write(html)

def gather_host_vulns_data(_shared, lw_provider):
    host_vulns = lw_provider.host_vulns(_shared._25_hours_ago, _shared._now)

    # style
    host_vulns_summary_by_host = _shared.t_lw.host_vulns_summary_by_host(host_vulns)
    host_vulns_summary_by_host = host_vulns_summary_by_host.style.set_table_styles({"Severity Count" : [
        {
            "selector" :"td.col1",
            "props": "white-space: pre; text-align:left"
        },
        {
            "selector" :"th.row_heading",
            "props": "white-space: nowrap; width: 15px"
        }

    ]})

    host_vulns_summary = _shared.t_lw.host_vulns_summary(host_vulns)
    host_vulns_summary_bar_graphic = _shared.g_lw_plotly.host_vulns_by_severity_bar(host_vulns_summary, width=750)
    host_vulns_summary_bar_graphic = _shared.g_lw_plotly.bytes_to_image_tag(host_vulns_summary_bar_graphic)

    return {
        'hosts_scanned_count': _shared.t_lw.host_vulns_total_evaluated(host_vulns),
        'host_vulns_summary': host_vulns_summary,
        'host_vulns_summary_bar_graphic': host_vulns_summary_bar_graphic,
        'host_vulns_summary_by_host': host_vulns_summary_by_host
    }

def gather_container_vulns_data(_shared, lw_provider):
    container_vulns = lw_provider.container_vulns(_shared._25_hours_ago,_shared._now)
    
    container_vulns_summary_by_image = _shared.t_lw.container_vulns_summary_by_image(container_vulns)
    container_vulns_summary_by_image = container_vulns_summary_by_image.style.set_table_styles([
        {
            "selector" :"td.col2",
            "props": "white-space: pre; text-align:left"
        },
        {
            "selector" :"th.row_heading",
            "props": "white-space: nowrap; width: 15px"
        },
        {
            "selector" :"td.col0",
            "props": "white-space: nowrap"
        },
        {
            "selector" :"td.col1",
            "props": "white-space: nowrap"
        },
        {
            "selector" :"td.col3",
            "props": "white-space: nowrap"
        }
    
    ])
    return {
        'containers_scanned_count': '[Containers Scanned Count Placeholder]', # _shared.t_lw.container_vulns_total_evaluated(host_vulns)
        'container_vulns_summary': _shared.t_lw.container_vulns_summary(container_vulns),
        'container_vulns_summary_bar_graphic': '[Container Vulns Summary Bar Graphic Placeholder]',
        'container_vulns_summary_by_image': container_vulns_summary_by_image,
        'active_images_count': '[Active Images Count Placeholder]'
    }

def gather_compliance_data(_shared, lw_provider):
    # get aws accounts
    integrations = lw_provider.integrations()
    aws_config_accounts = _shared.t_lw.integrations_config_accounts(integrations)

    # get compliance reports
    compliance_reports = lw_provider.compliance_reports(accounts=aws_config_accounts)

    compliance_detail = _shared.t_lw.compliance_reports_raw(compliance_reports)

    compliance_detail = compliance_detail.style.set_table_styles([
        {
            "selector" :"td.col0",
            "props": "white-space: nowrap"
        },
        {
            "selector" :".col3",
            "props": "white-space: nowrap"
        },
        {
            "selector" :".col4",
            "props": "white-space: nowrap"
        },
        {
            "selector" :"th.row_heading",
            "props": "white-space: nowrap; width: 15px"
        }
    
    ])
    return {
        'cloud_accounts_count': '[Cloud Accounts Count Placeholder]',
        'compliance_summary': _shared.t_lw.compliance_reports_summary(compliance_reports),
        'compliance_findings_by_service_bar_graphic': '[Compliance Findings by Service Bar Graphic Placeholder]',
        'compliance_findings_by_account_bar_graphic': '[Compliance Findings by Account Bar Graphic Placeholder]',
        'compliance_detail': compliance_detail
    }