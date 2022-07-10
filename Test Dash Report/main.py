import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data_full = pd.read_csv("avocado.csv")
data_full = data_full[~data_full['region'].isin(
    ['West', 'Northeast', 'SouthCentral', 'Midsouth', 'Southeast', 'TotalUS West', 'TotalUS'])]
data_full['Date'] = pd.to_datetime(data_full['Date'])
data = data_full.copy()
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)


app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Avocado Analytics",),
        html.Div(className='row', children=[
            html.Div([
                dcc.Dropdown(
                    id='selected_year',
                    options=[{'label': year, 'value': year} for year in data['year'].unique()],
                    value=data['year'].unique().max(),
                    clearable=False
                ),
            ], className='three columns'),
        ]),
        html.Div(className='row', children=[
            html.Div([
                dcc.Graph(
                    id='bar_stack'
                ),
            ], className='four columns'),
            html.Div([
                dcc.Graph(
                    id='total_amount_by_region'
                ),
            ], className='eight columns'),
        ]),

        html.Div(className='row', children=[
            html.Div([
                dcc.Graph(
                    id='sun_chart'
                ),
            ], className='four columns'),
            html.Div([
                dcc.Graph(
                    id='trend'
                ),
                dcc.RadioItems(
                    id='trend-resample',
                    options=[
                        {'label': 'Week', 'value': 'W'},
                        {'label': 'Month', 'value': 'M'},
                        {'label': 'Quarter', 'value': 'Q'}
                    ],
                    value='W',
                    labelStyle={'display': 'inline-block'}
                ),
            ], className='eight columns'),
        ]),

        html.Div(className='row', children=[
            html.Div([
                dcc.Graph(
                    id='pie_bags',
                ),
            ], className='four columns'),
            html.Div([
                dcc.Graph(
                    id='avg_price_v_total_amount'
                ),
            ], className='eight columns'),
        ]),

        html.Div(className='row', children=[
            html.Div([
                dcc.Graph(
                    id='animation_bar',
                ),
            ], className='twelve columns'),
        ]),

    ]
)

@app.callback(
    Output('total_amount_by_region', 'figure'),
    [Input('selected_year', 'value'),
     Input('bar_stack', 'selectedData')]
)
def update_graph(year, bar_stack):
    df = data_full.copy()

    bags = 'Total Volume'

    if bar_stack:
        if bar_stack['points'][0]['curveNumber'] == 2:
            bags = 'XLarge Bags'
        if bar_stack['points'][0]['curveNumber'] == 1:
            bags = 'Large Bags'
        if bar_stack['points'][0]['curveNumber'] == 0:
            bags = 'Small Bags'

    if year:
        df = df.loc[df['year'] == int(year)]

    df = df.loc[:, [bags, 'year', 'region']].\
        groupby(['year', 'region'], as_index=False).sum()

    fig = px.bar(df, x="region", y=bags, log_y=True, labels={'region': ''}, title='Total Volume by Region')
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(clickmode='event+select')
    # fig.update_layout(yaxis_range=[0, 2000000000])
    return fig


@app.callback(
    Output('avg_price_v_total_amount', 'figure'),
    Input('selected_year', 'value')
)
def update_graph2(year):
    df = data_full.copy()

    if year:
        df = df.loc[df['year'] == int(year)]

    df = df.loc[:, ['region', 'AveragePrice', 'Total Volume']]\
        .groupby('region', as_index=False).agg({'AveragePrice': 'mean', 'Total Volume': 'sum'})
    fig = px.scatter(df, x="region", y="AveragePrice", size="Total Volume", hover_name="Total Volume",
                     labels={'AveragePrice': 'Average Price', 'region': ''},
                     title='Total Amount by Average Price and Region')
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(clickmode='event+select')
    return fig

@app.callback(
    Output('pie_bags', 'figure'),
    [Input('selected_year', 'value'),
     Input('total_amount_by_region', 'selectedData'),
     Input('avg_price_v_total_amount', 'selectedData')]
)
def update_graph3(year, region1, region2):
    df = data_full.copy()
    filter_list = []

    if region1:
        filter_list.extend([point['x'] for point in region1['points']])

    if region2:
        filter_list.extend([point['x'] for point in region2['points']])

    if len(filter_list) > 0:
        df = df[df['region'].isin(filter_list)]

    if year:
        df = df.loc[df['year'] == int(year)]

    df = df.loc[:, ['year', 'Small Bags', 'Large Bags', 'XLarge Bags']]\
        .groupby('year', as_index=False).sum()
    df = df[['Small Bags', 'Large Bags', 'XLarge Bags']].T.rename_axis('size').reset_index().rename(columns={0: 'count'})
    fig = px.pie(df, values='count', names='size', title='Total Bags sold by Size')
    return fig


