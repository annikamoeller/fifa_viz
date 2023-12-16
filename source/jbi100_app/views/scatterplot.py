from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px

class Scatterplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id),
        )
    
    def update(x_axis_values=None):

        df = player_stats
        
        if x_axis_values is not None:
            df = df[df['team'] == x_axis_values]

        fig = px.scatter(df, x='birth_year', y='average_shot_distance', color='team')

        return fig
