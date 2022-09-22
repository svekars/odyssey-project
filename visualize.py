import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/svekars/odyssey-project/main/log.csv?token=GHSAT0AAAAAABVZYAVGI752FURWOPPNQIM4YZLQPLA')

fig = px.line(df, x = 'changed files', y = 'date', title='Tutorial Updates')
fig.show()
