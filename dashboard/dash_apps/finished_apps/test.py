import plotly.graph_objs as go

from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1('Hello Dash'),
        dcc.Graph(
            id='slider-graph',
            animate=True,
            style={"backgroundColor": "black", 'color': 'white'}
        ),
        dcc.Slider(
            id='slider-updatemode',
            marks={i: '{}'.format(i) for i in range(1, 6)},
            max=20,
            value=2,
            step=1,
            updatemode='drag'
        )
    ]
)

@app.callback(
    Output('slider-graph', 'figure'),
    [Input('slider-updatemode', 'value')]
)
def display_value(value):
    x = [i for i in range(value)]
    y = [i * i for i in range(value)]
    
    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout  = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white')
    )
    return {'data': [graph], 'layout': layout}