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
df_player_misc          = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_misc.csv', delimiter=',')
df_player_defense       = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_defense.csv', delimiter=',')
df_player_gca           = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_gca.csv', delimiter=',')
df_player_passing       = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_passing.csv', delimiter=',')
#df_player_passing_types = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_passing_types.csv', delimiter=',')
df_player_playingtime   = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_playingtime.csv', delimiter=',')
df_player_possession    = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_possession.csv', delimiter=',')
df_player_shooting      = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')
df_player_stats         = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')
df_player_keepers       = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_keepers.csv', delimiter=',')
df_player_keepersadv    = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Player Data/player_keepersadv.csv', delimiter=',')

# set index to player 
df_player_misc =df_player_misc.set_index('player')
df_player_defense =df_player_defense.set_index('player')
df_player_gca = df_player_gca.set_index('player')
df_player_passing= df_player_passing.set_index('player')
#df_player_passing_types = df_player_passing_types.set_index('player')
df_player_playingtime =df_player_playingtime.set_index('player')
df_player_possession= df_player_possession.set_index('player')
df_player_shooting= df_player_shooting.set_index('player')
df_player_stats = df_player_stats.set_index('player')
df_player_keepers = df_player_keepers.set_index('player')
df_player_keepersadv = df_player_keepersadv.set_index('player')

##### MAIN DATA #####
# remove players with 0 starts
df_player_playingtime = df_player_playingtime[df_player_playingtime['games_starts']!=0]

# gather useful statistics 
team = df_player_misc['team']
position = df_player_misc['position']
fouls = df_player_misc['fouls']
own_goals = df_player_misc['own_goals']
aerials_won = df_player_misc['aerials_won']
offsides = df_player_misc['offsides']

tackles = df_player_defense['tackles']
tackles_won = df_player_defense['tackles_won']
clearances = df_player_defense['clearances']
blocks = df_player_defense['blocks']
errors = df_player_defense['errors']

goal_creating_actions = df_player_gca['gca']
shot_creating_actions = df_player_gca['sca']
goal_creating_actions_90s = df_player_gca['gca_per90']
shot_creating_actions_90s = df_player_gca['sca_per90']


passes = df_player_passing['passes_completed']
passes_pct = df_player_passing['passes_pct']
passes_total_distance = df_player_passing['passes_total_distance']
passes_pct_long = df_player_passing['passes_pct_long']
progressive_passes = df_player_passing['progressive_passes']

appearances = df_player_playingtime['games_starts']

touches = df_player_possession['touches']
dispossessed = df_player_possession['dispossessed']
aerials_won_pct = df_player_misc['aerials_won_pct']
dribbles_completed_pct = df_player_possession['dribbles_completed_pct']
passes_received = df_player_possession['passes_received']
miscontrols  = df_player_possession['miscontrols']

goals = df_player_shooting['goals']
shots = df_player_shooting['shots']
shots_on_target = df_player_shooting['shots_on_target']
shots_on_target_pct= df_player_shooting['shots_on_target_pct']
goals_per_shot= df_player_shooting['goals_per_shot']
average_shot_distance= df_player_shooting['average_shot_distance']
pens_made= df_player_shooting['pens_made']
pens_att= df_player_shooting['pens_att']

xg = df_player_stats['xg']
birth_year = df_player_stats['birth_year']
assists = df_player_stats['assists']
yellow_cards = df_player_stats['cards_yellow']
red_cards = df_player_stats['cards_red']
minutes_90s= df_player_stats['minutes_90s']


############

##### INFO CARD DF#####
df_player_basic = pd.concat([birth_year, team, position, minutes_90s],axis=1)


##### MAIN DF #####
main_df = pd.concat([goals, xg, birth_year, assists, appearances, yellow_cards, red_cards, passes, touches, shots,
                     offsides, tackles, fouls, dispossessed, own_goals, clearances, position, team, shot_creating_actions, goal_creating_actions,
                    blocks, miscontrols], axis=1)
print(main_df.head())

