import json

import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_cached_data):
    import os
    from datetime import datetime

    import jinja2
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw
    
    events = lw_provider.events(_shared._25_hours_ago,_shared._now)

    data = {
        'events_raw_json': '<pre>' + json.dumps(events, indent=2) + '</pre>'
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