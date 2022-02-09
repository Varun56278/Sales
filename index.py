import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
 
 
sales1 = pd.read_csv("train.csv", encoding='unicode_escape')
 
app = dash.Dash(__name__,)
app.layout = html.Div([
 
html.Div([
    html.Br(), html.Br(),
    html.H1('Sample Sales Data Dashboard')],
    style={'margin-left': '5%','color':'#808000','width': '50%', 'display': 'inline-block'
 
    }),
 
html.Div([
    html.Br(), html.Br(),
    html.H4('Prepared by: SACHIN RAJPUT')],
    style={'color':'#17202A','width': '30%', 'display': 'inline-block', 'float': 'right'
 
    }),
 
html.Div([
        html.Label('Select a Country:'),
        dcc.Dropdown(id='w_countries',
                     multi=False,
                     clearable=True,
                     value='Australia',
                     placeholder='Select Countries',
                     options=[{'label': c, 'value': c}
                              for c in (sales1['COUNTRY'].unique())])
 
         ], style={'width': '10%','margin-left': '45%'}),
 
# Create combination of bar chart and line chart (Compare quantity ordered to each price of product)
html.Div([
    html.Br(),
    dcc.Graph(id='bar_line_1',
              config={'displayModeBar': False}),
 
        ],style={'margin-left': '1.4%','width': '50%', 'display': 'inline-block'}),
 
# Create combination of bar chart and line chart (Compare sales to each price of product)
html.Div([
    html.Br(),
    dcc.Graph(id='bar_line_2',
              config={'displayModeBar': False}),
 
        ],style={'width': '48.6%', 'display': 'inline-block', 'float': 'right'}),
 
# Create group bar chart (Compare sales and quantity ordered for each product)
html.Div([
    html.Br(),
    dcc.Graph(id='bar_bar_3',
              config={'displayModeBar': False}),
 
        ],style={'margin-left': '1.4%','width': '50%', 'display': 'inline-block'}),
 
# Create combination of bar chart and line chart (Compare each year sales and q. ordered for each product)
html.Div([
    html.Br(),
    dcc.Graph(id='bar_line_4',
              config={'displayModeBar': False}),
 
        ],style={'width': '48.6%', 'display': 'inline-block', 'float': 'right'}),
 
# Create line chart (each month sales)
html.Div([
    html.Br(),
    dcc.Graph(id='line_line_5',
              config={'displayModeBar': False}),
 
        ],style={'margin-left': '1.4%','width': '50%', 'display': 'inline-block', 'margin-bottom':'3%'}),
 
# Create scatter chart (Compare sales and q. ordered)
html.Div([
        html.Br(),
        dcc.Graph(id='scatter_6',
                  config={'displayModeBar': False}),
 
    ], style={'width': '48.6%', 'display': 'inline-block', 'float': 'right', 'margin-bottom':'3%'}),
 
 
  ], style={'background-color': '#e6e6e6'})
 
