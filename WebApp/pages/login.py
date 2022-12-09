from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import *

import numpy as np
from werkzeug.security import check_password_hash
from flask_login import login_user
import plotly.express as px

# Parametros de CSS para os Cards
card_style= {
    'width':'300px',
    'min-height':'300px',
    'padding-top':'25px',
    'padding-right':'25px',
    'padding-left':'25px',
    'align-self':'center',
}

def render_layout(message):
    message = "Usuário ou senha incorreta." if message =='error' else message
    login = html.Div([
        dbc.Card([
        html.Img(src='assets/logo.png', style={'width':'20%', 'align-self':'center'}),
        html.Legend("Login", style={'color':'black', 'margin-bottom':'10px', 'text-align':'center', 'margin-top':'10px'}),
        dcc.Input(id='user_login', placeholder='Usuário', type='text'),
        dcc.Input(id='user_pwd', placeholder='Senha', type='password'),
        dbc.Button('Entrar', id='login_button', style={'margin-top':'5px'}),
        html.Span(message, style={'text-align':'center', 'color':'red', 'padding':'5px'}),
        html.Div([
            html.Label('Ou', style={'margin-right':'5px'}),
            dcc.Link('Registre-se', href='/register', style={'margin-bottom':'10px'})
        ], style={'padding':'10px', 'justify-content':'center','display':'flex'})
    ], style=card_style)
    ], style={'height':'100vh','display':'flex', 'justify-content':'center'})
    return login

    # =========  Callbacks  =========== #
@app.callback(
    Output('login-state','data'),
    Input('login_button', 'n_clicks'),
    [
        State('user_login', 'value'),
        State('user_pwd', 'value')
    ])
def sucessful(n_clicks, username, password):
    if n_clicks == None:
        raise PreventUpdate

    user = Users.query.filter_by(username=username).first()
    if user and password is not None:
        if check_password_hash(user.password, password):
            login_user(user)
            return 'success'
        else:
            return 'error'
    else:
        return 'error'
    