#Drop goalkeepers
main_df = main_df.drop(main_df[main_df['position'] == 'GK'].index)

# fill NaN values with "No data available message"
main_df.fillna('No data')


##### MAIN DF 90S ######
main_df_90s = pd.DataFrame(index=main_df.index)

for column in main_df.columns:
    if column not in ['xg', 'birth_year', 'position', 'team']:
        main_df_90s[column + ' per 90s'] = main_df[column]/minutes_90s


##### TABLE DF #####
table_df = pd.concat([main_df, main_df_90s], axis=1)


# teams for table drop down
teams_list = list(main_df['team'].unique())
teams_list = sorted(teams_list)

# statistics for table drop down
player_stats = list(main_df.columns)
player_stats.remove('team')
player_stats.remove('position')
player_stats = sorted(player_stats)


##### RADAR DF #####

radar_df = pd.DataFrame()

# create main dataframe
aux_radar_df = pd.concat([position, minutes_90s,
                     goals, shots_on_target_pct, goals_per_shot, average_shot_distance,pens_made,pens_att,
                     tackles,tackles_won, clearances, blocks, errors,
                     touches, dispossessed, aerials_won_pct, dribbles_completed_pct, passes_received, miscontrols,
                     assists, passes_pct, passes_total_distance, passes_pct_long, progressive_passes,
                     red_cards, yellow_cards, fouls
                     ], axis=1)
aux_radar_df = aux_radar_df.drop(aux_radar_df[aux_radar_df['position'] == 'GK'].index)


aux_radar_df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

def get_attack_score(row):
    if (row['pens_att'] == 0): pens = 0
    else: pens = row['pens_made'] / row['pens_att']

    if row['minutes_90s'] == 0: goals = 0
    else: goals = row['goals']/row['minutes_90s']


    score = 1 + (pens 
             + goals
             + 2*row['goals_per_shot']/df_player_shooting['goals_per_shot'].max() 
             + row['shots_on_target_pct']/100
             + row['average_shot_distance']/df_player_shooting['average_shot_distance'].max() )

    return min(score, 5)

def get_defense_score(row):
    if (row['tackles'] == 0): tackles = 0
    else: tackles = row['tackles_won'] / row['tackles']

    score = 1 +(5/3*tackles 
             + 5/3*row['blocks']/df_player_defense['blocks'].max()
             + 5/3*row['clearances']/df_player_defense['blocks'].max() 
             - 2*row['errors'])

    return min(max(score, 0),5)

def get_control_score(row):
    if row['passes_received'] == 0: pen = 0
    else: pen = (row['miscontrols']+row['dispossessed'])/( row['passes_received'])

    score = 1+ (2*row['aerials_won_pct']/100
             + row['touches']/df_player_possession['touches'].max()
             + 2*row['dribbles_completed_pct']/100
             - pen)

    return min(max(score, 0), 5)

def get_passing_score(row):

    score = 1 + (row['passes_pct']/100
             + 0.5*row['passes_total_distance']/df_player_passing['passes_total_distance'].max()
             + 0.25*row['passes_pct_long']/100
             + 2.5*row['assists']/df_player_passing['assists'].max()
             + 0.75*row['progressive_passes']/df_player_passing['progressive_passes'].max())

    return min(score,5)

def get_discipline_score(row):

    if row['minutes_90s'] == 0:
        return 5
    else:
        score = 5 - (2.5*row['cards_red']
             + 5/3* row['cards_yellow']
             + row['fouls'])/row['minutes_90s']

    return max(score, 0)


radar_df['Attack'] = aux_radar_df.apply(get_attack_score, axis=1)
radar_df['Defense'] = aux_radar_df.apply(get_defense_score, axis=1)
radar_df['Control'] = aux_radar_df.apply(get_control_score, axis=1)
radar_df['Passing'] = aux_radar_df.apply(get_passing_score, axis=1)
radar_df['Discipline'] = aux_radar_df.apply(get_discipline_score, axis=1)


###### Gk Dfs######

