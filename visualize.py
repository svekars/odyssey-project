import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('merged.csv')

fig = px.histogram(df, x = 'filename')
fig.show()
