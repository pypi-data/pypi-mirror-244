import pandas as pd
import numpy as np
#from get_players_from_md import read_players
#from helpers import (get_teams, calculate_skill, skill_map, eval_codes)

class DataVolley:
    def __init__(self, file_path):
        self.file_path = file_path
        self._read_data()

    def get_teams(self, rows_list):
        teams_index = rows_list.index('[3TEAMS]\n')
        home_team = rows_list[teams_index + 1].strip()
        visiting_team = rows_list[teams_index + 2].strip()
        return home_team, visiting_team

    def calculate_skill(self, row):
        if pd.isna(row['player_number']):
            return np.nan
        else:
            return row['code'][3]

    skill_map = {
        "S": "Serve",
        "R": "Reception",
        "E": "Set", 
        "A": "Attack",
        "D": "Dig",
        "B": "Block",
        "F": "Freeball",
        "p": 'Point'
    }

    eval_codes = ["#", "+", '!', '-', '/', '=']

    @staticmethod
    def read_players(meta_data, team_name, H_or_V):
        columns_to_rename = {
            1: "player_number", 3: "starting_position_set1", 4: "starting_position_set2", 5: "starting_position_set3", 
            6: "starting_position_set4", 7: "starting_position_set5", 8: "player_id", 9: "lastname", 
            10: "firstname", 11: "nickname", 12: "special_role", 13: "role", 14: "foreign"
            }
        team_players = meta_data[(meta_data['meta_group'] == f'3PLAYERS-{H_or_V}') & (meta_data[0] != f'[3PLAYERS-{H_or_V}]\n')][0].str.split(';', expand = True)
        team_players.columns = [columns_to_rename[col] if col in columns_to_rename else col for col in team_players.columns]

        # Trim whitespace from nickname, firstname, and lastname
        team_players['nickname'] = team_players['nickname'].str.strip()
        team_players['firstname'] = team_players['firstname'].str.strip()
        team_players['lastname'] = team_players['lastname'].str.strip()

        # Replace NA values in nickname, firstname, and lastname with empty strings
        team_players['nickname'].fillna("", inplace=True)
        team_players['firstname'].fillna("", inplace=True)
        team_players['lastname'].fillna("", inplace=True)

        # Trim whitespace from firstname and lastname again after replacing NA values
        team_players['firstname'] = team_players['firstname'].str.strip()
        team_players['lastname'] = team_players['lastname'].str.strip()

        # Create a new 'name' column by concatenating firstname and lastname with a space separator
        team_players['player_name'] = team_players['firstname'] + ' ' + team_players['lastname']

        idx = team_players[team_players['player_name'].apply(lambda x: not bool(x))].index

        # If there are such indices, replace 'name' with "Unnamed player" followed by a sequence number
        if len(idx) > 0:
            team_players.loc[idx, 'player_name'] = ["Unnamed player " + str(i + 1) for i in range(len(idx))]

        # Trim whitespace from 'player_id', 'starting_position_set1', 'starting_position_set2', 'starting_position_set3', 'starting_position_set4', 'starting_position_set5'
        columns_to_trim = ['player_id', 'starting_position_set1', 'starting_position_set2', 'starting_position_set3', 'starting_position_set4', 'starting_position_set5']
        team_players[columns_to_trim] = team_players[columns_to_trim].apply(lambda x: x.str.strip())

        # Replace NA values in 'foreign' with False
        team_players['foreign'].fillna(False, inplace=True)

        # Convert 'number' column to integer
        team_players['number'] = team_players['player_number'].astype(str)

        team_players['team'] = team_name
        team_players = team_players[['player_number', 'player_id', 'player_name', 'team']]
        return team_players

    def _read_data(self):
        rows = [] # Initialize lists to store data
        with open(self.file_path, 'r') as file: # Read the file and extract data
            for line in file:
                rows.append(line)

        full_file = pd.DataFrame(rows)
        full_file['meta_group'] = full_file[0].str.extract(r'\[(.*?)\]', expand=False).ffill()

        # Get Player Names
        meta_data = full_file[full_file['meta_group'] != '3SCOUT']

        # Get teams metadata
        teams = self.get_teams(rows)
        home_team_id = teams[0].split(";")[0]
        visiting_team_id = teams[1].split(";")[0]
        home_team = teams[0].split(";")[1]
        visiting_team = teams[1].split(";")[1]

        # Parse out the [3SCOUT] and keep the rest
        index_of_scout = full_file.index[full_file[0] == '[3SCOUT]\n'][0]

        # Filter everything before and after "[3SCOUT]"
        plays = full_file.iloc[index_of_scout+1:].reset_index(drop = True)

        # Create code, point_phase attack_phase start_coordinate mid_coordainte end_coordainte time set home_rotation visitng_rotation video_file_number video_time
        plays = plays[0].str.split(';', expand = True).rename({0: 'code', 1: 'point_phase', 2: 'attack_phase', 4: 'start_coordinate', 5: 'mid_coordainte', 6: 'end_coordainte', 7: 'time', 8: 'set', 9: 'home_setter_position', 10: 'visiting_setter_position', 11: 'video_file_number', 12: 'video_time'}, axis=1)
        plays.columns.values[14:20] = [f"home_p{i+1}" for i in range(6)]
        plays.columns.values[20:26] = [f"visiting_p{i+1}" for i in range(6)]
        plays = plays.drop(columns=([3, 13, 26]))

        # Change coordiantes -1-1
        plays['start_coordinate'] = np.where(plays['start_coordinate'] == '-1-1', np.nan, plays['start_coordinate'])
        plays['mid_coordainte'] = np.where(plays['mid_coordainte'] == '-1-1', np.nan, plays['mid_coordainte'])
        plays['end_coordainte'] = np.where(plays['end_coordainte'] == '-1-1', np.nan, plays['end_coordainte'])

        # Create team
        plays['team'] = np.where(plays['code'].str[0:1] == '*', home_team, visiting_team)

        # Create player_number
        plays['player_number'] = plays['code'].str[1:3].str.extract(r'(\d{2})').astype(float).fillna(0).astype(int).astype(str)
        plays['player_number'] = np.where(plays['player_number'] == '0', np.nan, plays['player_number'])

        # Create player_name for both teams
        plays = pd.merge(plays, pd.concat(list([self.read_players(meta_data, home_team, 'H'), 
                                                self.read_players(meta_data, visiting_team, 'V')])
                                        ), on=['player_number', 'team'], how='left')

        # Create skill
        plays['skill'] = plays.apply(self.calculate_skill, axis=1)
        plays['skill'] = plays['skill'].map(self.skill_map)

        # Create evaluation_code
        plays['evaluation_code'] = plays['code'].str[5]
        plays['evaluation_code'] = np.where(plays['evaluation_code'].isin(self.eval_codes), plays['evaluation_code'], np.nan)

        # Create set_code
        plays['set_code'] = np.where(plays['skill'] == 'Set', plays['code'].str[6:8], np.nan)
        plays['set_code'] = np.where((plays['skill'] == 'Set') & (plays['set_code'] != '~~'), plays['set_code'], np.nan)

        # Create set_type
        plays['set_type'] = np.where(plays['skill'] == 'Set', plays['code'].str[8:9], np.nan)
        plays['set_type'] = np.where((plays['skill'] == 'Set') & (plays['set_type'] != '~~'), plays['set_type'], np.nan)

        # Create attack code
        plays['attack_code'] = plays['code'].str[6:8]
        plays['attack_code'] = np.where((plays['skill'] == 'Attack') & (plays['attack_code'] != '~~'), plays['attack_code'], np.nan)

        # Create num_players_numeric 
        plays['num_players_numeric'] = np.where(plays['skill'] == 'Attack', plays['code'].str[13:14], np.nan)
        plays['num_players_numeric'] = np.where((plays['skill'] == 'Attack') & (plays['num_players_numeric'] != '~~'), plays['num_players_numeric'], np.nan)

        # Create home_team_id
        plays['home_team_id'] = home_team_id
        plays['visiting_team_id'] = visiting_team_id

        # Create start_zone
        plays['start_zone'] = plays['code'].str[9:10]
        plays['start_zone'] = np.where(plays['start_zone'] != '~', plays['start_zone'], np.nan)
        plays['start_zone'] = np.where(plays['start_zone'] == '', np.nan, plays['start_zone'])

        # Create end_zone
        plays['end_zone'] = plays['code'].str[10:11]
        plays['end_zone'] = np.where(plays['end_zone'] != '~', plays['end_zone'], np.nan)
        plays['end_zone'] = np.where(plays['end_zone'] == '', np.nan, plays['end_zone'])

        # Create end_subzone
        plays['end_subzone'] = plays['code'].str[11:12]
        plays['end_subzone'] = np.where(plays['end_subzone'] != '~', plays['end_subzone'], np.nan)
        plays['end_subzone'] = np.where(plays['end_subzone'] == '', np.nan, plays['end_subzone'])

        # Create rally number
        plays['rally_number'] = plays.groupby('set', group_keys=False)['skill'].apply(lambda x: (x == 'Serve').cumsum())

        # Create point_won_by
        plays['point_won_by'] = plays.apply(lambda row: home_team if row['code'][0:2] == '*p' else visiting_team if row['code'][0:2] == 'ap' else None, axis=1)
        plays['point_won_by'] = plays['point_won_by'].bfill()
        plays['point_won_by'] = np.where(plays['code'].str.contains('Up'), np.nan, plays['point_won_by'])
        plays['point_won_by'] = np.select(
            [
                plays['code'].str.contains(r'\*\*1set'),
                plays['code'].str.contains(r'\*\*2set'),
                plays['code'].str.contains(r'\*\*3set'),
                plays['code'].str.contains(r'\*\*4set'),
                plays['code'].str.contains(r'\*\*5set')
            ],
            [np.nan, np.nan, np.nan, np.nan, np.nan],
            plays['point_won_by']
            )

        # Create point on skill
        plays['skill'] = np.where(plays['code'].str[1:2] == 'p', 'Point', plays['skill'])

        # Create home_team_score
        plays['home_team_score'] = plays[plays['code'].str[1:2] == 'p']['code'].str[2:4]
        plays['home_team_score'] = plays.groupby(['set', 'rally_number'])['home_team_score'].bfill()

        # Create visiting_team_score
        plays['visiting_team_score'] = plays[plays['code'].str[1:2] == 'p']['code'].str[5:7]
        plays['visiting_team_score'] = plays.groupby(['set', 'rally_number'])['visiting_team_score'].bfill()

        # Create coordinates

        # Create winning_attack

        # Create serving_team
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == '*'), home_team, None)
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == 'a'), visiting_team, plays['serving_team'])
        plays['serving_team'] = plays.groupby(['set', 'rally_number'])['serving_team'].ffill()

        # Create receiving_team
        plays['receiving_team'] = np.where(plays['serving_team'] == home_team, visiting_team, home_team)
        self.plays = plays.replace('', np.nan)

        # Create phase

        # Create home_score_start_of_point

        # Create visiting_score_start_of_point

        # Create team_touch_id

        # Create video_time

        # Create vieo_file_number

        # Create point_id

        # Create match_id

        # Create timeout

        # Create end_of_set

        # Create substitution

        # Create custom code

        # Create file line number

    def get_plays(self):
        return self.plays
