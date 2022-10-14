import json

import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_cached_data):
    import os
    from datetime import datetime

    import jinja2
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    # get aws accounts
    integrations = lw_provider.integrations()

    aws_config_accounts = _shared.t_lw.integrations_config_accounts(integrations)

    # get compliance reports
    compliance_reports = lw_provider.compliance_reports(accounts=aws_config_accounts)
    cloud_accounts_count = _shared.t_lw.compliance_reports_total_accounts_evaluated(compliance_reports)

    # set table classes
    compliance_detail = _shared.t_lw.compliance_reports_raw(compliance_reports)
    compliance_detail = compliance_detail.style.set_table_attributes('class="compliance_detail"')
    compliance_summary = _shared.t_lw.compliance_reports_summary(compliance_reports)
    compliance_summary = compliance_summary.style.set_table_attributes('class="compliance_summary"')

    # get graphics
    compliance_findings_summary_for_graphic = _shared.t_lw.compliance_reports_summary_for_graphic(compliance_reports)

    compliance_findings_by_account_bar_graphic = _shared.g_lw_plotly.compliance_findings_summary_by_account_bar(compliance_findings_summary_for_graphic, width=750)
    compliance_findings_by_account_bar_graphic = _shared.common.bytes_to_image_tag(compliance_findings_by_account_bar_graphic, 'svg+xml')

    compliance_reports_summary_by_service_for_graphic = _shared.t_lw.compliance_reports_summary_by_service_for_graphic(compliance_reports)
    
    compliance_findings_summary_by_service_bar_graphic = _shared.g_lw_plotly.compliance_findings_summary_by_service_bar(compliance_reports_summary_by_service_for_graphic, width=750)
    compliance_findings_summary_by_service_bar_graphic = _shared.common.bytes_to_image_tag(compliance_findings_summary_by_service_bar_graphic, 'svg+xml')
    
    data = {
        'cloud_accounts_count': cloud_accounts_count,
        'compliance_summary': compliance_summary.to_html(),
        'compliance_findings_summary_for_graphic': compliance_findings_summary_for_graphic.to_html(),
        'compliance_findings_by_service_bar_graphic': compliance_findings_summary_by_service_bar_graphic,
        'compliance_findings_by_account_bar_graphic': compliance_findings_by_account_bar_graphic,
        'compliance_detail': compliance_detail.to_html(),
        'compliance_raw_json': '<pre>' + json.dumps(compliance_reports, indent=2) + '</pre>'
    }

    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True, trim_blocks=True, lstrip_blocks=True)
    TEMPLATE_FILE = "template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    html = template.render(
        data = data
    )

    logger.info('Saving report to: ' + report_save_path)

    with open(report_save_path, 'w') as file:
        file.write(html)