# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 09:03:38 2022

@author: Josa - josageof@gmail.com
"""

# import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# from datetime import datetime


# from config import processed_storage_file
from trello_data_process import processTrelloData
from utils.plotly_graph import plotGraph1, plotGraph2, plotGraph3, plotGraph4


# Inicia o app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# ==== define as funções de layout

def drawFigure1(df_year):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=plotGraph1(df_year)
                )
            ])
        ),
    ])


def drawFigure2(df_month):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=plotGraph2(df_month)
                )
            ])
        ),
    ])


def drawFigure3(df_week_member):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=plotGraph3(df_week_member)
                )
            ])
        ),
    ])


def drawFigure4(df_task_type):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=plotGraph4(df_task_type)
                )
            ])
        ),
    ])

# Text field


def drawTextField(task_type, task_type_value):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(f"{task_type}"),
                    html.H2(f": {task_type_value}"),
                ], style={
                    "padding-top": "5px",
                    # 'textAlign': 'center',
                    'background-color': '#111111',
                    'color': '#FFFFFF',
                    'height': 70,
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                })
            ])
        ),
    ])

# byCubes logo


def drawLogo():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Img(
                        src="assets/trelloLogo.png",
                        height="80px",
                        style={"margin-top": "5px", "margin-bottom": "5px"}
                    ),
                ], style={
                    'background-color': '#111111',
                    'color': '#FFFFFF',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'font-weight': 'bold'})
            ])
        ),
    ])


# Trello logo


def bycubesLogo():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Img(
                        src="assets/bycubes_152x152.png",
                        height="80px",
                        style={"margin-top": "0px", "margin-bottom": "0px"}
                    ),
                ], style={
                    'background-color': '#111111',
                    'color': '#FFFFFF',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'font-weight': 'bold'})
            ])
        ),
    ])


# Text title


def drawTitle():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    # html.H1("bycubes :: Resumo do Trello"),
                    html.H1("bycubes :: trellodash :: My Trello Summary"),
                ], style={
                    "padding-top": "15px",
                    "padding-bottom": "10px",
                    "padding-left": "20px",
                    'background-color': '#111111',
                    'color': '#FFFFFF',
                    # 'height': 70,
                    'display': 'flex',
                    # 'align-items': 'center',
                    'justify-content': 'center',
                    'font-weight': 'bold'})
            ])
        ),
    ])


@app.callback(Output('output', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_output(n):

    # data = pd.read_pickle(processed_storage_file)
    data = processTrelloData()
    
    # # print('Análise ocorrida: {}'.format(datetime.now()))

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        bycubesLogo()
                    ], width=1),
                    dbc.Col([
                        drawTitle()
                    ], width=10, align='center'),
                    dbc.Col([
                        drawLogo()
                    ], width=1),
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        drawTextField("To do", data['todo'])
                    ], width=4),
                    dbc.Col([
                        drawTextField("Doing", data['doing'])
                    ], width=4),
                    dbc.Col([
                        drawTextField("Done", data['done'])
                    ], width=4),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        drawFigure2(data['df_month'])
                    ], width=6),
                    dbc.Col([
                        drawFigure3(data['df_week_member'])
                    ], width=6),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        drawFigure1(data['df_year'])
                    ], width=8),
                    dbc.Col([
                        drawFigure4(data['df_task_type'])
                    ], width=4),
                ], align='center'),
            ]), color='dark'
        )
    ])


app.layout = html.Div([
    html.Div(id='output'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # atualiza a cada minuto
        n_intervals=0
    )])


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
