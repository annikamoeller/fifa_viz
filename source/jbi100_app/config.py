# Here you can add any global configuations
import pandas as pd
from jbi100_app.views.normalize_df import *

"""Never use these global dataframes directly
If you want to modify them make a new dataframe 
(e.g. df = player_stats) and use that instead"""

team_data = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
player_stats = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')

# Player data
df_player_defense       = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_defense.csv', delimiter=',')
df_player_gca           = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_gca.csv', delimiter=',')
df_player_keepers       = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_keepers.csv', delimiter=',')
df_player_keepersadv    = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_keepersadv.csv', delimiter=',')
df_player_misc          = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_misc.csv', delimiter=',')
df_player_passing       = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_passing.csv', delimiter=',')
df_player_passing_types = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_passing_types.csv', delimiter=',')
df_player_playingtime   = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_playingtime.csv', delimiter=',')
df_player_possession    = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_possession.csv', delimiter=',')
df_player_shooting      = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')
df_player_stats         = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')

# set index to player 
df_player_stats = df_player_stats.set_index('player')
df_player_defense =df_player_defense.set_index('player')
df_player_misc =df_player_misc.set_index('player')
df_player_passing= df_player_passing.set_index('player')
df_player_shooting= df_player_shooting.set_index('player')
df_player_possession= df_player_possession.set_index('player')
df_player_playingtime =df_player_playingtime.set_index('player')

# remove players with 0 starts
df_player_playingtime = df_player_playingtime[df_player_playingtime['games_starts']!=0]

# gather useful statistics 
goals = df_player_stats['goals']
xg = df_player_stats['xg']
birth_year = df_player_stats['birth_year']
goal_creating_actions = df_player_gca['gca']
assists = df_player_stats['assists']
appearances = df_player_playingtime['games_starts']
yellow_cards = df_player_stats['cards_yellow']
red_cards = df_player_stats['cards_red']
passes = df_player_passing['passes_completed']
touches = df_player_possession['touches']
shots = df_player_shooting['shots']
offsides = df_player_misc['offsides']
tackles = df_player_defense['tackles']
fouls = df_player_misc['fouls']
dispossessed = df_player_possession['dispossessed']
own_goals = df_player_misc['own_goals']
clearances = df_player_defense['clearances']
aerials_won = df_player_misc['aerials_won']
position = df_player_misc['position']
team = df_player_misc['team']

# create main dataframe
main_df = pd.concat([goals, xg, birth_year, assists, appearances, yellow_cards, red_cards, passes, touches, shots, offsides, tackles, fouls, dispossessed, own_goals, clearances, position, team], axis=1)

# teams for table drop down
teams_list = list(main_df['team'].unique())

# statistics for table drop down
player_stats = list(main_df.columns)
player_stats.remove('team')
player_stats.remove('position')

# fill NaN values with "No data available message"
main_df.fillna("No data")

# create goalkeeper df
gk_df = pd.merge(df_player_keepers[['player', 'gk_save_pct', 'gk_pens_save_pct']], df_player_keepersadv[['player', 'gk_passes_length_avg', 'gk_goal_kick_length_avg']], on='player', how='inner')
gk_df = gk_df.set_index('player')

# basic player info df for info card
df_player_basic = df_player_misc[['birth_year', 'team', 'position']]

# Globally Normalized Data
# normalized_main_df = main_df.drop(["team"])#.apply(normalize_df)
normalized_main_df = main_df.drop(columns=['team', 'position', 'birth_year'])
normalized_main_df = normalized_main_df.apply(normalize_df)

