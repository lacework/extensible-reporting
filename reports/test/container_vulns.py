import json

import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_cached_data):
    import os
    from datetime import datetime

    import jinja2
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw
    
    container_vulns = lw_provider.container_vulns(_shared._25_hours_ago,_shared._now)

    # set table classes
    container_vulns_summary_by_image = _shared.t_lw.container_vulns_summary_by_image(container_vulns)
    container_vulns_summary_by_image = container_vulns_summary_by_image.style.set_table_attributes('class="container_vulns_summary_by_image"')
    container_vulns_summary = _shared.t_lw.container_vulns_summary(container_vulns)
    container_vulns_summary = container_vulns_summary.style.set_table_attributes('class="container_vulns_summary"')

    data = {
        'containers_scanned_count': _shared.t_lw.container_vulns_total_evaluated(container_vulns),
        'container_vulns_summary': container_vulns_summary.to_html(),
        'container_vulns_summary_bar_graphic': '[Container Vulns Summary Bar Graphic Placeholder]',
        'container_vulns_summary_by_image': container_vulns_summary_by_image.to_html(),
        'container_vulns_raw_json': '<pre>' + json.dumps(container_vulns, indent=2) + '</pre>'
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