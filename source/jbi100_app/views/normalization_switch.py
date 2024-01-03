from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
import dash_daq as daq

class NormalizationSwitch(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="switch",
            children=
                daq.BooleanSwitch(id="normalization_switch", on=False, color="blue", label="Normalize locally")
        )