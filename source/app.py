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
from jbi100_app.views.normalization_switch import *

from jbi100_app.views.multival_dropdown import *
from dash import html
from dash.dependencies import Input, Output
import json

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
    filter_position_dropdown = Dropdown("position_dd", ['FW', 'MF', 'DF'], None, 'Filter by position', multiple_values=True)
    filter_team_dropdown = Dropdown("team_dd", teams_list, None, 'Filter by team', multiple_values=True)
    # group dropdowns together horizontally
    table_dropdowns = html.Div([table_stat_dropdown, filter_position_dropdown, filter_team_dropdown], style={'display': 'flex', 'flexDirection': 'row'})

        #Reset button
    reset_button = html.Div(html.Button(children='Reset', 
                                        id='reset_button', 
                                        n_clicks=0,
                                        style={'backgroundColor': 'white'}), 
                                        style={'text-align': 'center',
                                               'padding-bottom': '3rem'} )

    # Scatter plot
    scatter_plot = Scatterplot("scatterplot", main_df, 'goals', 'goals')
    
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
    normalization_switch = NormalizationSwitch('normalization_switch')
    heatmap_plot = Heatmap("heatmap_plot", df_hm)

    #this variable is used for many callbacks and it represents the highlighted player
    #when saving data in it, it must be serialized by using json.dumps(data)
    #when reading, we must decode by using json.loads(data)
    store = dcc.Store(id='highlighted-player-value')

    # Set up page on left and right
    left_menu_plots = [gk_switch, table_dropdowns, player_data_table, reset_button, scatter_dropdowns, scatter_plot]
    right_menu_plots = [radar_plot, info_card1, normalization_switch, heatmap_plot, store]

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
        Output(filter_position_dropdown.html_id, 'options'),
        Output(filter_position_dropdown.html_id, 'value'),
        Output(table_stat_dropdown.html_id, 'options'),
        Output(table_stat_dropdown.html_id, 'value'),
        Input(gk_switch.html_id, 'on')
    )
    def toggle_gk_mode(on):
        x_options, x_value = x_axis_dropdown.update(on)
        y_options, y_value = y_axis_dropdown.update(on)
        filter_options, filter_value = filter_position_dropdown.update(on)
        table_stat_options, table_stat_value = table_stat_dropdown.update(on)
        return x_options, x_value, y_options, y_value, filter_options, filter_value, table_stat_options, table_stat_value
    
    # update the scatter plot based on the x and y drop downs
    @app.callback(
        Output(scatter_plot.html_id, 'figure'),
        Output('highlighted-player-value', 'data'),
        Output(player_data_table.html_id, 'style_data_conditional'),
        Output(player_data_table.html_id, 'active_cell'),
        Input(gk_switch.html_id, 'on'),
        Input(scatter_plot.html_id, 'clickData'),
        Input(x_axis_dropdown.html_id, "value"),
        Input(y_axis_dropdown.html_id, "value"),
        Input(table_stat_dropdown.html_id, 'value'),
        Input(filter_team_dropdown.html_id, 'value'),
        Input(filter_position_dropdown.html_id, 'value'),
        Input(player_data_table.html_id, 'data'),
        Input(player_data_table.html_id, 'active_cell')
                )
    def update_scatter(on, click, x_label, y_label, selected_stat, team_filter, position_filter, clicked_table_player_data, clicked_cell):
        """
        Return a figure with a teams plot based on team dropdown value 
        """
        player = None
        blue_highlight_style = [
        {
            
            "if": {"state": "selected"},
            "backgroundColor": "rgb(204, 230, 255)",
            "line_color": "1px black",
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "rgb(204, 230, 255)",
            "line_color": "1px black"
        }
        ]

        white_highlight_style = [
        {
            "if": {"state": "selected"},
            "backgroundColor": "#ebebeb",
            "line_color": "1px black"
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "#ebebeb",
            "line_color": "1px black"
        }
        ]

        style = blue_highlight_style.copy()
        if clicked_cell: 
            style.append(
                {
                    "if": {"row_index": clicked_cell["row"]},
                    "backgroundColor": "rgb(204, 230, 255)",
                    "line_color": "1px black"
                },
            )

        #get the last clicked scatter and table clicked player 
        if clicked_table_player_data and clicked_cell: 
            table_player = clicked_table_player_data[clicked_cell['row']]['player']
        else: table_player = None
        
        if click: scatter_player = click['points'][0]['customdata'][0] #get click data
        else: scatter_player = None
        #get the previously clicked players
        prev_table_click, prev_scatter_click = scatter_plot.get_click_player()
        #if the players are not the same and a new value is clicked, set it
        if table_player != scatter_player:
            if prev_table_click != table_player: player = table_player

            elif prev_scatter_click != scatter_player: 
                player = scatter_player
                style = white_highlight_style.copy()
                if clicked_cell: 
                    style.append(
                        {
                            "if": {"row_index": clicked_cell["row"]},
                            "backgroundColor": "#ebebeb",
                            "line_color": "1px black"
                        },
                    )
            #if we change labels or filters we persist the table click value,
            #otherwise, we set the clicked players in scatter_plot
            if x_label != scatter_plot.x_axis_stat \
                                or y_label != scatter_plot.y_axis_stat  \
                                or team_filter != scatter_plot.team_filter \
                                or position_filter != scatter_plot.position_filter:

                    player = table_player
                    scatter_plot.set_click_player(table_player, None)
                    style = white_highlight_style.copy()
                    style.append(
                        {
                            "if": {"row_index": clicked_cell["row"]},
                            "backgroundColor": "#ebebeb",
                            "line_color": "1px black"
                        },
                    )
    
            else: 
                scatter_plot.set_click_player(table_player, scatter_player)
        else: 
            player = scatter_player
        return scatter_plot.update(on, x_label, y_label, selected_stat, team_filter, position_filter, player), json.dumps(player), style, clicked_cell
    
    # update the table based on the drop downs
    @app.callback(
            Output(player_data_table.html_id, 'data'),
            Output(player_data_table.html_id, 'columns'),
            Input(table_stat_dropdown.html_id, 'value'),
            Input(filter_team_dropdown.html_id, 'value'),
            Input(filter_position_dropdown.html_id, 'value'),
            Input(gk_switch.html_id, 'on')
    )
    def update_table(selected_stat, team, position, on):
        new_data, new_cols = player_data_table.update(selected_stat, on, team, position)
        return new_data, new_cols
    
    # reset the selected cells
    @app.callback(
            Output(player_data_table.html_id, 'active_cell', allow_duplicate=True),
            Output(player_data_table.html_id, 'selected_cells', allow_duplicate=True),
            Input('reset_button', 'n_clicks'),
            prevent_initial_call=True
    )
    def reset_table(n_clicks):
        if n_clicks not in [0, None]:
            return None, []
    
    # Callback to update the style of the selected row
    # @app.callback(
    #     Output(player_data_table.html_id, 'style_data_conditional'),
    #     Input(player_data_table.html_id, 'active_cell'),
    #     Input('highlighted-player-value', 'data')
    # )
    # def update_selected_row_color(active, highlight_player):

    #     style_data_conditional = [
    #         {
    #             "if": {"state": "active"},
    #             "backgroundColor": "rgb(204, 230, 255)",
    #             "border": "1px green",
    #         },
    #         {
    #             "if": {"state": "selected"},
    #             "backgroundColor": "rgb(204, 230, 255)",
    #             "border": "1px green",
    #         },
    #     ]

    #     style = style_data_conditional.copy()
    #     if active:
    #         style.append(
    #             {
    #                 "if": {"row_index": active["row"]},
    #                 "backgroundColor": "rgb(204, 230, 255)",
    #                 "border": "1px green",
    #             },
    #         )
    #     return style
         
    #update the similar player table and heatmap
    @app.callback(
            # Output(similar_player_table.html_id, 'data'),
            # Output(similar_player_table.html_id, 'columns'),
            Output(heatmap_plot.html_id, 'figure'),
            Input(gk_switch.html_id, 'on'),
            Input(player_data_table.html_id, 'data'),
            Input(player_data_table.html_id, 'active_cell'),
            Input(player_data_table.html_id, 'columns'),
            Input(normalization_switch.html_id, 'on'),
            Input('highlighted-player-value', 'data'),
            Input(scatter_plot.html_id, 'selectedData')
    )
    def update_similar_players(goalkeeper_mode, data, clicked_cell, columns, local_normalization, highlight_player_data, selected_players_in_scatter_plot):
        # Function partly broken, only updates heatmap when no players are selected in the scatterplot.
        player = json.loads(highlight_player_data)

        # if selected_players:
        #     print('Players Selected')
        #     players = [player['customdata'][0] for player in selected_players['points']]
        #     new_heatmap = heatmap_plot.update(players, None, local_normalization)

        new_data = []
        columns = []
        new_heatmap = heatmap_plot.initial_heatmap(goalkeeper_mode=goalkeeper_mode)

        if player:
            new_data, columns = similar_player_table.get_similar_players(goalkeeper_mode, player)
            similar_players = similar_player_table.get_5_similar_players_df()
            similar_player_names = similar_players.index.tolist()
            new_heatmap = heatmap_plot.update(goalkeeper_mode, similar_player_names, local_normalization)
        
        try:
            selected_names_in_scatter_plot = [player['customdata'][0] for player in selected_players_in_scatter_plot['points']]
            if not selected_names_in_scatter_plot:
                pass
            else:
                new_heatmap = heatmap_plot.update(selected_names_in_scatter_plot, local_normalization)
        except: 
            pass

        #return new_data, columns, new_heatmap
        return new_heatmap
    
    # update the radar plot based on click and hover data
    @app.callback(
    Output(radar_plot.html_id, 'figure'),
    Input(scatter_plot.html_id, 'hoverData'),
    Input('highlighted-player-value', 'data'),
    Input(gk_switch.html_id, 'on')
    )
    def selected_player(hover, highlight_player_data, on):
        """
        Get clicked, hovered player and stats dropdown value 
        return a radar figure with the stats of the selected players and dropdown
        """
        highlight_player_data = json.loads(highlight_player_data)

        if hover: hoveredPlayer = hover['points'][0]['customdata'][0] #get hover data
        else: hoveredPlayer = None

        return radar_plot.update(on, highlight_player_data, hoveredPlayer)

    # update info card to display basic player info when clicked on in scatter plot 
    @app.callback(
        Output(info_card1.html_id, 'value'),
        Input('highlighted-player-value', 'data')
    )
    def info_card(highlight_player_data):
        highlight_player_data = json.loads(highlight_player_data)
        if highlight_player_data:
            return info_card1.update(highlight_player_data)
        else: return "" #empty infocard
    
    app.run_server(debug=True, dev_tools_ui=True)