# Here you can add any global configuations
import pandas as pd
#color_list1 = ["green", "blue"]
#color_list2 = ["red", "purple"]

team_data = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
teams_list = team_data['team']