from dash import dcc, html
from jbi100_app.config import *
from PIL import Image
import cv2 as cv2

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
        #Using Pillow to read the the image

        # im = cv2.imread("jbi100_app/assets/soccer_field_3.jpg")
        
        pil_img = Image.open(open("jbi100_app/assets/soccer_field_3.jpg", 'rb'))

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.Img(id=self.html_id, src=pil_img)],     
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
                        for player_name in os.listdir(team_path):
                            if player_name != '.DS_Store':
                                player_name_processed = player_name.split('_')[1].split('(')[0].strip()
                                player_name_path = os.path.join(team_path, player_name)
                                if player_name_processed == name:
                                    img_path = os.path.join(player_name_path, f'{name}{random_number}.jpg')
                                    pil_img = Image.open(img_path)
                                    return pil_img