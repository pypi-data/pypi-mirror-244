from dash import Dash, dcc, html, Input, Output, State, ALL
import dash_mantine_components as dmc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import random
import colorlover as cl
import numpy as np
from PIL import Image
 

# Link for Image in navbar
AMPLABS_LOGO = Image.open("assets/favicon.ico")

HTML_NAVBAR = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=AMPLABS_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("AmpLabs", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            href="https://plotly.com",
            style={"textDecoration": "none", "marginLeft": "1%"},
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavItem(dbc.NavLink("About Us", href="https://www.amplabs.ai/",target="_blank")),
                    ),
                ],
                style={"color": "white"},
            ),
            id="navbar-collapse",
            is_open=False,
            navbar=True,
            style={
                "justifyContent": "end",
                "marginRight": "5%",
            },
        ),
    ],
    color="dark",
    dark=True,
)