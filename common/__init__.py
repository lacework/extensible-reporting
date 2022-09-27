def bytes_to_image_tag(img_bytes,format):
	import base64
	b64content = base64.b64encode(img_bytes).decode('utf-8')
	return f"<img src='data:image/{format};base64,{b64content}'/>"