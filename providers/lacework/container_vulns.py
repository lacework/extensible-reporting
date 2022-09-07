from . import lw
from . import datetime_to_lacework_time

def container_vulns(start_time, end_time):
    container_vulns = lw.vulnerabilities.containers.search(json={
        "timeFilters": {
            "startTime": datetime_to_lacework_time(start_time),
            "endTime": datetime_to_lacework_time(end_time)
        }
    })
    
    results = []
    for page in container_vulns:
        print('.')
        results.extend(page['data'])
    return results
