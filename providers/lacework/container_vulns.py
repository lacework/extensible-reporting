from . import lw
from . import datetime_to_lacework_time

def container_vulns(start_time, end_time, severities=["Critical", "High"]):
    container_vulns = lw.vulnerabilities.containers.search(json={
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
    })
    
    results = []
    i = 0
    for page in container_vulns:
        if i == 4:
            break
        i = i + 1
        results.extend(page['data'])
    return results
