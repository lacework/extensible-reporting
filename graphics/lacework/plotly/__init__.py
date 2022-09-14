from .host_vulns_by_severity_bar import host_vulns_by_severity_bar

def bytes_to_image_tag(img_bytes):
	import base64
	b64content = base64.b64encode(img_bytes).decode('utf-8')
	return f"<img src='data:image/svg+xml;base64,{b64content}'/>"