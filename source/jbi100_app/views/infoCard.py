from dash import dcc, html
from jbi100_app.config import *

class InfoCard(html.Div):
 
    def __init__(self, name):
        """
        Create a dropdown
        @name (str): name of the plot, used for html_id
        @dropDownValues (array[str]): an array of values to be displayed on the dropdown 
        @startingValue (str): the starting value for the dropdown
        @label (str): the title above the dropdown, leave empty for none
        """
        self.html_id = name.lower().replace(" ", "-")
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="info_card",
            children=[
                dcc.Textarea(
                id = self.html_id,
                placeholder = 'No player selected',
                value = "",
                style={'width': '50%', 'justifyContent': 'center', 'height': 120, 'padding': 10}
        )],     style=dict(display='flex', justifyContent='center')
)

    def update(self, player_name):
        if player_name:
            return f"Name: {player_name} \n Birth year: {df_player_basic.loc[player_name]['birth_year']} \n Team: {df_player_basic.loc[player_name]['team']} \n Position: {df_player_basic.loc[player_name]['position']}"
        