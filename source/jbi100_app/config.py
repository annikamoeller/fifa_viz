# Here you can add any global configuations
import pandas as pd

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

main_df = pd.concat([goals, xg, birth_year, assists, appearances, yellow_cards, red_cards, passes, touches, shots, offsides, tackles, fouls, dispossessed, own_goals, clearances, position, team], axis=1)
teams_list = main_df['team'].unique()
main_df.fillna("No data")
# goalkeeper df
gk_df = pd.merge(df_player_keepers[['player', 'gk_save_pct', 'gk_pens_save_pct']], df_player_keepersadv[['player', 'gk_passes_length_avg', 'gk_goal_kick_length_avg']], on='player', how='inner')
gk_df = gk_df.set_index('player')

# basic player info df for info card
df_player_basic = df_player_misc[['birth_year', 'team', 'position']]

# # Create new stats per 90s for defense df 
# df_player_defense['blocked_shots_per_90s'] = df_player_defense['blocked_shots'] / df_player_defense['minutes_90s']
# df_player_defense['blocked_passes_per_90s'] = df_player_defense['blocked_passes'] / df_player_defense['minutes_90s']
# df_player_defense['blocked_interceptions_per_90s'] = df_player_defense['interceptions'] / df_player_defense['minutes_90s']
# df_player_defense['tackles_won_percentage'] = df_player_defense['tackles_won'] / df_player_defense['tackles']

# # defense df
# defense_radar_df = df_player_defense[['player', 'blocked_shots_per_90s','blocked_passes_per_90s', 'blocked_interceptions_per_90s', 'tackles_won_percentage', 'dribble_tackles_pct']]
# defense_radar_df = defense_radar_df.set_index('player')

# # striker df
# striker_radar_df = df_player_shooting[['player', 'shots_on_target_pct', 'goals_per_shot', 'average_shot_distance', 'xg', 'shots_per90']]
# striker_radar_df = striker_radar_df.set_index('player')

# # create new stats for midfielder df 
# df_player_misc['aerials_won_pct'] = df_player_misc['aerials_won'] / (df_player_misc['aerials_lost'] + df_player_misc['aerials_won'])
# # midfielder df
# midfielder_radar_df = pd.merge(df_player_passing[['player','xg_assist', 'passes_pct', 'pass_xa']], df_player_gca[['player','gca']],  on='player', how='inner')
# midfielder_radar_df = pd.merge(midfielder_radar_df, df_player_misc[['player','aerials_won_pct']], on = 'player', how='inner')
# midfielder_radar_df = midfielder_radar_df.set_index('player')

# position_df = df_player_misc[['player', 'position']]
# position_df_no_gk = position_df[position_df['position']!='GK']

# # total player df for non-keeper players (all stats used in radar plots combined into one df)
# total_player_df = pd.merge(midfielder_radar_df, striker_radar_df, on='player', how='inner')
# total_player_df = pd.merge(total_player_df, defense_radar_df, on='player', how='inner')
# total_player_df_no_gk = pd.merge(total_player_df, position_df_no_gk, on='player', how='inner')
# total_player_df_no_gk = total_player_df_no_gk.set_index('player')



