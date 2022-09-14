def host_vulns_by_severity_bar(df, width=600, height=350, format='svg'):
	import plotly.graph_objects as go
	
	colors = [
		'crimson',
		'darkorange',
		'gold',
		'lightskyblue'
	]


	# Use textposition='auto' for direct text
	fig = go.Figure(data=[go.Bar(x=df['Severity'], y=df['Total CVEs'], marker_color=colors)])

	fig.update_layout(
	    title='Severities by CVE',
	    yaxis=dict(
	        title='Number of CVEs'
	    )
	)

	img_bytes = fig.to_image(format=format, width=width, height=height)
	return img_bytes
