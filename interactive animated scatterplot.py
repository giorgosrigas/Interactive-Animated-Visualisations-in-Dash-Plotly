import pandas as pd
import plotly.express as px
import dash  # (version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.io as pio
import statsmodels as sm

pio.templates.default = "plotly_dark+xgridoff"

df16 = pd.read_csv( 'Happiness.csv' )
# make column names more readable
df16['Social Support Score'] = df16['Family']
df16['Economy-GDP per Capita Score'] = df16['Economy (GDP per Capita)']
df16['Health Index Score'] = df16['Health (Life Expectancy)']
df16['Freedom Score'] = df16['Freedom']
df16['Generosity Score'] = df16['Generosity']

# create a list with column names of predictors for later iteration over the columns
cols1 = list( df16 )[10:]

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash( __name__, external_stylesheets=external_stylesheets )
app.layout = html.Div( [
    html.Div( [
        html.Label( ['Compare between Regions:'], style={'font-weight': 'bold'} ),
        # dropdowns which iterate over all the unique values of region column
        dcc.Dropdown(
            id='Region1',
            options=[{'label': x, 'value': x} for x in df16.sort_values( 'Region' )['Region'].unique()],
            value='Western Europe',
            multi=False,
            clearable=False,
            # style={"width": "50%"},
            persistence_type='memory' ),
        dcc.Dropdown(
            id='Region2',
            options=[{'label': x, 'value': x} for x in df16.sort_values( 'Region' )['Region'].unique()],
            value='Latin America and Caribbean',
            multi=False,
            clearable=False,
            # style={"width": "50%"},
            persistence_type='session' ),
        dcc.Dropdown(
            id='Region3',
            options=[{'label': x, 'value': x} for x in df16.sort_values( 'Region' )['Region'].unique()],
            value='Sub-Saharan Africa',
            multi=False,
            clearable=False,
            # style={"width": "50%"},
            persistence_type='local' ),

    ], className='four columns' ),
    html.Div( [
        html.Label( ['Change x-axis predictor for happiness:'], style={'font-weight': 'bold'},
                    ),

        dcc.Dropdown(
            id='drop2',
            options=[{'label': x, 'value': x} for x in cols1],
            value='Economy-GDP per Capita Score',
            # style=dict( display='inline-block', justifyContent='center' , width = '59%', height = '100%'),

        ),
    ], className='four columns' ),

    html.Div( [
        html.Label( ['Regression statistics:'], style={'font-weight': 'bold'},
                    ),
        # radio-items for choosing to have regression line
        dcc.RadioItems(
            id='radio',
            options=[{'label': 'Add regression line', 'value': 'graph1'},
                     {'label': 'Remove  regression line', 'value': 'graph2'}],
            value='graph2',
            # style=dict( display='inline-block', justifyContent='center', width='50%', height='100%' ),

        ),
    ], className='four columns' ),

    html.Div(
        dcc.Graph( id='the_graph',
                   style={'height': 600, 'width': 1100, 'display': 'flex'}
                   ),

    ),

] )


# ---------------------------------------------------------------
@app.callback(
    Output( 'the_graph', 'figure' ),
    [Input( 'Region1', 'value' ),
     Input( 'Region2', 'value' ),
     Input( 'Region3', 'value' ),
     Input( 'drop2', 'value' ),
     Input( 'radio', 'value' )]
)
#function for updating the graph
def update_graph(first_region, second_region, third_region, predictor, value):
    #filtering the data
    dff = df16[(df16['Region'] == first_region) |
               (df16['Region'] == second_region) |
               (df16['Region'] == third_region)]
    if value == 'graph1':
        scat = px.scatter(
            dff,
            x=predictor,
            y="Happiness Score",
            color="Region",
            # size="Health (Life Expectancy)",
            size_max=60,
            opacity=0.65,
            title='Relationship between happiness and' + ' ' + str( predictor ),
            trendline='ols',
            hover_name='Country',
            animation_frame='Year',
            range_x=[min( dff[predictor] ), max( dff[predictor] ) + 0.2],  # set range of x-axis
            range_y=[2.0, 9.00],  # set range of y-axis
            category_orders={'Year': [2015, 2016, 2017, 2018, 2019]},  # set a specific ordering of values

        )

        scat.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1300
        scat.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 700
        scat.update_layout( title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                            )

        scat.update_traces( marker=dict( size=13,
                                         line=dict( width=0.40,
                                                    color='DarkSlateGrey' ) ),
                            selector=dict( mode='markers' ) )
        return scat

    else:
        scat2 = px.scatter(
            dff,
            x=predictor,
            y="Happiness Score",
            color="Region",
            size_max=60,
            opacity=0.65,
            title='Relationship between happiness and' + ' ' + str( predictor ),
            hover_name='Country',
            animation_frame='Year',
            range_x=[min( dff[predictor] ), max( dff[predictor] ) + 0.2],  # set range of x-axis
            category_orders={'Year': [2015, 2016, 2017, 2018, 2019]},  # set a specific ordering of values =

        )

        scat2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1300
        scat2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 700
        scat2.update_layout( title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                             )

        scat2.update_traces( marker=dict( size=13,
                                          line=dict( width=0.40,
                                                     color='DarkSlateGrey' ) ),
                             selector=dict( mode='markers' ) )
        return scat2


if __name__ == '__main__':
    app.run_server( debug=True, port=8019 )
