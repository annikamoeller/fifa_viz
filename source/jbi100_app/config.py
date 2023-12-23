# Here you can add any global configuations
import pandas as pd

"""Never use these global dataframes directly
If you want to modify them make a new dataframe 
(e.g. df = player_stats) and use that instead"""

team_data = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
teams_list = team_data['team']
player_stats = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')