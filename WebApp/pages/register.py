from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash

import numpy as np

from app import *

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
    """Função responsavel por redenrizar a pagina de registro
    Returns:
        Vanilla HTML components for Dash: layout
    """
    message = "Ocorreu um error durente o registro." if message =='error' else message
    layout = html.Div([
        dbc.Card([
        html.Legend("Registrar"),
        dcc.Input(id='user_register', placeholder='Usuário', type='text'),
        dcc.Input(id='email_register', placeholder='Email', type='text'),
        dcc.Input(id='pwd_register', placeholder='Senha', type='password'),
        dbc.Button('Enviar', id='register_button'),
        html.Span(message, style={'text-align':'center', 'color':'red'}),
        html.Div([
            html.Label('Ou', style={'margin-right':'5px'}),
            dcc.Link('Faça Login', href='/login')
        ], style={'padding':'10px', 'justify-content':'center','display':'flex'})
    ], style=card_style)
    ], style={'height':'100vh','display':'flex', 'justify-content':'center'})
    return layout


# =========  Callbacks  =========== #
@app.callback(
    Output('register-state', 'data'),
    Input('register_button', 'n_clicks'),
    [State('user_register', 'value'),
    State('pwd_register', 'value'),
    State('email_register', 'value')])
def register(n_clicks, username, password, email):
    if n_clicks == None:
        raise PreventUpdate

    if username is not None and password is not None and email is not None:
        hashed_password = generate_password_hash(password=password, method='sha256', salt_length=256)
        ins = Users_table.insert().values(username=username, password=hashed_password, email=email)
        conn =engine.connect()
        conn.execute(ins)
        conn.close()
        return ''
    else:
        return 'error'
