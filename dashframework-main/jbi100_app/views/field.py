from dash import dcc, html
import plotly.graph_objects as go
import pitchly
from pitchly.pitch import Pitch

class Field(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="field",
            children=[html.H6(name)
            ]
        )

    def update(self):
        self.fig = Pitch()

        return self.fig
