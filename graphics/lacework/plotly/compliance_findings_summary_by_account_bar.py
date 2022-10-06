def compliance_findings_summary_by_account_bar(df, width=600, height=350, format='svg'):
	import plotly.graph_objects as go
	
	colors = [
		'crimson',
		'darkorange',
		'gold',
		'lightskyblue',
		'powderblue'
	]

	unique_accounts = len(df.index)

	# acct_id, criticals, highs, mediums, lows, infos

	if unique_accounts == 1:
		fig = go.Figure(go.Bar(name="asdf", x=df.columns, y=df.iloc[0], marker_color=colors))
		fig.update_layout(
		    title='Compliance Severities Found',
		    yaxis=dict(
		        title='Failed resources'
		    )
		)
	else:
		severities = df.columns
		graph_data = []
	
		for idx, sev in enumerate(severities):
			bar = go.Bar(name=sev, x=df.index, y=df[sev], marker_color=colors[idx])
			graph_data.append(bar)
		
		fig = go.Figure(
			data=graph_data[::-1]
		)

		fig.update_layout(
		    title='Compliance Severities by Account',
		    yaxis=dict(
		        title='Failed resources'
		    ),
		    barmode='stack'
		)

	img_bytes = fig.to_image(format=format, width=width, height=height)
	return img_bytes
