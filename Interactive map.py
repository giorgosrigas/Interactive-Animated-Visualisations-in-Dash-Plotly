import numpy as np
import pandas as pd
import pycountry
import plotly.express as px
import dash  # (version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.io as pio
import dash_bootstrap_components as dbc
#from dash_bootstrap_components import themes
pio.templates.default = "seaborn+presentation"
df = pd.read_csv('master.csv' )
# filtering the data for each year's rate sum
dff = df.groupby( 'Year-Country', as_index=False )[
    'suicide rate (deaths per 100,000)'].sum()  # column with the total number per year
dff['Country'] = dff['Year-Country'].str[:-4]  # separate column with only the country in the new dataframe
dff['Year'] = dff['Year-Country'].str[-4:] # separate column with only the year in the new dataframe
dff['Year'] = dff['Year'].apply( pd.to_numeric )

def search(country):
    try:
        result = pycountry.countries.search_fuzzy( country )
    except Exception:
        return np.nan
    else:
        return result[0].alpha_3


iso_code = {i: search( i ) for i in dff["Country"].unique()}

dff["code"] = dff["Country"].map( iso_code )  # column with the iso_code to be recognized


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SUPERHERO] )
app.layout = html.Div( [

    html.Div( [
        dcc.Graph( id='graph' , style={'height': 600, 'width': 1500, 'display': 'flex'})
    ]),

    html.Div( [
        html.P("Change the year"),

        dcc.Input( id='input_state', type='number', inputMode='numeric', value=2007,
                   max=2016, min=1985, step=1, required=True ),
        html.Button( id='button', n_clicks=0, children='Submit' ),
        html.Div( id='output' ),
    ], style={'width': '82%', 'text-align': 'center', 'fontColor' : 'white'} ),

] )

#callback for conencting the output ewith the input

@app.callback(
    [Output( 'output', 'children' ),
     Output( component_id='graph', component_property='figure' )],
    [Input( component_id='button', component_property='n_clicks' )],
    [State( component_id='input_state', component_property='value' )]
)

def update_output(clicks, val):
    if val == None:
        raise PreventUpdate
    else:
        #filter the data
        dd = dff[dff['Year'] == val]

        choro = px.choropleth( dd, locations="code",
                               color="suicide rate (deaths per 100,000)",
                               hover_name="Country",
                               #projection= 'natural earth',
                               scope= 'world',

                               title='Yearly Suicide Rate by Country',
                               color_continuous_scale=px.colors.sequential.ice[::-1] )

        choro.update_layout( title=dict( font=dict( size=31 ), x=0.45, xanchor='center' ),
                             margin=dict( l=70, r=70, t=60, b=60 ), geo=dict(bgcolor= 'rgba(0,0,0,0)'))

        return ('We are on the year {} and the user has clicked \
                the button {} times'.format( val, clicks ), choro)


if __name__ == '__main__':
    app.run_server( debug=True, port = 844)
