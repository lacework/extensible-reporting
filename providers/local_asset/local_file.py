def local_file(path):
	with open(path, "rb") as in_file:
	    file_bytes = in_file.read()
	return file_bytes