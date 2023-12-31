from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
from ..common import *

class Scatterplot(html.Div):
    def __init__(self, name, df):
        """
        @name (str): used for the html_id
        @feature_x (str): x-axis value that matches df column
        @feature_y (str): y-axis value that matches df column
        @df (df): main dataframe to be used
        """
        self.html_id = name.lower().replace(" ", "-")
        self.clickPlayer = None
        self.df = df

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id),
            style={'margin': 'auto', 'width': '100%', 'height': 400, 'padding': 10}
        )

    def update(self, on, x_axis_stat, y_axis_stat, team_filter, position_filter):
        """
        @on (str): whether or not goalkeeper mode is on
        @x_axis_stat (str): statistic chosen for x-axis 
        @y_axis_stat (str): statistic chosen for y-axis
        @team_filter (str): team to filter results by
        @position_filter (str): playing position to filter by
        @returns ->>> figure class with new plot
        """
        if on: df = gk_df.reset_index()
        else: df = main_df.reset_index()

        df = filter_df(df, team_filter, position_filter)
        fig = px.scatter(df, x=x_axis_stat, y=y_axis_stat, hover_data='player', color='position')

        return self.update_layout(fig)
        
    def update_layout(self, fig):
        #Update the style and colors of the graph
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

    #Not needed or used for now
    def get_click_player(self):
        return self.clickPlayer
    
    #Not needed or used for now
    def set_click_player(self, clickedPlayer):
        self.clickPlayer = clickedPlayer