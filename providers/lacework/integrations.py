import logging
logger = logging.getLogger(__name__)

from . import lw

def integrations():
	logger.info('Getting integrations')
	integrations = lw().integrations.get_all()['data']
	return integrations