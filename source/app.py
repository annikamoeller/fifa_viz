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
    
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="one-half column",
                children=make_menu_layout()
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
        return Scatterplot.update(team)

    app.run_server(debug=True, dev_tools_ui=False)