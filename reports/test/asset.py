import json
import os

import logging
logger = logging.getLogger(__name__)

def generate_report(_shared, report_save_path, use_cached_data):
    import jinja2

    graphic_bytes = _shared.p_local_asset.local_file(os.path.join(os.getcwd(), 'assets/lacework/images/polygraph-info.png'))
    graphic_html = _shared.common.bytes_to_image_tag(graphic_bytes,'png')

    data = {
        'graphic': graphic_html
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