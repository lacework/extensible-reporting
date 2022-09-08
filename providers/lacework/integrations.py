from . import lw

def integrations():
	integrations = lw.integrations.get_all()['data']
	return integrations