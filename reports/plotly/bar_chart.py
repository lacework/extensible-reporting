import plotly.graph_objects as go
import pandas as pd
import base64
d = {'Severity': ['Critical', 'High', 'Medium', 'Low'], 'Total CVEs': [97,1794,8910,4671], 'Hosts Affected': [16,27,30,30]}
df = pd.DataFrame(data=d)

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

img_bytes = fig.to_image(format="svg", width=600, height=350)
b64content = base64.b64encode(img_bytes).decode('utf-8')
print(f"<html><body><img src='data:image/svg+xml;base64,{b64content}'/></body></html>")