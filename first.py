import goldsberry
import pandas as pd
import matplotlib.pyplot as plt

players = goldsberry.PlayerList(Season='2017-18')
players2017 = pd.DataFrame(players.players())
players2017.head()

lillard_id = players2017.loc[players2017['PLAYERCODE'] == 'damian_lillard']['PERSON_ID']

lillard_game_logs = goldsberry.player.game_logs(lillard_id)
lillard_game_logs_2017 = pd.DataFrame(lillard_game_logs.logs())
post_all_star = lillard_game_logs_2017.loc[58:82]
#lgl17 = post_all_star.loc[
#								(post_all_star['PTS'] > 25)
#								& (post_all_star['PTS'] < 30)
#								]

ts = pd.DataFrame(lgl17, columns=['PTS'])
print ts
print "\n"
print ts.mean()

ts = ts.plot()
plt.show()