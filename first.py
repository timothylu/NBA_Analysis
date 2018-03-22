import goldsberry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def pre_post_ASB_2017(playercode):
   #playercode = 'damian_lillard'
   

   players = goldsberry.PlayerList(Season='2017-18')
   players2017 = pd.DataFrame(players.players())
   players2017.head()

   player_id = players2017.loc[players2017['PLAYERCODE'] == playercode]['PERSON_ID']

   player_game_logs = goldsberry.player.game_logs(player_id)
   player_game_logs_2017 = pd.DataFrame(player_game_logs.logs())
   post_all_star = player_game_logs_2017.loc[58:82]
   pre_all_star = player_game_logs_2017.loc[0:57]
   #lgl17 = post_all_star.loc[
   #								(post_all_star['PTS'] > 25)
   #								& (post_all_star['PTS'] < 30)
   #								]

   after = np.array(pd.DataFrame(post_all_star, columns=['PTS']))
   before = np.array(pd.DataFrame(pre_all_star, columns=['PTS']))
   print after.mean()
   print "\n"
   print before.mean()

   # MAKE A LINE PLOT
   # #######################
   #
   # scaled_post = (pd.Series(range(1,len(after) + 1)) * len(before)/len(after)).tolist()
   # plt.plot(scaled_post,after,list(range(1, len(before) + 1)), before)


   # MAKE A BOX/WHISKER
   #######################
   
   fig, axs = plt.subplots(1,2)

   axs[0].boxplot(before)
   axs[0].set_title("Before All-Star Break (PPG)")

   axs[1].boxplot(after)
   axs[1].set_title("After All-Star Break (PPG)")
   axs[1].set_ylim(axs[0].get_ylim())

   fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.9, hspace =0.4, wspace=0.3)


   # MAKE A HISTOGRAM
   # #####################
   # 
   # fig, axs = plt.subplots(1,2, sharey=True, tight_layout=True)
   #
   # axs[0].hist(before, bins=4)
   # axs[1].hist(after, bins=4)

   plt.savefig('figure.png')


def main():
   pre_post_ASB_2017('damian_lillard')

if __name__ == "__main__":
   main()