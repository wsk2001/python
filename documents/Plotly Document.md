#### Simple OHLC Chart with Pandas

출처: https://plotly.com/python/ohlc-charts/



#### Simple OHLC Chart with Pandas

``` py
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['AAPL.Open'],
                    high=df['AAPL.High'],
                    low=df['AAPL.Low'],
                    close=df['AAPL.Close']))
fig.show()
```





#### OHLC Chart without Rangeslider

``` py
import plotly.graph_objects as go

import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=go.Ohlc(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close']))
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()
```



#### Adding Customized Text and Annotations

``` py
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=go.Ohlc(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close']))

fig.update_layout(
    title='The Great Recession',
    yaxis_title='AAPL Stock',
    shapes = [dict(
        x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    annotations=[dict(
        x='2016-12-09', y=0.05, xref='x', yref='paper',
        showarrow=False, xanchor='left', text='Increase Period Begins')]
)

fig.show()
```



#### Custom OHLC Colors

``` py
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=[go.Ohlc(
    x=df['Date'],
    open=df['AAPL.Open'], high=df['AAPL.High'],
    low=df['AAPL.Low'], close=df['AAPL.Close'],
    increasing_line_color= 'cyan', decreasing_line_color= 'gray'
)])
fig.show()
```



#### Simple OHLC with `datetime` Objects

``` py
import plotly.graph_objects as go

from datetime import datetime

open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
dates = [datetime(year=2013, month=10, day=10),
         datetime(year=2013, month=11, day=10),
         datetime(year=2013, month=12, day=10),
         datetime(year=2014, month=1, day=10),
         datetime(year=2014, month=2, day=10)]

fig = go.Figure(data=[go.Ohlc(x=dates,
                          open=open_data, high=high_data,
                          low=low_data, close=close_data)])
fig.show()
```



### Custom Hovertext

``` py
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

hovertext=[]
for i in range(len(df['AAPL.Open'])):
    hovertext.append('Open: '+str(df['AAPL.Open'][i])+'<br>Close: '+str(df['AAPL.Close'][i]))

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=go.Ohlc(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'],
                text=hovertext,
                hoverinfo='text'))
fig.show()
```



#### Reference

캔들 속성에 대한 자세한 내용은 https://plotly.com/python/reference/ohlc/를 참조하십시오.



### 대시(Dash)는 어떻습니까?

Dash는 Javascript가 필요하지 않은 분석 애플리케이션을 구축하기 위한 오픈 소스 프레임워크이며 Plotly 그래프 라이브러리와 긴밀하게 통합됩니다.

https://dash.plot.ly/installation에서 Dash를 설치하는 방법에 대해 알아보세요.

이 페이지에서 fig.show()를 볼 수 있는 모든 곳에서 다음과 같이 내장 dash_core_components 패키지에서 Graph 구성 요소의 figure 인수로 전달하여 동일한 그림을 Dash 애플리케이션에 표시할 수 있습니다.



``` py
import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
```

