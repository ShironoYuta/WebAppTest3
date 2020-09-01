import dash  
import dash_core_components as dcc   
import dash_html_components as html
import plotly.graph_objs as go  
import pandas as pd 
from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
import csv
import time
import definition


app = dash.Dash(__name__)

# ②表示作成
app.layout = html.Div(children=[
    html.Div(
        html.H1('電力調達シミュレータ',
        style = {'textAlign': 'center'})
    ),
    dcc.Dropdown(
        id = 'demand_drop',
        options = [
                       {"label": "月間電力需要(2019)", "value":"DemandMonth2019"},
                       {"label": "月間電力需要(仮想シナリオ)", "value":"DemandMonthSce"},
                       {"label": "日次電力需要(2019)", "value":"DemandDay2019"},
                       {"label": "日次電力需要(仮想シナリオ)", "value":"DemandDaySce"},
                ],
        value = 'DemandMonth2019'
    ),
    dcc.Input(id='month', value=1, type='text'),
    dcc.Input(id='day', value=1, type='text'),
    dcc.Graph(
        id="DemandGraph",
    )
])

# ③コールバック作成
@app.callback(
    dash.dependencies.Output('DemandGraph', 'figure'),
    [
        dash.dependencies.Input("demand_drop", "value"),
        dash.dependencies.Input("month", "value"),
        dash.dependencies.Input("day", "value"),
    ],
)
def update_graph(demand_drop,month,day):

    if demand_drop ==  "DemandMonth2019":
        Days,TraceAct,TraceFore = definition.OutputMonthlyDemand_1(month)
        return {
            'data': [go.Scatter(x = Days,y = TraceFore,name='予測値'),
                    go.Scatter(x = Days,y = TraceAct,name='2019年実績値'),
                    ]
        }
    elif demand_drop ==  "DemandMonthSce":
        Days,Trace1,Trace2,Trace3,Trace4,TraceFore = definition.OutputMonthlyDemand(month)
        return {
            'data': [go.Scatter(x = Days,y = TraceFore,name='予測値'),
                    go.Scatter(x = Days,y = Trace1,name='シナリオ1'),
                    go.Scatter(x = Days,y = Trace2,name='シナリオ2'),
                    go.Scatter(x = Days,y = Trace3,name='シナリオ3'),
                    go.Scatter(x = Days,y = Trace4,name='シナリオ4'),
                    ]
        }
    if demand_drop ==  "DemandDay2019":
        Hours,TraceAct,TraceFore = definition.OutputDailyDemand_1(month,day)
        return {
            'data': [go.Scatter(x = Hours,y = TraceFore,name='予測値'),
                    go.Scatter(x = Hours,y = TraceAct,name='2019年実績値'),
                    ]
        }
    elif demand_drop ==  "DemandDaySce":
        Hours,Trace1,Trace2,Trace3,Trace4,TraceFore = definition.OutputDailyDemand(month,day)
        return {
            'data': [go.Scatter(x = Hours,y = TraceFore,name='予測値'),
                    go.Scatter(x = Hours,y = Trace1,name='シナリオ1'),
                    go.Scatter(x = Hours,y = Trace2,name='シナリオ2'),
                    go.Scatter(x = Hours,y = Trace3,name='シナリオ3'),
                    go.Scatter(x = Hours,y = Trace4,name='シナリオ4'),
                    ]
        }

if __name__ == '__main__':
    app.run_server(debug=True)