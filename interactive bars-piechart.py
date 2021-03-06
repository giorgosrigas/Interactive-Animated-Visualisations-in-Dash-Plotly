import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

dff = pd.read_csv('master.csv')

dff['Country'] = dff['Year-Country'].str[:-4] # separate column with only the country in the new dataframe
dff['Year'] = dff['Year-Country'].str[-4:] # separate column with only the year in the new dataframe
dff3 =dff
#dff['Year'] = dff['Year'].apply(pd.to_numeric)
dff2 = dff[(dff['Year'] == '1985') | (dff['Year'] == '1990')| (dff['Year'] == '1995')| (dff['Year'] == '2000')
   | (dff['Year'] == '2005') | (dff['Year'] == '2010') | (dff['Year'] == '2015')]
dff = dff2.sort_values(by='Year')
dff['Total_suicides_number'] = dff['suicides_no'] # make name clearer
dff3['Total_suicides_number'] = dff3['suicides_no'] # make name clearer

# make a column with the continents
Asia = [ 'Armenia', 'Kazakhstan','Israel', 'Japan', 'Kuwait', 'Kyrgyzstan', 'Macau',
        'Maldives', 'Mongolia', 'Oman', 'Philippines', 'Qatar', 'Republic of Korea', 'Sri Lanka', 'Thailand'
       , 'Turkmenistan', 'Turkey',  'Uzbekistan']
Europe = ['Albania','Azerbaijan', 'Belarus','Belgium','Bosnia and Herzegovina','Cyprus','Ukraine',
          'Germany','Georgia','Spain', 'France', 'Italy', 'Netherlands', 'Norway', 'Sweden','Czech Republic', 'Finland',
      'Denmark', 'Czech Republic', 'Switzerland', 'United Kingdom', 'Poland', 'Greece','Austria',
      'Bulgaria', 'Luxembourg', 'Romania' , 'Slovakia',  'Slovenia','Portugal',
      'Croatia', 'Lithuania', 'Latvia','Serbia', 'Estonia','Hungary',
       'Iceland', 'Ireland', 'Malta', 'Montenegro', 'Russian Federation', 'San Marino' ]
North_america = ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize','Canada','El Salvador',
                'Grenada', 'Guatemala', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Puerto Rico', 'Saint Vincent and Grenadines'
                , 'United States', 'Saint Lucia, Saint Kitts and Nevis']
South_america = ['Argentina','Aruba', 'Brazil','Chile''Colombia', 'Costa Rica','Cuba','Dominica', 'Ecuador',
       'Guyana', 'Paraguay', 'Trinidad and Tobago', 'Uruguay', 'Suriname']
Oceania = ['Australia', 'Fiji', 'Kiribati', 'New Zealand']
def Continents(country):
    if country in Asia:
        return "Asia"
    elif country in Europe:
        return "Europe"

    elif country in North_america:
        return "North America"
    elif country in South_america:
        return "South America"
    else:
        return 'Oceania'
dff['Continent'] = dff['Country'].apply(lambda x: Continents(x))
dff3['Continent'] = dff3['Country'].apply(lambda x: Continents(x))

# clean column names
dff['Total suicides number' ]=  dff['Total_suicides_number']
dff['Suicide rate per 100k people'] = dff3['suicide rate (deaths per 100,000)']
dff3['Total suicides number' ]=  dff3['Total_suicides_number']
dff3['Suicide rate per 100k people'] = dff3['suicide rate (deaths per 100,000)']

# create a frame with the average rate and the sum of total number
dff= dff.groupby(['sex','age','Year', 'Continent'],as_index=False).aggregate({'Total suicides number':np.sum,'Suicide rate per 100k people':np.average})
dff3= dff3.groupby(['sex','age', 'Continent'],as_index=False).aggregate({'Total suicides number':np.sum,'Suicide rate per 100k people':np.average})
# drop missing values
dff['age'] = dff['age'].str.replace("years", "") #clean the string
dff.dropna(inplace=True)

# CSS sheet for the layout
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
app.layout = html.Div([
    html.Div( [
        html.Div([
            html.Label(['Choose a factor:'],style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='radio_factors',
                options=[
                         {'label': 'Gender', 'value': 'sex'},
                        {'label': 'Continent', 'value': 'Continent'},
                         {'label': 'Age', 'value': 'age'},


                ],
                value='Continent',

            ),
        ],className='three columns'),

        html.Div([
            html.Br(),
            html.Label(['Choose an outcome:'], style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='radio_outcomes',
                options=[
                         {'label': 'Total suicides number', 'value': 'Total suicides number'},
                         {'label': 'Average suicide rate per 100k people', 'value': 'Suicide rate per 100k people'},
                ],
                value='Total suicides number',

            ),
        ],className='three columns'),
],className='row'),


    html.Div([
        html.Div([
            dcc.Graph(id='pie'),
        ],className='four columns'),

        html.Div([
            dcc.Graph(id='bar'),
        ],className='eight columns'),

    ],className='row'),

])
#---------------------------------------------------
# call for conecting the input with our actual graphs
@app.callback(
    [Output( 'pie', 'figure' ),
     Output( 'bar', 'figure' )],
    [Input(component_id='radio_factors', component_property='value'),
     Input(component_id='radio_outcomes', component_property='value')]
)


def update_func(factors, outcomes):
    pie = px.pie(
        data_frame=dff3,
        names=factors,
        values=outcomes,
        color=factors,
        title='Proportion of '+ ' ' + outcomes + '<br>' + ' ' + 'by' + ' ' + factors + ' ' + 'between 1985-2016',
        template='seaborn+gridon',
        width=500,
        height=500)
    pie.update_traces( textinfo='percent',
                                          marker=dict(line=dict( width=1)),
                                      pull=[0, 0, 0, 0], opacity=0.9, rotation=180)

    bar = px.bar(
        data_frame=dff,
        x=factors,
        y=outcomes,
        facet_col='Year',
        opacity=1,
        orientation="v",
        title=' Yearly distribution of suicides by' + ' ' + factors + ' ' + ' for seven different years',
        template='seaborn+gridon',
        width=920,
        height=650,
        labels={'Total_suicides_number': 'Total Suicides Number', 'age': 'Age'
                },
    )
    bar.update_layout( xaxis={'categoryorder': 'total ascending'},

                       )

    return (pie,bar)

if __name__ == '__main__':
    app.run_server(debug=True, port = 8011)