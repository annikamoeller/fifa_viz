from dash import dcc, html
from jbi100_app.config import *

class Dropdown(html.Div):
 
    def __init__(self, name, dropDownValues, startingValueNormal=None, startingValueGk=None, label=None, multiple_values=False):
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
        self.startingValueNormal = startingValueNormal
        self.startingValueGk = startingValueGk
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.Label(label, 
                           style = {'text-align': 'left'}),
                dcc.Dropdown(
                    id=self.html_id,
                    options=dropDownValues,
                    value=startingValueNormal,
                    multi=multiple_values
                )
            ], style={'margin': 'auto', 'width': '25%', 'color': 'black', 'padding': 10} #Style of the dropdown
        )

    def update(self, on):

        if self.html_id == 'position_dd':
            if on:
                options =  ['GK']
                return options, options
            else: return self.dropDownValues, None 
            
        if on:
            self.dropDownValues = gk_stats 
            return self.dropDownValues, self.startingValueGk 
        else: 
            self.dropDownValues = player_stats 
            return self.dropDownValues, self.startingValueNormal
        