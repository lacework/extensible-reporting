def container_vulns_top_packages_bar(df, width=600, height=350, format='svg'):
	import plotly.graph_objects as go
	
	# Use textposition='auto' for direct text
	fig = go.Figure(data=[go.Bar(x=df['Package Info'], y=df['Count'])])
	fig.update_layout(
	    title='High Priority Packages to Patch (by CVE Count)',
	    yaxis=dict(
	        title='Number of Affected Images'
	    ),
	    xaxis_tickangle=45
	)

	img_bytes = fig.to_image(format=format, width=width, height=height)
	return img_bytes
