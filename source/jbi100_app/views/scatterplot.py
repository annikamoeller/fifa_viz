from dash import dcc, html
import plotly.graph_objects as go
from ..config import *
import plotly.express as px
from ..common import *
import numpy as np

class Scatterplot(html.Div):
    def __init__(self, name, df, x_axis_stat, y_axis_stat):
        """
        @name (str): used for the html_id
        @feature_x (str): x-axis value that matches df column
        @feature_y (str): y-axis value that matches df column
        @df (df): main dataframe to be used
        """
        self.html_id = name.lower().replace(" ", "-")
        self.table_clicked = None
        self.plot_clicked = None
        self.highlighted_player = None
        self.team_filter = None
        self.position_filter = None
        self.x_axis_stat = x_axis_stat
        self.y_axis_stat = y_axis_stat
        self.df = df
        
        df = main_df.reset_index()
        self.initial_plot = px.scatter(df, x=x_axis_stat, y=y_axis_stat, hover_data='player', color='position')
        
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=
                dcc.Graph(id=self.html_id, figure=self.update_layout(self.initial_plot)),
            style={'margin': 'auto', 'width': '100%', 'height': 400, 'padding': 10}
        )

    def update(self, on, x_axis_stat, y_axis_stat, selected_stat, team_filter, position_filter, player):
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

        self.x_axis_stat = x_axis_stat
        self.y_axis_stat = y_axis_stat
        self.selected_stat = selected_stat
        self.team_filter = team_filter
        self.position_filter = position_filter
               
        df = filter_df(df, team_filter, position_filter)
        fig = px.scatter(df, x=x_axis_stat, y=y_axis_stat, hover_data='player', color='position')

        if player:
            self.highlight_player(fig, player)

        return self.update_layout(fig)
        
    def update_layout(self, fig):
        #Update the style and colors of the graph
        fig.update_layout(plot_bgcolor='#26232C',
            paper_bgcolor='#26232C',
            title_font_color='white',
            legend_font_color='white',
            legend_title_font_color='white',
            xaxis = dict(
                color="#9D9D9D",
                title_font=dict(size=20, color='#9D9D9D')),
            yaxis=dict(
                color="#9D9D9D",
                titlefont_size=16,
                gridcolor='#9D9D9D',
                title_font=dict(size=20, color='#9D9D9D'),
            ))
        return fig

    def highlight_player(self, fig, player):
        """
        @fig (fig): plot figure to be updated
        @player (str): player to be highlighted
        """
        traces = []
        for item in fig.select_traces():
            traces.append(item)

        for trace in traces:
            # Set default point styles.
            n = len(trace.x)
            color = [trace.marker.color] * n
            opacity = [1] * n
            size = [5] * n
            #this gets a numpy array with the player idx
            idx = np.where(trace.customdata == player)[0] 
            
            if idx.size != 0: #check if we found a player
                
                idx = idx[0] #get the actual int

                if idx == 0:
                    #if the selected player is at idx 0, we have to switch it to a dif position
                    #this is because pyplot sets the legend color based on the first idx of the trace
                    #hence, changing the color of idx=0 also changes the label color
                    x = trace.x
                    y = trace.y
                    player_name = trace.customdata

                    x[0], x[1] = x[0], x[1]
                    y[0], y[1] = y[0], y[1]

                    selected = player_name[0]
                    switch = player_name[1]
                    player_name[1] = selected
                    player_name[0] = switch

                    idx = 1

                self.highlighted_player = player
                color[idx] = "yellow"
                size[idx] = 15
                # Update trace.
                trace.marker.color = color
                trace.marker.size = size
                trace.marker.line.color = color
                trace.marker.opacity = opacity

    def get_click_player(self):
        return self.table_clicked, self.plot_clicked
    
    def set_click_player(self, table_clicked, plot_clicked):
        self.table_clicked = table_clicked
        self.plot_clicked = plot_clicked

    def get_hilghlighted_player(self):
        self.highlighted_player

    def get_initial_plot(self):
        return self.initial_plot
    
    def get_df(self):
        return self.df