@app.callback(
    Output('bar_stack', 'figure'),
    Input('total_amount_by_region', 'selectedData')
)
def update_graph4(selectedData):
    df = data_full.copy()

    if selectedData:
        filter_list = [point['x'] for point in selectedData['points']]
        df = df[df['region'].isin(filter_list)]

    df = df[['year', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags']].groupby('year', as_index=False).sum()
    x = df.loc[:, 'year']
    fig = go.Figure(go.Bar(x=x, y=df.loc[:, 'Small Bags'], name='Small Bags'))
    fig.add_trace(go.Bar(x=x, y=df.loc[:, 'Large Bags'], name='Large Bags'))
    fig.add_trace(go.Bar(x=x, y=df.loc[:, 'XLarge Bags'], name='XLarge Bags'))
    fig.update_layout(barmode='stack')
    fig.update_layout(clickmode='event+select')
    fig.update_layout(title="Total Bags sold By Year")

    return fig


@app.callback(
    Output('sun_chart', 'figure'),
    Input('total_amount_by_region', 'selectedData')
)
def update_graph3(selectedData):
    df = data_full.copy()

    if selectedData:
        filter_list = [point['x'] for point in selectedData['points']]
        df = df[df['region'].isin(filter_list)]

    df = df[['year', 'type', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags']]\
        .groupby(['year', 'type'], as_index=False).sum()

    fig = px.sunburst(df, path=['year', 'type'], values='Total Bags', title='Bags type by Year %')
    return fig

@app.callback(
    Output('trend', 'figure'),
    [Input('total_amount_by_region', 'selectedData'),
     Input('trend-resample', 'value')]
)
def update_graph3(selectedData, period):
    df = data_full.copy()

    if selectedData:
        filter_list = [point['x'] for point in selectedData['points']]
        df = df[df['region'].isin(filter_list)]

    if period == 'M':
        df = df.loc[df['type'] == 'conventional', ['region', 'Date', 'AveragePrice']]\
            .groupby("region").resample('M', on='Date').mean().reset_index().sort_values(by='Date')

    if period == 'Q':
        df = df.loc[df['type'] == 'conventional', ['region', 'Date', 'AveragePrice']]\
            .groupby("region").resample('Q', on='Date').mean().reset_index().sort_values(by='Date')

    df = df[['Date', 'AveragePrice']]\
        .groupby(['Date'], as_index=False).mean().sort_values('Date')

    fig = px.line(df, x="Date", y="AveragePrice", title='Average Avocado Price',
                  labels={'AveragePrice': 'Average Price', 'Date': ''})
    return fig


@app.callback(
    Output('animation_bar', 'figure'),
    [Input('total_amount_by_region', 'selectedData'),
     Input('avg_price_v_total_amount', 'selectedData')]
)
def update_graph3(region1, region2):
    df = data_full.copy()
    filter_list = []

    if region1:
        filter_list.extend([point['x'] for point in region1['points']])

    if region2:
        filter_list.extend([point['x'] for point in region2['points']])

    if len(filter_list) > 0:
        df = df[df['region'].isin(filter_list)]

    if len(df.region.unique()) <= 10:
        color_col = 'region'
    else:
        color_col = None

    df = df.loc[df['type'] == 'conventional', ['region', 'AveragePrice', 'Date']]
    df = df.groupby("region").resample('M', on='Date').mean().reset_index().sort_values(by=['Date', 'AveragePrice'])
    df['Date'] = df.Date.apply(lambda x: x.date()).apply(str)

    fig = px.bar(df, x="region", y="AveragePrice", orientation="v",
                 animation_frame="Date", animation_group="region", text='region', range_y = [0, 2.1],
                 labels={'AveragePrice': 'Average Price', 'region': 'Region'},
                 title='Avocado Average Price By Date (Animation)', color=color_col)
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    fig.update_layout(xaxis_visible=False, xaxis_showticklabels=False)

    # fig.update_yaxes(range=(-.5, 9.5)) # top 10 val

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 650
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)