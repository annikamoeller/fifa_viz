from dash import dcc, html
from jbi100_app.config import *

class Dropdown(html.Div):
 
    def __init__(self, name, dropDownValues, startingValue=None, label=None, multiple_values=False):
        """
        Create a dropdown
        @name (str): name of the plot, used for html_id
        @dropDownValues (array[str]): an array of values to be displayed on the dropdown 
        @startingValue (str): the starting value for the dropdown
        @label (str): the title above the dropdown, leave empty for none
        @multiple_values (bool): whether dropdown should allow selection of multiple values
        """
        self.html_id = name.lower().replace(" ", "-")
        self.dropDownValues = dropDownValues

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.Label(label),
                dcc.Dropdown(
                    id=self.html_id,
                    options=dropDownValues,
                    value=startingValue,
                    multi=multiple_values
                )
            ], style={'margin': 'auto', 'width': '40%', 'color': 'black', 'padding': 20} #Style of the dropdown
        )

    def update(self, on):
        if on: return list(gk_df.columns), list(gk_df.columns)[0]
        else: return player_stats, player_stats[0]
        