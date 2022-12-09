from dash import html, dcc
from dash.dependencies import Input, State, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash
from flask_login import current_user

from app import *
from pages import login, register, dashb


# Configuração do user
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# =========  Layout  =========== #
app.layout =  html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Location(id='base-url', refresh=False),
            dcc.Store(id='login-state', data=""),
            dcc.Store(id='register-state', data=""),
            html.Div(id='page-content', style={'height':'100vh'})
        ])
    ])
], style={'margin':'0px','padding':'0px'})

# =========  Callbacks  =========== #
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.callback(
    Output("base-url", "pathname"),
    [Input("login-state", "data"),
    Input("register-state", "data")])
def render_page_content(login_state, register_state):
    #print(dash.callback_context.triggered)
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigg_id == 'login-state' and login_state == 'success':
            return '/data'
        if trigg_id == 'login-state' and login_state == 'error':
            return '/login'

        if trigg_id == 'register-state':
            if register_state == "":
                return '/login'
            else:
                return '/register'
    return '/'

@app.callback(
    Output("page-content", "children"),
    Input("base-url", "pathname"),
    [State("login-state", "data"), State("register-state", "data")])
def render_page_content(pathname, login_state, register_state):
    """Função responsavel pelas trocas de teles

    Args:
        pathname (_type_): _description_

    Returns:
        _type_: _description_
    """
    if(pathname == "/login" or pathname =="/"):
        return login.render_layout(login_state)                #Função que renderizar a rela de login

    if(pathname == "/register"):
        return register.render_layout(register_state)

    if pathname == '/data':
        if current_user.is_authenticated:
            return dashb.render_layout(current_user.username)
        else:
            return login.render_layout(login_state)

if __name__ == "__main__":
    app.run_server(host='0.0.0.0',port=8051, debug=True)