def compliance_findings_summary_by_service_bar(df, width=600, height=350, format='svg'):
	import plotly.graph_objects as go
	
	# colors = [
	# 	'crimson',
	# 	'darkorange',
	# 	'gold',
	# 	'lightskyblue',
	# 	'powderblue'
	# ]

	categories = df.columns
	graph_data = []
	for acct, data in df.iterrows():
		bar = go.Bar(name=acct, x=categories, y=data)
		graph_data.append(bar)
	
	fig = go.Figure(
		data=graph_data
	)

	fig.update_layout(
	    title='Compliance Severities by Service',
	    yaxis=dict(
	        title='Failed resources'
	    ),
	    barmode='group'
	)

	img_bytes = fig.to_image(format=format, width=width, height=height)
	return img_bytes
