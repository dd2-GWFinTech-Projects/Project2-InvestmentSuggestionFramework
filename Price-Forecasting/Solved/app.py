<<<<<<< HEAD
# Import libraries and dependencies
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
<<<<<<< HEAD
<<<<<<< HEAD
from dash.dependencies import Input, Output

app = dash.Dash()

df = pd.read_csv('../Resources/ATLAS.csv')

df = df.groupby(['Year', 'State', 'Month', 'Subscription', 'Customers Status'])[['Invoice Amount']].sum()
df.reset_index(inplace=True)

# App Layout
app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash", style={"text-align": "center"}),
    dcc.Dropdown(
        id ="slct_year",
        options=[
            {"label": "2015", "values": 2015},
            {"label": "2016", "values": 2016},
            {"label": "2018", "values": 2018},
            {"label": "2019", "values": 2019},
            {"label": "2020", "values": 2020}],
        
        multi=False,
        value=2015,
        #style={'width': "40%"}
        ),
    
    html.Div(id='ouput_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
    
    ])


    # Run
if __name__ == '__main__':
    app.run_server(debug=False)
=======
import dash
import dash_core_components as dcc
import dash_html_components as html
>>>>>>> parent of 826170c... Commit
=======
=======
>>>>>>> parent of 8771e24... New Changes in the breakout room

app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
<<<<<<< HEAD
])
>>>>>>> parent of 8771e24... New Changes in the breakout room
=======
])
>>>>>>> parent of 8771e24... New Changes in the breakout room
