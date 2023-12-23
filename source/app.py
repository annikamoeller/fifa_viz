from jbi100_app.main import app
from jbi100_app.views.menu import *
from jbi100_app.views.field import *
from jbi100_app.config import *
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from PIL import Image
    
if __name__ == '__main__':

    """ 
    This is the main layout of the webpage, its children are then sub divided
    into further html layouts 
    """
    scatter_plot = Scatterplot("shot_distance", 'birth_year', 'average_shot_distance', player_stats)
    radar_plot = radar("radar", "Messi", "Ronaldo", player_stats)
    
    left_menu_plots = [scatter_plot, radar_plot]
    left_menu = Menu(left_menu_plots)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="one-half column",
                children=left_menu.make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="one-half column",
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
        Output(scatter_plot.html_id, 'figure'),
        Input("select-team", "value")
    )
    def selected_team(team):
        return scatter_plot.update(team)
    
    @app.callback(
    Output(radar_plot.html_id, 'figure'),
    Input(scatter_plot.html_id, 'clickData'),
    Input(scatter_plot.html_id, 'hoverData')
    )
    def selected_player(click, hover):
        newPlayerClicked = False

        if click: clickedPlayer = click['points'][0]['customdata'][0] #get click data
        else: clickedPlayer = None

        if clickedPlayer != scatter_plot.get_click_player():
                previouslyClickedPlayer = scatter_plot.get_click_player()
                scatter_plot.set_click_player(clickedPlayer) 
                newPlayerClicked = True

        if hover: hoveredPlayer = hover['points'][0]['customdata'][0] #get hover data
        else: hoveredPlayer = None
        
        return radar_plot.update(clickedPlayer, hoveredPlayer)

    app.run_server(debug=True, dev_tools_ui=True)