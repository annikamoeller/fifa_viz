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
        self.clickPlayer = None

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id),
            style={'margin': 'auto', 'width': '70%', 'padding': 20}
        )
    
    def update(self, x_axis_values=None):
        df = player_stats

        if x_axis_values is not None:
            df = df[df['team'] == x_axis_values]
        fig = px.scatter(df, x=self.feature_x, y=self.feature_y, color='team', hover_data='player')

        fig.update_layout(plot_bgcolor='#26232C',
            paper_bgcolor='#26232C',
            modebar_color = '#136d6d',
            title_font_color='white',
            legend_font_color='white',
            legend_title_font_color='white',
            xaxis = dict(
            color="#9D9D9D",
            tickfont_size=14,
            title_font=dict(size=20, color='#9D9D9D')),
            yaxis=dict(
                color="#9D9D9D",
                titlefont_size=16,
                tickfont_size=14,
                gridcolor='#9D9D9D',
                title_font=dict(size=17, color='#9D9D9D'),
            ))
        
        return fig

    def get_click_player(self):
        return self.clickPlayer
    
    def set_click_player(self, clickedPlayer):
        self.clickPlayer = clickedPlayer