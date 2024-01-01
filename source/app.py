from jbi100_app.main import app
from jbi100_app.views.menu import *
from jbi100_app.views.field import *
from jbi100_app.config import *
from jbi100_app.views.dropdown import *
from jbi100_app.views.radar import *
from jbi100_app.views.scatterplot import *
from jbi100_app.views.switch import *
from jbi100_app.views.heatmap import *
from jbi100_app.views.infoCard import *
from jbi100_app.views.table import *

from jbi100_app.views.multival_dropdown import *
from dash import html
from dash.dependencies import Input, Output

if __name__ == '__main__':

    """ 
    This is the main layout of the webpage, its children are then sub divided
    into further html layouts 
    """
    # goalkeeper mode switch
    gk_switch = Switch("gk_switch")

    # Table elements 
    player_data_table = Table("player_data_table", main_df, 'birth_year')
    similar_player_table = Table("similar_player_table", None, 'birth_year')
    # drop downs 
    table_stat_dropdown = Dropdown("stat_dd", player_stats, player_stats[0], 'Select statistic')
    filter_position_dropdown = Dropdown("position_dd", ['FW', 'MF', 'DF', 'GK'], None, 'Filter by position', multiple_values=True)
    filter_team_dropdown = Dropdown("team_dd", teams_list, None, 'Filter by team', multiple_values=True)
    # group dropdowns together horizontally
    table_dropdowns = html.Div([table_stat_dropdown, filter_position_dropdown, filter_team_dropdown], style={'display': 'flex', 'flexDirection': 'row'})

    # Scatter plot
    scatter_plot = Scatterplot("scatterplot", main_df)
    
    # drop downs for scatter plot 
    x_axis_dropdown = Dropdown("x_axis_dropdown", player_stats, startingValue=player_stats[0], label='X-Axis Values')
    y_axis_dropdown = Dropdown("y_axis_dropdown", player_stats, startingValue=player_stats[1], label='Y-Axis Values')
    # group dropdowns together horizontally
    scatter_dropdowns = html.Div([x_axis_dropdown, y_axis_dropdown], style={'display': 'flex', 'flexDirection': 'row'})

    # Radar plot
    radar_plot = Radar("radar", main_df)

    # player 1 info card
    info_card1 = InfoCard("infocard1")

    # player 2 info card
    #info_card2 = InfoCard("infocard2")

    # radar and info card grouping 
    radar_and_info = html.Div([radar_plot, info_card1], style={'display': 'flex', 'flexDirection': 'row'})

    # Heatmap plot
    heatmap_plot = Heatmap("heatmap_plot", main_df)

    # Set up page on left and right
    left_menu_plots = [gk_switch, table_dropdowns, player_data_table, scatter_dropdowns, scatter_plot]
    right_menu_plots = [radar_plot, info_card1, similar_player_table, heatmap_plot]

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
                className="one-half column", #base.css 
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
    # toggle goalkeeper mode 
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
        Input(y_axis_dropdown.html_id, "value"),
        Input(filter_team_dropdown.html_id, 'value'),
        Input(filter_position_dropdown.html_id, 'value')
    )
    def update_scatter(on, x_label, y_label, team_filter, position_filter):
        """
        Return a figure with a teams plot based on team dropdown value 
        """
        return scatter_plot.update(on, x_label, y_label, team_filter, position_filter)
    
    # update the table based on the drop downs
    @app.callback(
            Output(player_data_table.html_id, 'data'),
            Output(player_data_table.html_id, 'columns'),
            Input(table_stat_dropdown.html_id, 'value'),
            Input(filter_team_dropdown.html_id, 'value'),
            Input(filter_position_dropdown.html_id, 'value')
    )
    def update_table(selected_stat, team, position):
        new_data, new_cols = player_data_table.update(selected_stat, team, position)
        return new_data, new_cols
    
    style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgb(204, 230, 255)",
        "border": "1px green",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgb(204, 230, 255)",
        "border": "1px green",
    },
]
    
    # Callback to update the style of the selected row
    @app.callback(
        Output(player_data_table.html_id, 'style_data_conditional'),
        Input(player_data_table.html_id, 'active_cell')
    )
    def update_selected_row_color(active):
        style = style_data_conditional.copy()
        if active:
            style.append(
                {
                    "if": {"row_index": active["row"]},
                    "backgroundColor": "rgb(204, 230, 255)",
                    "border": "1px green",
                },
            )
        return style
         
    #update the similar player table and heatmap
    @app.callback(
            Output(similar_player_table.html_id, 'data'),
            Output(similar_player_table.html_id, 'columns'),
            Output(heatmap_plot.html_id, 'figure'),
            Input(player_data_table.html_id, 'data'),
            Input(player_data_table.html_id, 'active_cell'),
            Input(player_data_table.html_id, 'columns')
    )
    def update_similar_players(data, clicked_cell, columns):
        player = data[clicked_cell['row']]['player']
        if player:
            new_data, columns = similar_player_table.get_similar_players(player)
            similar_players = similar_player_table.get_5_similar_players_df()
            new_heatmap = heatmap_plot.update(player, similar_players)
        return new_data, columns, new_heatmap
    
    # update the radar plot based on click and hover data
    @app.callback(
    Output(radar_plot.html_id, 'figure'),
    Input(scatter_plot.html_id, 'clickData'),
    Input(scatter_plot.html_id, 'hoverData')
    )
    def selected_player(click, hover):
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
        
        return radar_plot.update(clickedPlayer, hoveredPlayer)

    # update info card to display basic player info when clicked on in scatter plot 
    @app.callback(
        Output(info_card1.html_id, 'value'),
        Input(scatter_plot.html_id, 'clickData')
    )
    def info_card(click):
        if click: clickedPlayer = click['points'][0]['customdata'][0] #get click data
        else: clickedPlayer = None
        return info_card1.update(clickedPlayer)
    
    app.run_server(debug=True, dev_tools_ui=True)