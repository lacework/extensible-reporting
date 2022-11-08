import logging
logger = logging.getLogger(__name__)

from . import lw
from . import datetime_to_lacework_time

def host_vulns(start_time, end_time):
    filters = {
        "timeFilters": {
            "startTime": datetime_to_lacework_time(start_time),
            "endTime": datetime_to_lacework_time(end_time)
        }
    }
    logger.info('Getting Host Vulns with following filters:')
    logger.info(filters)

    host_vulns = lw().vulnerabilities.hosts.search(json=filters)
    results = []
    i = 1
    for page in host_vulns:
        logger.info('Saving page ' + str(i))
        i = i + 1
        results.extend(page['data'])
        break
    if i > 100:
        logger.warning("Lacework API returned maximum pages of host vuln results (100 pages). Processed dataset is likely incomplete.")
    return results
    