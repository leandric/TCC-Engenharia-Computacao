from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import *

from flask_login import current_user, logout_user
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty"])

card_style = {
    'height': '100%',
    'width': '100%',
    'margin': '10px'
}

# =========  Tratativas de Dados  =========== #
df = pd.DataFrame(np.random.randn(100, 1), columns=['dados'])
df_dia = df.to_dict()
fig = px.line(df, x=df.index, y='dados', template='minty')

# =========  Layout  =========== #


def render_layout(username):
    layout = html.Div([
        dcc.Location(id='data-url', refresh=True),
        dcc.Store(id='df_dia', data=df_dia),

        # ======== Row1 ======== #
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Projeto TCC')
                        ], sm=8),
                        dbc.Col([
                            html.Img(src='assets/logo.png')
                        ], sm=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Legend(f'Bem Vindo {username}!')
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Sair', id='logout_button')
                        ])
                    ])
                ])
            ], style={'height': '100%', 'margin-left': '10px'})
        ], lg=2),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend('Potência'),
                            dcc.Graph(id='grafico-1', figure=fig)
                        ]),
                    ], style=card_style)
                ], sm=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend('Consumo KWh'),
                            dcc.Graph(id='grafico-2', figure=fig)
                        ]),
                    ], style=card_style)
                ], sm=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend('Valor R$'),
                            dcc.Graph(id='grafico-3', figure=fig)
                        ]),
                    ], style=card_style)
                ], sm=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend('Pontêcia Diária'),
                            dcc.Graph(id='grafico-4', figure=fig)
                        ])
                    ])
                ], style=card_style, sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend('Consumo Diária'),
                            dcc.Graph(id='grafico-5', figure=fig)
                        ])
                    ])
                ], style=card_style, sm=6),
            ])

        ], lg=10)

    ], style={'display': 'flex'})
    return layout

# =========  Callbacks  =========== #


@app.callback(
    Output('data-url', 'pathname'),
    Input('logout_button', 'n_clicks'))
def successful(n_clicks):
    if n_clicks == None:
        raise PreventUpdate

    if current_user.is_authenticated:
        logout_user()
        return '/login'
    else:
        return '/login'
