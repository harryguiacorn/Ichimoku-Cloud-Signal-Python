import plotly.graph_objects as go
import numpy as np

import pandas as pd
from datetime import datetime
pd.options.plotting.backend = "plotly"

# sample data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
df.index = df.Date
df = df[['AAPL.Close', 'mavg']]
df['mavg2'] = df['AAPL.Close'].rolling(window=50).mean()
df.columns = ['y', 'ma1', 'ma2']
df=df.tail(250).dropna()
df1 = df.copy()

# split data into chunks where averages cross each other
df['label'] = np.where(df['ma1']>df['ma2'], 1, 0)
df['group'] = df['label'].ne(df['label'].shift()).cumsum()
df = df.groupby('group')
dfs = []
for name, data in df:
    dfs.append(data)

# custom function to set fill color
def fillcol(label):
    print(label)
    if label >= 1:
        return 'rgba(0,250,0,0.4)'
    else:
        return 'rgba(250,0,0,0.4)'

fig = go.Figure()

for df in dfs:
    fig.add_traces(go.Scatter(x=df.index, y = df.ma1,
                              line = dict(color='rgba(0,0,0,0)')))
    
    fig.add_traces(go.Scatter(x=df.index, y = df.ma2,
                              line = dict(color='rgba(0,0,0,0)'),
                              fill='tonexty', 
                              fillcolor = fillcol(df['label'].iloc[0])))

# include averages
fig.add_traces(go.Scatter(x=df1.index, y = df1.ma1,
                          line = dict(color = 'blue', width=1)))

fig.add_traces(go.Scatter(x=df1.index, y = df1.ma2,
                          line = dict(color = 'red', width=1)))

# include main time-series
fig.add_traces(go.Scatter(x=df1.index, y = df1.y,
                          line = dict(color = 'black', width=2)))

fig.update_layout(showlegend=False)
fig.show()