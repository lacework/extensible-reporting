import logging
logger = logging.getLogger(__name__)

from . import lw

def integrations():
	logger.info('Getting integrations')
	integrations = lw().cloud_accounts.get()
	return integrations['data']