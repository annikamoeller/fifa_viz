from jbi100_app.main import app
from jbi100_app.views.menu import *
from jbi100_app.views.field import *
from jbi100_app.config import *
from jbi100_app.views.dropdown import *
from jbi100_app.views.radar import *
from jbi100_app.views.scatterplot import *
from jbi100_app.views.switch import *
from jbi100_app.views.heatmap import *

from jbi100_app.views.multival_dropdown import *
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from PIL import Image
import dash_daq as daq

if __name__ == '__main__':

    """ 
    This is the main layout of the webpage, its children are then sub divided
    into further html layouts 
    """
    #teams_for_dropdown = [team for team in teams_list]
    gk_switch = Switch("gk_switch")

    scatter_vals = list(total_player_df_no_gk.columns)

    scatter_plot = Scatterplot("scatterplot", total_player_df_no_gk)
    radar_plot = Radar("radar", total_player_df_no_gk)
    x_axis_dropdown = Dropdown("x_axis_dropdown", scatter_vals, scatter_vals[0], 'X-Axis Values')
    y_axis_dropdown = Dropdown("y_axis_dropdown", scatter_vals, scatter_vals[0], 'Y-Axis Values')

    #teams_dropdown = Dropdown("teams_dropdown", teams_for_dropdown, teams_for_dropdown[0], 'Team')
    positions_dropdown = Dropdown("positions_dropdown", ['Goalkeeper', 'Defender', 'Midfilder', 'Striker'], 'Defender', 'Stat')
    attribute_dropdown = MultiValDropdown("attribute_dropdown", ['A', 'B', 'C'], None, 'Attributes')

    heatmap_plot = Heatmap("heatmap_plot", total_player_df_no_gk)

    left_menu_plots = [gk_switch, x_axis_dropdown, y_axis_dropdown, scatter_plot, attribute_dropdown, heatmap_plot]
    right_menu_plots = [positions_dropdown, radar_plot]

    #Create left and right side of the page
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="one-half column",#base.css style
                children=left_menu_plots #plots
            ),

            # Right column
            html.Div(
                id="right-column",
                className="one-half column", #base.css style
                children=right_menu_plots #plots
            ),
        ],
    )

    """
    @app.callback(output=x, input=y) 
    A callback updates a field of a html.div element based on input and output values

    Input and output take the id of the html.div and the field to update, e.g. value,
    children, options, etc..

    We then define a function that takes as input variables based on @app.callback input var
    and returns the output var. 
    """

    """
        Here we update the element children (note that children is a dcc.Graph 
        variable and as such it is returned the same way in order to update the scatter plot)
        of the html.Div scatter-plot defined in menu.py
        and we take as input the field value of the html.Div select-team
        in this case, the drop-down menu value
    """

    @app.callback(
        Output(x_axis_dropdown.html_id, 'options'),
        Output(x_axis_dropdown.html_id, 'value'),
        Output(y_axis_dropdown.html_id, 'options'),
        Output(y_axis_dropdown.html_id, 'value'),
        Input(gk_switch.html_id, 'on')
    )
    def toggle_gk_mode(on):
        x_options, x_value = x_axis_dropdown.update(on)
        y_options, y_value = y_axis_dropdown.update(on)
        return x_options, x_value, y_options, y_value
    
    # update the scatter plot based on the x and y drop downs
    @app.callback(
        Output(scatter_plot.html_id, 'figure'),
        Input(gk_switch.html_id, 'on'),
        Input(x_axis_dropdown.html_id, "value"),
        Input(y_axis_dropdown.html_id, "value")
    )
    def selected_x_y_labels(on, x_label, y_label):
        """
        Return a figure with a teams plot based on team dropdown value 
        """
        return scatter_plot.update(on, x_label, y_label)
    
    
    # update the radar plot based on click and hover data
    @app.callback(
    Output(radar_plot.html_id, 'figure'),
    Input(scatter_plot.html_id, 'clickData'),
    Input(scatter_plot.html_id, 'hoverData'),
    Input(positions_dropdown.html_id, 'value'),
    )
    def selected_player(click, hover, selected_stat):
        """
        Get clicked, hovered player and stats dropdown value 
        return a radar figure with the stats of the selected players and dropdown
        """
        newPlayerClicked = False
        
        if click: clickedPlayer = click['points'][0]['customdata'][0] #get click data
        else: clickedPlayer = None

        #Keeping track of the clicked and previously clicked player. May be needed in the future
        if clickedPlayer != scatter_plot.get_click_player():
                previouslyClickedPlayer = scatter_plot.get_click_player()
                scatter_plot.set_click_player(clickedPlayer) 
                newPlayerClicked = True

        if hover: hoveredPlayer = hover['points'][0]['customdata'][0] #get hover data
        else: hoveredPlayer = None
        
        return radar_plot.update(clickedPlayer, hoveredPlayer, selected_stat)

    @app.callback(
        Output(attribute_dropdown.html_id, 'options'),
        Input(positions_dropdown.html_id, 'value')
    )
    def update_heatmap_attribute_options(selected_stat):
        """
        Get stats dropdown value 
        return list of attributes to be shown as options in attribute dropdown
        """
        return attribute_dropdown.update(selected_stat)

    @app.callback(
        Output(heatmap_plot.html_id, 'figure'),
        Input(scatter_plot.html_id, 'selectedData'),
        Input(attribute_dropdown.html_id, 'value'),
        Input(positions_dropdown.html_id, 'value')
    )
    def update_heatmap_players(selected_player, selected_attribute, selected_stat):
        """
        Get stats dropdown value, selected attributes, selected players
        return updates heatmap
        """
        if selected_player: 
            player_names = [player['customdata'][0] for player in selected_player['points']]
        else: player_names = []
        return heatmap_plot.update(player_names, selected_attribute, selected_stat)

    app.run_server(debug=True, dev_tools_ui=True)