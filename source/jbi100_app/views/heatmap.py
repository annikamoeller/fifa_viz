import pandas as pd
from ..config import *
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px

class Heatmap(html.Div):
    def __init__(self, name, df):
        """
        @name (str): used for the html_id
        @df (df): main dataframe to be used
        """
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id),
            style={'margin': 'auto', 'width': '70%','text-align': 'center', 'padding': 20}
        )
    

    def update(self, attribute=None):
        """ 
        @attribute List(str): The selected attributes dropdown.
        """
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=[[1, 20, 30],
               [20, 1, 60],
               [30, 60, 1]]))
 

        # #Set the color scheme for the plot
        # fig = self.set_fig_style(fig)

        return fig