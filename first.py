import goldsberry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

players = goldsberry.PlayerList(Season='2017-18')
players2017 = pd.DataFrame(players.players())
players2017.head()

lillard_id = players2017.loc[players2017['PLAYERCODE'] == 'damian_lillard']['PERSON_ID']

lillard_game_logs = goldsberry.player.game_logs(lillard_id)
lillard_game_logs_2017 = pd.DataFrame(lillard_game_logs.logs())
post_all_star = lillard_game_logs_2017.loc[58:82]
pre_all_star = lillard_game_logs_2017.loc[0:57]
#lgl17 = post_all_star.loc[
#								(post_all_star['PTS'] > 25)
#								& (post_all_star['PTS'] < 30)
#								]

after = np.array(pd.DataFrame(post_all_star, columns=['PTS']))
before = np.array(pd.DataFrame(pre_all_star, columns=['PTS']))
print after.mean()
print "\n"
print before.mean()

scaled_post = (pd.Series(range(1,len(after) + 1)) * len(before)/len(after)).tolist()

plt.plot(scaled_post,after,list(range(1, len(before) + 1)), before)
plt.show()