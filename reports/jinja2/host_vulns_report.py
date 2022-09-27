def generate_report(_shared, report_save_path, use_cached_data):
    import os
    from datetime import datetime

    import logging
    logger = logging.getLogger(__name__)

    import jinja2
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    host_vulns = lw_provider.host_vulns(_shared._25_hours_ago, _shared._now)

    # style
    host_vulns_summary_by_host = _shared.t_lw.host_vulns_summary_by_host(host_vulns)
    host_vulns_summary_by_host = host_vulns_summary_by_host.style.set_table_styles({"Severity Count" : [
        {
            "selector" :"td",
            "props": "white-space: pre-wrap; text-align:left"
        }
    ]})

    host_vulns_summary = _shared.t_lw.host_vulns_summary(host_vulns)
    host_vulns_summary_bar_graphic = _shared.g_lw_plotly.host_vulns_by_severity_bar(host_vulns_summary, width=720)
    host_vulns_summary_bar_graphic = _shared.common.bytes_to_image_tag(host_vulns_summary_bar_graphic,'svg+xml')

    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
    TEMPLATE_FILE = "host_vulns_report.html.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    html = template.render(
        host_vulns_total_evaluated=str(_shared.t_lw.host_vulns_total_evaluated(host_vulns)),
        host_vulns_summary_bar_graphic=host_vulns_summary_bar_graphic,
        host_vulns_summary=host_vulns_summary,
        host_vulns_summary_by_host=host_vulns_summary_by_host,
        host_vulns_full_table=_shared.t_lw.host_vulns_full_table(host_vulns),
        date=datetime.now()
    )

    logger.info('Saving report to: ' + report_save_path)

    with open(report_save_path, 'w') as file:
        file.write(html)
