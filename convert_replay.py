import carball
import gzip
import sys
import json

from typing import List
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager

from replay_player import ReplayPlayer
from replay_positions import ReplayPositions

def better_jsonify(response: object):
    try:
        if hasattr(response, 'to_JSON'):
            return better_jsonify(response.to_JSON())
    except:
        pass

    try:
        return json.dumps(response)
    except TypeError as e:
        if isinstance(response, list):
            return json.dumps([value.__dict__ for value in response])
        else:
            return json.dumps(response.__dict__)
 
if len(sys.argv) != 2:
    raise ValueError('Please provide the input replay file!')

replay_file = sys.argv[1]

_json = carball.decompile_replay(replay_file)

game = Game()
game.initialize(loaded_json=_json)

analysis_manager = AnalysisManager(game)
analysis_manager.create_analysis()
    
proto_object = analysis_manager.get_protobuf_data()
json_proto_object = analysis_manager.get_json_data()
dataframe = analysis_manager.get_data_frame()

cs = ['pos_x', 'pos_y', 'pos_z']
rot_cs = ['rot_x', 'rot_y', 'rot_z']

ball = dataframe['ball']
ball_df = ball[cs].fillna(-100)

players = proto_object.players
names = [player.name for player in players]

def process_player_df(game) -> List[ReplayPlayer]:
    player_data = []
    for player in names:
        dataframe[player].loc[:, rot_cs] = dataframe[player][rot_cs] / 65536.0 * 2 * 3.14159265
        dataframe[player].loc[:, 'pos_x'] = dataframe[player]['pos_x']
        dataframe[player].loc[:, 'pos_y'] = dataframe[player]['pos_y']
        dataframe[player].loc[:, 'pos_z'] = dataframe[player]['pos_z']
        player_positions = dataframe[player][cs + rot_cs + ['boost_active']].fillna(-100)
        player_data.append(player_positions.values.tolist())
    return player_data

players_data = process_player_df(proto_object)
game_frames = dataframe['game'][['delta', 'seconds_remaining', 'time']].fillna(-100)

print(better_jsonify(ReplayPositions(
    id_=replay_file,
    ball=ball_df.values.tolist(),
    players=players_data,
    colors=[player.is_orange for player in players],
    names=[player.name for player in players],
    frames=game_frames.values.tolist()
)))