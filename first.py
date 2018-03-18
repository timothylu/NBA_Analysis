import goldsberry
import pandas as pd
import matplotlib.pyplot as plt

players = goldsberry.PlayerList(Season='2017-18')
players2017 = pd.DataFrame(players.players())
players2017.head()

lillard_id = players2017.loc[players2017['PLAYERCODE'] == 'damian_lillard']['PERSON_ID']

lillard_game_logs = goldsberry.player.game_logs(lillard_id)
lillard_game_logs_2017 = pd.DataFrame(lillard_game_logs.logs())

lgl17 = lillard_game_logs_2017.loc[(lillard_game_logs_2017['PTS'] > 25) & (lillard_game_logs_2017['PTS'] < 30)]

ts = pd.DataFrame(lgl17, columns=['FGA'])
print ts.mean()

ts = ts.plot()
plt.show()