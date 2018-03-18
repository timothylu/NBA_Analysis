import goldsberry
import pandas as pd

players = goldsberry.PlayerList(Season='2017-18')
players2017 = pd.DataFrame(players.players())
players2017.head()

lillard_id = players2017.loc[players2017['PLAYERCODE'] == 'damian_lillard']['PERSON_ID']

lillard_game_logs = goldsberry.player.game_logs(lillard_id)
lillard_game_logs_2017 = pd.DataFrame(lillard_game_logs.logs())

print lillard_game_logs_2017
