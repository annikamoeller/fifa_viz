from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
import dash_daq as daq

class Switch(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="switch",
            children=
                daq.BooleanSwitch(id="gk_switch", on=False, color="blue", label="Goalkeeper mode")
        )