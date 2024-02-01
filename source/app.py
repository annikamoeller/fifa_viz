from jbi100_app.main import app
from jbi100_app.views.menu import *
from jbi100_app.config import *
from jbi100_app.views.dropdown import *
from jbi100_app.views.radar import *
from jbi100_app.views.scatterplot import *
from jbi100_app.views.switch import *
from jbi100_app.views.heatmap import *
from jbi100_app.views.infoCard import *
from jbi100_app.views.table import *
from jbi100_app.views.normalization_switch import *
from jbi100_app.views.picture import *

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
    #similar_player_table = Table("similar_player_table", None, 'birth_year')
    # drop downs 
    table_stat_dropdown = Dropdown("stat_dd", player_stats, startingValueNormal=player_stats[0], startingValueGk='gk_save_pct', label='Select statistic')
    filter_position_dropdown = Dropdown("position_dd", ['FW', 'MF', 'DF'], label='Filter by position', multiple_values=True)
    filter_team_dropdown = Dropdown("team_dd", teams_list, label= 'Filter by team', multiple_values=True)
    # group dropdowns together horizontally
    table_dropdowns = html.Div([table_stat_dropdown, filter_team_dropdown,filter_position_dropdown], style={'display': 'flex', 'flexDirection': 'row', 'margin': 'auto' })

        #Reset button
    reset_button = html.Div(html.Button(children='Reset all plots', 
                                        id='reset_button', 
                                        n_clicks=0,
                                        style={'backgroundColor': 'white'}), 
                                        style={'text-align': 'center',
                                               'padding-left': '3rem', 'padding-top': '1rem'} )

    # Scatter plot
    scatter_plot = Scatterplot("scatterplot", main_df, 'goals', 'goals')
    
    # drop downs for scatter plot 
    x_axis_dropdown = Dropdown("x_axis_dropdown", player_stats, startingValueNormal='birth_year', startingValueGk = 'gk_save_pct', label='X-Axis Values')
    y_axis_dropdown = Dropdown("y_axis_dropdown", player_stats, startingValueNormal='tackles', startingValueGk = 'gk_passes_length_avg', label='Y-Axis Values')
    # group dropdowns together horizontally
    scatter_dropdowns = html.Div([x_axis_dropdown, y_axis_dropdown], style={'display': 'flex', 'flexDirection': 'row'})

    # Radar plot
    radar_plot = Radar("radar", radar_df)

    # player 1 info card
    
    info_card1 = InfoCard("infocard1")

    player_image = Picture("image")
    info_and_image =  html.Div(id='info-and-image', children=[player_image, info_card1], style={'display': 'flex', 'flexDirection': 'row'})

    # player 2 info card
    #info_card2 = InfoCard("infocard2")

    # radar and info card grouping 
    # radar_and_info = html.Div([radar_plot, info_card1], style={'display': 'flex', 'flexDirection': 'row'})

    # Heatmap plot
    normalization_switch = NormalizationSwitch('normalization_switch')
    heatmap_plot = Heatmap("heatmap_plot", radar_df)

    #this variable is used for many callbacks and it represents the highlighted player
    #when saving data in it, it must be serialized by using json.dumps(data)
    #when reading, we must decode by using json.loads(data)
    store = dcc.Store(id='highlighted-player-value')
    hovered_player_store = dcc.Store(id='hello')
    toggle_store = dcc.Store(id = 'toggle-store', data = json.dumps(False))
    previous_toggle_store = dcc.Store(id = 'previous-toggle-store', data=json.dumps(False))

    gk_and_reset =  html.Div(id='gk_and_reset', children=[gk_switch, reset_button], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'center', 'padding': '20px', 'margin': 'auto'})
    # Set up page on left and right
    top_bar = [gk_and_reset]
    #table_title = html.H5("this is my table", style={'text-align': 'center', 'font-family': 'arial', 'font-color': '#ebebeb', 'font-size': 20})

    left_menu_plots = [table_dropdowns, player_data_table, scatter_dropdowns, scatter_plot]
    right_menu_plots = [normalization_switch, heatmap_plot, radar_plot, info_and_image, store, toggle_store, previous_toggle_store]

    #Create left and right side of the page
    app.layout = html.Div(
        id="app-container",
        children=[
            # Top bar
            html.Div(id="top", className="top-bar", children = top_bar),
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
        Output('toggle-store', 'data'),
        Output('previous-toggle-store', 'data'),
        Input(gk_switch.html_id, 'on'),
        Input('previous-toggle-store', 'data')
    )
    def toggle_gk_mode(on, previous_toggle_store):
        x_options, x_value = x_axis_dropdown.update(on)
        y_options, y_value = y_axis_dropdown.update(on)
        filter_options, filter_value = filter_position_dropdown.update(on)
        table_stat_options, table_stat_value = table_stat_dropdown.update(on)
        previous_toggle = json.loads(previous_toggle_store)

        if on and not previous_toggle: 
            toggled = True
            previous_toggle_store = True
        if not on and previous_toggle: 
            toggled = True
            previous_toggle_store = False
        if not on and not previous_toggle: 
            toggled = False
            previous_toggle_store = False
        if on and previous_toggle: 
            toggled = False
            previous_toggle_store = True
        return x_options, x_value, y_options, y_value, filter_options, filter_value, table_stat_options, table_stat_value, json.dumps(toggled), json.dumps(previous_toggle_store)

    # update the scatter plot based on the x and y drop downs
    @app.callback(
        Output(scatter_plot.html_id, 'figure'),
        Output('highlighted-player-value', 'data'),
        Output(player_data_table.html_id, 'style_data_conditional'),
        Output('toggle-store', 'data', allow_duplicate=True),
        Input('toggle-store', 'data'),
        Input(gk_switch.html_id, 'on'),
        Input(scatter_plot.html_id, 'clickData'),
        Input(x_axis_dropdown.html_id, "value"),
        Input(y_axis_dropdown.html_id, "value"),
        Input(table_stat_dropdown.html_id, 'value'),
        Input(filter_team_dropdown.html_id, 'value'),
        Input(filter_position_dropdown.html_id, 'value'),
        Input(player_data_table.html_id, 'data'),
        Input(player_data_table.html_id, "page_current"),
        Input(player_data_table.html_id, "page_size"),
        Input(player_data_table.html_id, 'active_cell'),
        prevent_initial_call=True
    )
    def update_scatter(gk_toggled, on, click, x_label, y_label, selected_stat, team_filter, position_filter, clicked_table_player_data, current_page, page_size, clicked_cell):
        """
        Return a figure with a teams plot based on team dropdown value 
        """
        gk_toggled = json.loads(gk_toggled)
        scatter_plot.set_gk_toggled(gk_toggled)
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

        lightgrey_highlight_style = [
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
            try:
                table_player = clicked_table_player_data[clicked_cell['row']+(current_page)*page_size]['player']
            except: 
                table_player = None
        else: table_player = None
        
        if click: 
            scatter_player = click['points'][0]['customdata'][0] #get click data
        else: scatter_player = None
        #get the previously clicked players
        prev_table_click, prev_scatter_click = scatter_plot.get_click_player()
        #if the players are not the same and a new value is clicked, set it
        if table_player != scatter_player:
            if prev_table_click != table_player: player = table_player

            elif prev_scatter_click != scatter_player: 
                player = scatter_player
                style = lightgrey_highlight_style.copy()
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
                if not table_player:
                    scatter_plot.set_click_player(None, None)
                else:
                    player = table_player
                    scatter_plot.set_click_player(table_player, None)
                    style = lightgrey_highlight_style.copy()
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
        if gk_toggled:
            player = None
        return scatter_plot.update(on, x_label, y_label, selected_stat, team_filter, position_filter, player), json.dumps(player), style, json.dumps(False)
    
    # update the table based on the drop downs
    @app.callback(
            Output(player_data_table.html_id, 'data'),
            Output(player_data_table.html_id, 'columns'),
            Input(table_stat_dropdown.html_id, 'value'),
            Input(filter_team_dropdown.html_id, 'value'),
            Input(filter_position_dropdown.html_id, 'value'),
            Input(gk_switch.html_id, 'on'),
            #Input(player_data_table.html_id, 'active_cell')
    )
    def update_table(selected_stat, team, position, on):
        new_data, new_cols = player_data_table.update(selected_stat, on, team, position)
        return new_data, new_cols
    
    # reset the selected cells
    @app.callback(
            Output(player_data_table.html_id, 'active_cell', allow_duplicate=True),
            Output(player_data_table.html_id, 'selected_cells', allow_duplicate=True),
            Output(radar_plot.html_id, 'figure', allow_duplicate=True),
            Input('reset_button', 'n_clicks'),
            prevent_initial_call=True
    )
    def reset_table(n_clicks):
        if n_clicks not in [0, None]:
            return None, [], radar_plot.update(False, None, None)
         
    #update the similar player heatmap
    @app.callback(
            Output(heatmap_plot.html_id, 'figure'),
            Input(gk_switch.html_id, 'on'),
            Input(normalization_switch.html_id, 'on'),
            Input('highlighted-player-value', 'data'),
            Input(scatter_plot.html_id, 'selectedData')
    )
    def update_similar_players(goalkeeper_mode, local_normalization, highlight_player_data, selected_players_in_scatter_plot):
        player = json.loads(highlight_player_data)
        new_heatmap = heatmap_plot.initial_heatmap(goalkeeper_mode=goalkeeper_mode)

        if player:
            similar_players = get_similar_players(goalkeeper_mode, player)
            similar_players = similar_players.set_index('player')
            similar_player_names = similar_players.index.tolist()
            new_heatmap = heatmap_plot.update(goalkeeper_mode, player, similar_player_names, local_normalization)
        try:
            selected_names_in_scatter_plot = [player['customdata'][0] for player in selected_players_in_scatter_plot['points']]
            if not selected_names_in_scatter_plot:
                pass
            else:
                new_heatmap = heatmap_plot.update(goalkeeper_mode, player, selected_names_in_scatter_plot, local_normalization)
        except: 
            pass

        #return new_data, columns, new_heatmap
        return new_heatmap
    
    # update the radar plot based on click and hover data
    @app.callback(
    Output(radar_plot.html_id, 'figure'),
    Input(scatter_plot.html_id, 'hoverData'),
    Input('highlighted-player-value', 'data'),
    Input(gk_switch.html_id, 'on'),
    Input('toggle-store', 'data')
    )
    def selected_player(hover, highlight_player_data, on, toggle_store):
        """
        Get clicked, hovered player and stats dropdown value 
        return a radar figure with the stats of the selected players and dropdown
        """
        toggled = scatter_plot.get_gk_toggled()

        highlight_player_data = json.loads(highlight_player_data)

        if hover: hover_player = hover['points'][0]['customdata'][0] #get hover data
        else: hover_player = None

        if toggled:
            hover_player = None
            scatter_plot.set_gk_toggled(False)
            return radar_plot.clear(df_radar)
        return radar_plot.update(on, highlight_player_data, hover_player)

    # update info card to display basic player info when clicked on in scatter plot 
    @app.callback(
        Output(info_card1.html_id, 'value'),
        Output(player_image.html_id, 'src'),
        Input('highlighted-player-value', 'data')
    )
    def info_card(highlight_player_data):
        highlight_player_data = json.loads(highlight_player_data)
        if highlight_player_data:
            return info_card1.update(highlight_player_data), player_image.update(highlight_player_data, 13)
        else: return "", "" #empty infocard
    
    app.run_server(debug=True, dev_tools_ui=True)