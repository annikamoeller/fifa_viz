from dash import dcc, html
from jbi100_app.config import *
from PIL import Image
from unidecode import unidecode
import random

class Picture(html.Div):
 
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
            className="graph_card",
            children=[
                html.Img(id=self.html_id)],     
                style=dict(display='flex', justifyContent='left', backgroundColor='#26232C', color='white'), 
)
        
    def update(self, name, random_number):
        main_path = '../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Images/Images/'
        for group in os.listdir(main_path):
            if group != '.DS_Store':
                group_path = os.path.join(main_path, group)
                for team in os.listdir(group_path):
                    if team != '.DS_Store':
                        team_path = os.path.join(group_path, team)
                        for player_folder in os.listdir(team_path):
                            if player_folder != '.DS_Store':
                                player_folder_no_Images_ = player_folder.split('_')[1] # remove 'Images_
                                player_folder_no_Images_or_captain = player_folder_no_Images_.split('(')[0].strip() # remove (captain)
                                player_folder_no_Images_captain_or_accents = unidecode(player_folder_no_Images_or_captain) # remove accents for comparison
                                name_processed = unidecode(name) # remove accents for comparison
                                player_name_path = os.path.join(team_path, player_folder)
                                n_images = len(os.listdir(player_name_path))
                                random_number = random.randint(1,n_images)
                                if player_folder_no_Images_captain_or_accents == name_processed:
                                    img_path = os.path.join(player_name_path, f'{player_folder_no_Images_}{random_number}.jpg')
                                    pil_img = Image.open(img_path)
                                    pil_img = pil_img.resize((230,200))
                                    return pil_img