from . import lw
from . import datetime_to_lacework_time

def host_vulns(start_time, end_time):
    host_vulns = lw.vulnerabilities.hosts.search(json={
        "timeFilters": {
            "startTime": datetime_to_lacework_time(start_time),
            "endTime": datetime_to_lacework_time(end_time)
        }
    })
    results = []
    for page in host_vulns:
        print('.')
        results.extend(page['data'])
    return results
    