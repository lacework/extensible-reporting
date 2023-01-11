import logging
logger = logging.getLogger(__name__)

from . import lw

def _get_start_end_times(day_delta=2):
    from datetime import datetime, timezone, timedelta
    
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(days=day_delta)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return start_time, end_time

def query(query, start_end_times=_get_start_end_times()):
    logger.info('Running LQL query')
    
    start_time, end_time = start_end_times
    response = lw().queries.execute(
        query_text = query,
        arguments = {
            "StartTimeRange": start_time,
            "EndTimeRange": end_time,
        }
    )
    return response['data']