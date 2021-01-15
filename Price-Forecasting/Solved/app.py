# Import libraries and dependencies
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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