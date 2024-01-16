# Here you can add any global configuations
import pandas as pd
import numpy as np
from jbi100_app.common import *

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
main_df = main_df.drop(main_df[main_df['position'] == 'GK'].index)

# teams for table drop down
teams_list = list(main_df['team'].unique())

# statistics for table drop down
player_stats = list(main_df.columns)
player_stats.remove('team')
player_stats.remove('position')

# fill NaN values with "No data available message"
main_df.fillna("No data")

# create goalkeeper df
gk_df = pd.merge(df_player_keepers[['player', 'team', 'position', 'gk_save_pct', 'gk_pens_save_pct']], df_player_keepersadv[['player', 'gk_passes_length_avg', 'gk_goal_kick_length_avg']], on='player', how='inner')
gk_df = gk_df.set_index('player')
# statistics for table drop down
gk_stats = list(gk_df.columns)
gk_stats.remove('team')
gk_stats.remove('position')

# basic player info df for info card
df_player_basic = df_player_misc[['birth_year', 'team', 'position']]

# Globally Normalized Data
# normalized_main_df = main_df.drop(["team"])#.apply(normalize_df)
normalized_main_df = main_df.drop(columns=['team', 'position', 'birth_year'])
normalized_main_df = normalized_main_df.apply(normalize_df)

##### Prepare data for usage in Heatmap (and possibly other widgets)
# Attacking DF
df_attack = pd.DataFrame()
# df_attack['Player'] = df_player_shooting.index
# df_attack = df_attack.set_index('Player')
df_attack['Shot Accuracy'] = df_player_shooting['shots_on_target'] / df_player_shooting['shots']
df_attack['SCA per 90s'] = df_player_gca.set_index('player')['sca_per90']
df_attack['GCA per 90s'] = df_player_gca.set_index('player')['gca_per90']
df_attack['Goals per 90s'] = df_player_shooting['goals'] / df_player_shooting['minutes_90s']

# Defensive DF
df_defense = pd.DataFrame()
# df_defense['Player'] = df_player_defense.index
# df_defense = df_defense.set_index('Player')
df_defense['Tackle Succes'] = df_player_defense['tackles_won'] / df_player_defense['tackles']
df_defense['Blocks per 90s'] = df_player_defense['blocks'] / df_player_defense['minutes_90s']
df_defense['Clearances per 90s'] = df_player_defense['clearances'] / df_player_defense['minutes_90s']
df_defense['Severe Error'] = df_player_defense['errors'] / df_player_defense['minutes_90s']


# Possesion
df_possesion = pd.DataFrame()
# df_possesion['Player'] = df_player_possession.index
# df_possesion = df_possesion.set_index('Player')
df_possesion['Touches per 90s'] = df_player_possession['touches'] / df_player_possession['minutes_90s']
df_possesion['Dribble Succes'] = df_player_possession['dribbles_completed_pct']
df_possesion['Miscontrol per 90s'] = df_player_possession['miscontrols'] / df_player_possession['minutes_90s']
df_possesion['Dispossessed per 90s'] = df_player_possession['dispossessed'] / df_player_possession['minutes_90s']


# Concatenate of dataframes (hm=heatmap)
df_hm = pd.concat([df_attack, df_defense, df_possesion], axis=1)
df_hm.replace([np.inf, -np.inf], 0, inplace=True)
df_hm_norm = df_hm.apply(normalize_df)


#Goalkeeper Dataframe for the Heatmap
df_keepers = df_player_keepers[['player', 'gk_goals_against_per90', 'gk_save_pct', 'gk_clean_sheets_pct', 'gk_pens_save_pct']]
df_keepers.set_index('player', inplace=True)

df_keepersadv = df_player_keepersadv[['player', 'gk_passes_pct_launched', 'gk_passes_length_avg', 'gk_crosses_stopped_pct']]
df_keepersadv.set_index('player', inplace=True)

df_gk_hm = pd.concat([df_keepers, df_keepersadv], axis=1)
df_gk_hm.fillna(0, inplace=True)

df_gk_hm.rename(columns={'gk_goals_against_per90':'Goals conceded per 90s',
                         'gk_save_pct':'Goals saved percentage',
                         'gk_clean_sheets_pct':'Clean sheets percentage',
                         'gk_pens_save_pct': 'Penalty save percentage',
                         'gk_passes_pct_launched':'Percentage of successful passes',
                         'gk_passes_length_avg':'Average pass lenght',
                        'gk_crosses_stopped_pct':'Stopped crosses percentage' }, inplace=True)

df_gk_hm_norm = df_gk_hm.apply(normalize_df)


## NAN-Filled Dataframes by median imputation. (main & gk)
df_hm_filled = df_hm.apply(median_imputation_of_nan)
df_gk_hm_filled = df_gk_hm.apply(median_imputation_of_nan)