# Create combination of bar chart and line chart (Compare quantity ordered to each price of product)
@app.callback(Output('bar_line_1', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# Data for bar
    product_sales1 = sales1.groupby(['PRODUCTLINE', 'COUNTRY'])['QUANTITYORDERED'].sum().reset_index()
# Data for line
    product_sales2 = sales1.groupby(['PRODUCTLINE', 'COUNTRY'])['PRICEEACH'].mean().reset_index()
 
    return {
        'data': [go.Bar(x=product_sales1[product_sales1['COUNTRY'] == w_countries]['PRODUCTLINE'],
                        y=product_sales1[product_sales1['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                        text=product_sales1[product_sales1['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                        name='Quantity Ordered',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        marker=dict(
                            color=product_sales1[product_sales1['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                            colorscale='phase',
                            showscale=False),
                        yaxis='y1',
 
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + product_sales1[product_sales1['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Q.Ordered</b>: ' + [f'{x:,.0f}' for x in product_sales1[product_sales1['COUNTRY'] == w_countries]['QUANTITYORDERED']] + '<br>'+
                        '<b>Product</b>: ' + product_sales1[product_sales1['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'
 
 
                        ),
 
                go.Scatter(
                            x=product_sales2[product_sales2['COUNTRY'] == w_countries]['PRODUCTLINE'],
                            y=product_sales2[product_sales2['COUNTRY'] == w_countries]['PRICEEACH'],
                            name='Price of Product',
                            text=product_sales2[product_sales2['COUNTRY'] == w_countries]['PRICEEACH'],
                            mode='markers + lines',
                            marker=dict(color='#bd3786'),
                            yaxis='y2',
                            hoverinfo='text',
                            hovertext=
                            '<b>Country</b>: ' + product_sales2[product_sales2['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                            '<b>Price</b>: $' + [f'{x:,.0f}' for x in product_sales2[product_sales2['COUNTRY'] == w_countries]['PRICEEACH']] + '<br>'+
                            '<b>Product</b>: ' + product_sales2[product_sales2['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'
                            )],
 
 
        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Quantity ordered and price of each product : ' + (w_countries),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
 
             hovermode='x',
 
             xaxis=dict(title='<b>Name of Product</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
 
                ),
 
             yaxis=dict(title='<b>Quantity Ordered</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
 
                ),
             yaxis2=dict(title='<b>Price of Each Product ($)</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )
 
                 ),
 
             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),
 
                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',
 
                 )
 
    }
 
# Create combination of bar chart and line chart (Compare sales to each price of product)
@app.callback(Output('bar_line_2', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# Data for bar
    product_sales3 = sales1.groupby(['PRODUCTLINE', 'COUNTRY'])['SALES'].sum().reset_index()
# Data for line
    product_sales4 = sales1.groupby(['PRODUCTLINE', 'COUNTRY'])['PRICEEACH'].mean().reset_index()
 
    return {
        'data': [go.Bar(x=product_sales3[product_sales3['COUNTRY'] == w_countries]['PRODUCTLINE'],
                        y=product_sales3[product_sales3['COUNTRY'] == w_countries]['SALES'],
                        text=product_sales3[product_sales3['COUNTRY'] == w_countries]['SALES'],
                        name='Total Sales',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        marker=dict(
                            color=product_sales3[product_sales3['COUNTRY'] == w_countries]['SALES'],
                            colorscale='portland',
                            showscale=False),
                        yaxis='y1',
 
 
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + product_sales3[product_sales3['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Sales</b>: $' + [f'{x:,.0f}' for x in product_sales3[product_sales3['COUNTRY'] == w_countries]['SALES']] + '<br>'+
                        '<b>Product</b>: ' + product_sales3[product_sales3['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'
 
                        ),
 
                go.Scatter(
                            x=product_sales4[product_sales4['COUNTRY'] == w_countries]['PRODUCTLINE'],
                            y=product_sales4[product_sales4['COUNTRY'] == w_countries]['PRICEEACH'],
                            name='Price of Product',
                            text=product_sales4[product_sales4['COUNTRY'] == w_countries]['PRICEEACH'],
                            mode='markers + lines',
                            marker=dict(color='#bd3786'),
                            yaxis='y2',
                            hoverinfo='text',
                            hovertext=
                            '<b>Country</b>: ' + product_sales4[product_sales4['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                            '<b>Product</b>: ' + product_sales4[product_sales4['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'+
                            '<b>Price</b>: $' + [f'{x:,.0f}' for x in product_sales4[product_sales4['COUNTRY'] == w_countries]['PRICEEACH']] + '<br>'
                            )],
 
 
        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Total Sales and price of each product : ' + (w_countries),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
 
             hovermode='x',
 
             xaxis=dict(title='<b>Name of Product</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
 
                ),
 
             yaxis=dict(title='<b>Total Sales</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
 
                ),
             yaxis2=dict(title='<b>Price of Each Product ($)</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )
 
                 ),
 
             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),
 
                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',
 
                 )
 
    }
 
# Create group bar chart (Compare sales and quantity ordered for each product)
@app.callback(Output('bar_bar_3', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# Data for bar
    product_sales5 = sales1.groupby(['PRODUCTLINE', 'COUNTRY'])['SALES'].sum().reset_index()
# Data for line
    product_sales6 = sales1.groupby(['PRODUCTLINE', 'COUNTRY'])['QUANTITYORDERED'].sum().reset_index()
 
    return {
        'data': [go.Bar(x=product_sales5[product_sales5['COUNTRY'] == w_countries]['PRODUCTLINE'],
                        y=product_sales5[product_sales5['COUNTRY'] == w_countries]['SALES'],
                        text=product_sales5[product_sales5['COUNTRY'] == w_countries]['SALES'],
                        name='Total Sales',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        # marker=dict(
                        #     color=product_sales5[product_sales5['COUNTRY'] == w_countries]['SALES'],
                        #     colorscale='portland',
                        #     showscale=False),
                        marker = dict(color='rgb(214, 137, 16)'),
                        yaxis='y1',
                        offsetgroup=1,
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + product_sales5[product_sales5['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Product</b>: ' + product_sales5[product_sales5['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'+
                        '<b>Total Sales</b>: $' + [f'{x:,.0f}' for x in product_sales5[product_sales5['COUNTRY'] == w_countries]['SALES']] + '<br>'
                        ),
 
                go.Bar(
                            x=product_sales6[product_sales6['COUNTRY'] == w_countries]['PRODUCTLINE'],
                            y=product_sales6[product_sales6['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                            name='Total Q. Ordered',
                            text=product_sales6[product_sales6['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                            texttemplate='%{text:.2s}',
                            textposition='auto',
                            marker=dict(color='rgb(112, 123, 124)'),
                            yaxis='y2',
                            offsetgroup=2,
                            hoverinfo='text',
                            hovertext=
                            '<b>Country</b>: ' + product_sales6[product_sales6['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                            '<b>Product</b>: ' + product_sales6[product_sales6['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'+
                            '<b>Total Q. Ordered</b>: ' + [f'{x:,.0f}' for x in product_sales6[product_sales6['COUNTRY'] == w_countries]['QUANTITYORDERED']] + '<br>'
                            )],
 
 
        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Total Sales and Quantity ordered of each product : ' + (w_countries),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
 
             hovermode='x',
 
             xaxis=dict(title='<b>Name of Product</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
 
                ),
 
             yaxis=dict(title='<b>Total Sales</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
 
                ),
             yaxis2=dict(title='<b>Total Quantity Ordered</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )
 
                 ),
 
             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),
 
                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',
 
                 )
 
    }
 
# Create combination of bar chart and line chart (Compare each year sales and q. ordered for each product)
@app.callback(Output('bar_line_4', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# Data for bar
    product_sales7 = sales1.groupby(['COUNTRY', 'YEAR_ID'])['SALES'].sum().reset_index()
# Data for line
    product_sales8 = sales1.groupby(['COUNTRY', 'YEAR_ID'])['QUANTITYORDERED'].sum().reset_index()
 
    return {
        'data': [go.Bar(x=product_sales7[product_sales7['COUNTRY'] == w_countries]['YEAR_ID'],
                        y=product_sales7[product_sales7['COUNTRY'] == w_countries]['SALES'],
                        text=product_sales7[product_sales7['COUNTRY'] == w_countries]['SALES'],
                        name='Total Sales',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        # marker=dict(
                        #     color=product_sales1[product_sales1['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                        #     colorscale='phase',
                        #     showscale=False),
                        marker = dict(color='rgb(11, 220, 239)'),
                        yaxis='y1',
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + product_sales7[product_sales7['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Total Sales</b>: $' + [f'{x:,.0f}' for x in product_sales7[product_sales7['COUNTRY'] == w_countries]['SALES']] + '<br>'+
                        '<b>Year</b>: ' + product_sales7[product_sales7['COUNTRY'] == w_countries]['YEAR_ID'].astype(str) + '<br>'
                        ),
 
                go.Scatter(
                            x=product_sales8[product_sales8['COUNTRY'] == w_countries]['YEAR_ID'],
                            y=product_sales8[product_sales8['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                            name='Total Q. Ordered',
                            text=product_sales8[product_sales8['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                            mode='markers + lines',
                            marker=dict(color='#bd3786'),
                            yaxis='y2',
                            hoverinfo='text',
                            hovertext=
                            '<b>Country</b>: ' + product_sales8[product_sales8['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                            '<b>Total Q. Ordered</b>: ' + [f'{x:,.0f}' for x in product_sales8[product_sales8['COUNTRY'] == w_countries]['QUANTITYORDERED']] + '<br>'+
                            '<b>Year</b>: ' + product_sales8[product_sales8['COUNTRY'] == w_countries]['YEAR_ID'].astype(str) + '<br>'
                            )],
 
 
        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Yearly sales and quantity ordered for each product : ' + (w_countries),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
 
             hovermode='x',
 
             xaxis=dict(title='<b>Name of Product</b>',
                        tick0=0,
                        dtick=1,
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
 
                ),
 
             yaxis=dict(title='<b>Total Sales</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
 
                ),
             yaxis2=dict(title='<b>Total Q. Ordered</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )
 
                 ),
 
             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),
 
                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',
 
                 )
 
    }
 
# Create line chart (each month sales)
@app.callback(Output('line_line_5', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# Data for line
    monthly_sales = sales1.groupby(['COUNTRY','YEAR_ID','MONTH_ID'])['SALES'].sum().reset_index()
 
    return {
        'data': [go.Scatter(x=monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['MONTH_ID'],
                        y=monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['SALES'],
                        text=monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['SALES'],
                        name='2003',
                        mode='markers+lines',
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Year</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['YEAR_ID'].astype(str) + '<br>'+
                        '<b>Month</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['MONTH_ID'].astype(str) + '<br>'+
                        '<b>Sales</b>: $' + [f'{x:,.0f}' for x in monthly_sales[(monthly_sales['YEAR_ID'] == 2003) & (monthly_sales['COUNTRY'] == w_countries)]['SALES']] + '<br>'
                        ),
 
              go.Scatter(x=monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['MONTH_ID'],
                        y=monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['SALES'],
                        text=monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['SALES'],
                        name='2004',
                        mode='markers+lines',
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Year</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['YEAR_ID'].astype(str) + '<br>'+
                        '<b>Month</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['MONTH_ID'].astype(str) + '<br>'+
                        '<b>Sales</b>: $' + [f'{x:,.0f}' for x in monthly_sales[(monthly_sales['YEAR_ID'] == 2004) & (monthly_sales['COUNTRY'] == w_countries)]['SALES']] + '<br>'
                        ),
 
             go.Scatter(x=monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['MONTH_ID'],
                        y=monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['SALES'],
                        text=monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['SALES'],
                        name='2005',
                        mode='markers+lines',
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Year</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['YEAR_ID'].astype(str) + '<br>'+
                        '<b>Month</b>: ' + monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['MONTH_ID'].astype(str) + '<br>'+
                        '<b>Sales</b>: $' + [f'{x:,.0f}' for x in monthly_sales[(monthly_sales['YEAR_ID'] == 2005) & (monthly_sales['COUNTRY'] == w_countries)]['SALES']] + '<br>'
                        )],
 
 
 
 
        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Monthly sales : ' + (w_countries),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
 
             hovermode='x',
 
             xaxis=dict(title='<b>Month</b>',
                        tick0=0,
                        dtick=1,
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
 
                ),
 
             yaxis=dict(title='<b>Total Sales</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
 
                ),
 
             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),
 
                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',
 
                 )
 
    }
 
# Create scatter chart (Compare sales and q. ordered)
@app.callback(Output('scatter_6', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
 
    scatter = sales1.groupby(['COUNTRY','PRODUCTLINE'])[['QUANTITYORDERED', 'SALES']].sum().reset_index()
 
    return {
        'data': [go.Scatter(x=scatter[scatter['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                        y=scatter[scatter['COUNTRY'] == w_countries]['SALES'],
                        text=scatter[scatter['COUNTRY'] == w_countries]['SALES'],
                        mode='markers',
                        hoverinfo='text',
                        hovertext=
                        '<b>Country</b>: ' + scatter[scatter['COUNTRY'] == w_countries]['COUNTRY'].astype(str) + '<br>'+
                        '<b>Product</b>: ' + scatter[scatter['COUNTRY'] == w_countries]['PRODUCTLINE'].astype(str) + '<br>'+
                        '<b>Q.Ordered</b>: ' + [f'{x:,.0f}' for x in scatter[scatter['COUNTRY'] == w_countries]['QUANTITYORDERED']] + '<br>'+
                        '<b>Sales</b>: $' + [f'{x:,.0f}' for x in scatter[scatter['COUNTRY'] == w_countries]['SALES']] + '<br>',
                            marker=dict(
                                size=20,
                                color=scatter[scatter['COUNTRY'] == w_countries]['QUANTITYORDERED'],
                                colorscale='mrybm',
                                showscale=False
 
                            )
                            )],
 
 
 
 
        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Sales of ordered quantity : ' + (w_countries),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
 
             hovermode='x',
 
             xaxis=dict(title='<b>Quantity Ordered</b>',
 
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
 
                ),
 
             yaxis=dict(title='<b>Sales</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
 
                ),
 
 
 
             )
 
    }
 
 
 
 
 
if __name__ == '__main__':
    app.run_server(debug=True)
