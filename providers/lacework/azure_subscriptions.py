import logging
logger = logging.getLogger(__name__)

from . import lw
from . import LWApiError

import json
   
def azure_subscriptions(tenant_id=''):
    results = []
    
    try:
        logger.info('Getting Subscriptions for Azure tenant: ' + tenant_id)
        a = lw().compliance.list_azure_subscriptions( azure_tenant_id=tenant_id)
        results.extend(a['data'][0]['subscriptions'])
    except LWApiError:
        logger.warning('Could not get subscriptions for azure tenant: ' + tenant_id)

    return results