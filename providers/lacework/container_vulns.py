import logging
logger = logging.getLogger(__name__)

from . import lw
from . import datetime_to_lacework_time

def container_vulns(start_time, end_time, severities=["Critical", "High"]):
    filters = {
        "timeFilters": {
            "startTime": datetime_to_lacework_time(start_time),
            "endTime": datetime_to_lacework_time(end_time)
        },
        "filters": [
            {"field": "status", "expression": "eq", "value": "VULNERABLE"},
            {
                "field": "severity",
                "expression": "in",
                "values": severities,
            }
        ]
    }
    logger.info('Getting Container Vulnerabilities with following filters:')
    logger.info(filters)
    container_vulns = lw().vulnerabilities.containers.search(json=filters)
    
    results = []

    # logger.info('Found ' + len(container_vulns) + ' pages of data')
    i = 1
    for page in container_vulns:
        logger.info('Saving page ' + str(i))
        i = i + 1
        results.extend(page['data'])
    if i > 100:
        logger.warning("Lacework API returned maximum pages of container vuln results (100 pages). Processed dataset is likely incomplete.")
    return results
