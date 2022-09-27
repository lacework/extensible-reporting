import json

import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_cached_data):
    import os
    from datetime import datetime

    import jinja2
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    host_vulns = lw_provider.host_vulns(_shared._25_hours_ago, _shared._now)

    # set table classes
    host_vulns_summary_by_host = _shared.t_lw.host_vulns_summary_by_host(host_vulns)
    host_vulns_summary_by_host = host_vulns_summary_by_host.style.set_table_attributes('class="host_vulns_summary_by_host"')
    host_vulns_summary_data = _shared.t_lw.host_vulns_summary(host_vulns)
    host_vulns_summary = host_vulns_summary_data.style.set_table_attributes('class="host_vulns_summary"')    

    # get graphics
    host_vulns_summary_bar_graphic = _shared.g_lw_plotly.host_vulns_by_severity_bar(host_vulns_summary_data, width=750)
    host_vulns_summary_bar_graphic = _shared.g_lw_plotly.bytes_to_image_tag(host_vulns_summary_bar_graphic)

    data = {
        'hosts_scanned_count': _shared.t_lw.host_vulns_total_evaluated(host_vulns),
        'host_vulns_summary': host_vulns_summary.to_html(),
        'host_vulns_summary_bar_graphic': host_vulns_summary_bar_graphic,
        'host_vulns_summary_by_host': host_vulns_summary_by_host.to_html(),
        'host_vulns_raw_json': '<pre>' + json.dumps(host_vulns, indent=2) + '</pre>'
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