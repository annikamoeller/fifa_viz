# Here you can add any global configuations
import pandas as pd

"""Never use these global dataframes directly
If you want to modify them make a new dataframe 
(e.g. df = player_stats) and use that instead"""

team_data = pd.read_csv('../../fifa_viz/FIFA Dataset/Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
teams_list = team_data['team']
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

# Create new stats per 90s for defense df 
df_player_defense['blocked_shots_per_90s'] = df_player_defense['blocked_shots'] / df_player_defense['minutes_90s']
df_player_defense['blocked_passes_per_90s'] = df_player_defense['blocked_passes'] / df_player_defense['minutes_90s']
df_player_defense['blocked_interceptions_per_90s'] = df_player_defense['interceptions'] / df_player_defense['minutes_90s']
df_player_defense['tackles_won_percentage'] = df_player_defense['tackles_won'] / df_player_defense['tackles']

# defense df
defense_radar_df = df_player_defense[['player', 'blocked_shots_per_90s','blocked_passes_per_90s', 'blocked_interceptions_per_90s', 'tackles_won_percentage', 'dribble_tackles_pct']]

# striker df
striker_radar_df = df_player_shooting[['player', 'shots_on_target_pct', 'goals_per_shot', 'average_shot_distance', 'xg', 'shots_per90']]

# goalkeeper df
goalkeeping_radar_df = pd.merge(df_player_keepers[['player', 'gk_save_pct', 'gk_pens_save_pct']], df_player_keepersadv[['player', 'gk_goal_kick_length_avg', 'gk_passes_length_avg', 'gk_goal_kick_length_avg']], on='player', how='inner')

# create new stats for midfielder df 
df_player_misc['aerials_won_pct'] = df_player_misc['aerials_won'] / (df_player_misc['aerials_lost'] + df_player_misc['aerials_won'])
# midfielder df
midfielder_radar_df = pd.merge(df_player_passing[['player','xg_assist', 'passes_pct', 'pass_xa']], df_player_gca[['player','gca']],  on='player', how='inner')
midfielder_radar_df = pd.merge(midfielder_radar_df, df_player_misc[['player','aerials_won_pct']], on = 'player', how='inner')

# total player df for non-keeper players (all stats used in radar plots combined into one df)
total_player_df = pd.merge(midfielder_radar_df, striker_radar_df, on='player', how='inner')
total_player_df = pd.merge(total_player_df, defense_radar_df, on='player', how='inner')