# gather useful statistics 
#stopping
gk_clean_sheets_pct = df_player_keepers['gk_clean_sheets_pct']
gk_save_pct = df_player_keepers['gk_save_pct']

#defense
gk_crosses_stopped_pct = df_player_keepersadv['gk_crosses_stopped_pct']
gk_def_actions_outside_pen_area_per90 = df_player_keepersadv['gk_def_actions_outside_pen_area_per90']
gk_avg_distance_def_actions = df_player_keepersadv['gk_avg_distance_def_actions']

#penalty
gk_pens_save_pct = df_player_keepers['gk_pens_save_pct']

#passing
gk_passes_pct_launched = df_player_keepersadv['gk_passes_pct_launched']
gk_passes_length_avg  = df_player_keepersadv['gk_passes_length_avg']

#kick
gk_goal_kick_length_avg = df_player_keepersadv['gk_goal_kick_length_avg']
gk_pct_goal_kicks_launched= df_player_keepersadv['gk_pct_goal_kicks_launched']


# create main dataframe
main_gk_df = pd.concat([position, team, minutes_90s, appearances,
                        gk_clean_sheets_pct, gk_save_pct,
                        gk_crosses_stopped_pct, gk_def_actions_outside_pen_area_per90, gk_avg_distance_def_actions,
                        gk_pens_save_pct,
                        gk_passes_pct_launched, gk_passes_length_avg,
                        gk_goal_kick_length_avg, gk_pct_goal_kicks_launched
                     ], axis=1)
main_gk_df = main_gk_df.drop(main_gk_df[main_gk_df['position'] != 'GK'].index)


main_gk_df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# statistics for table drop down
gk_stats = list(main_gk_df.columns)
gk_stats.remove('team')
gk_stats.remove('position')

radar_gk_df = pd.DataFrame()

def get_stopping_score(row):
    return 2*row['gk_clean_sheets_pct']/100 + 3*row['gk_save_pct']/100

def get_defense_score(row):
    
    score = (2*row['gk_crosses_stopped_pct']/100
             + 2*row['gk_def_actions_outside_pen_area_per90']/df_player_keepersadv['gk_def_actions_outside_pen_area_per90'].max()
             + row['gk_avg_distance_def_actions']/df_player_keepersadv['gk_avg_distance_def_actions'].max())

    return score

def get_penalty_score(row):
    return 5*row['gk_pens_save_pct']/100

def get_passing_score(row):

    score = (row['gk_passes_length_avg']/df_player_keepersadv['gk_passes_length_avg'].max()
             + 4*row['gk_passes_pct_launched']/100)

    return score

def get_kick_score(row):

    score = (2*row['gk_goal_kick_length_avg']/df_player_keepersadv['gk_goal_kick_length_avg'].max()
            + 3*row['gk_pct_goal_kicks_launched']/100)

    return score

radar_gk_df['Stopping'] = main_gk_df.apply(get_stopping_score, axis=1)
radar_gk_df['Defense'] = main_gk_df.apply(get_defense_score, axis=1)
radar_gk_df['Kick'] = main_gk_df.apply(get_kick_score, axis=1)
radar_gk_df['Passing'] = main_gk_df.apply(get_passing_score, axis=1)
radar_gk_df['Penalty'] = main_gk_df.apply(get_penalty_score, axis=1)


#################################################FUCKING GK END #####################################################

def get_similar_players(on, player, num_similar_players=5):
    """
    @player (str): the player for which we want similar players
    @num_similar_players (str): the number of players that we want returned
    @returns ->>> similar player data and columns for table
    """
    if on: df = radar_gk_df
    else: df = radar_df

    player = df.loc[player].values
    player = player.reshape(1, -1)
    df = df.dropna()

    result = cosine_similarity(player, df)

    result = np.array(result)
    result = result.round(8)
    x = np.argsort(result[0])[::-1][1:num_similar_players+1]
    similar_player_df = df.iloc[x]
    similar_player_df = similar_player_df.reset_index()
    return similar_player_df