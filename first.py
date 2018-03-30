import goldsberry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# gets PER of a player for given player game logs
def getPER(player):
   # FIX LATER
   player['PTS'].mean()

# returns the gamescore for a particular player's game
def gamescore(playerGame):
   p = playerGame
   GmSc = p['PTS'] + 0.4*p['FGM'] - 0.7*p['FGA'] - 0.4*(p['FTA'] - p['FTM']) + 0.7*p['OREB'] + 0.3*(p['REB'] - p['OREB']) + p['STL'] + 0.7*p['AST'] + 0.7*p['BLK'] - 0.4*p['PF'] - p['TOV']
   return GmSc

def TSA(playerGame):
   p = playerGame
   return p['FGA'] + 0.44*p['FTA']

def TSPercent(playerGame):
   p = playerGame
   TSP = p['PTS']/(2*TSA(p))
   return TSP

def getGameLog(playerGame):
   p = playerGame
   gID = p['Game_ID']
   print "looking for " + str(p['MATCHUP']) + " game. ID = " + str(gID)
   gameids = goldsberry.GameIDs()
   gameids2017 = pd.DataFrame(gameids.game_list())
   return gameids2017.ix[gameids2017['GAME_ID'] == gID]

def uPER(playerGame):
   # TO FIX LATER
   p = playerGame

   uPER = 0
   return uPER

def pre_post_ASB_2017_18(playercode):
   first, last = playercode.split('_')
   first = first.title()
   last = last.title()
   

   players = goldsberry.PlayerList(Season='2017-18')
   players2017 = pd.DataFrame(players.players())

   player_id = players2017.loc[players2017['PLAYERCODE'] == playercode]['PERSON_ID']

   team_id = players2017.loc[players2017['PLAYERCODE'] == playercode]['TEAM_ID']

   player_game_logs = goldsberry.player.game_logs(player_id)
   player_game_logs_2017 = pd.DataFrame(player_game_logs.logs())
   player_game_logs_2017['GmSc'] = player_game_logs_2017.apply(lambda row: gamescore (row),axis = 1)
   player_game_logs_2017['TSP'] = player_game_logs_2017.apply(lambda row: TSPercent (row), axis = 1)
   post_all_star = player_game_logs_2017.loc[58:82]
   pre_all_star = player_game_logs_2017.loc[0:57]
   # lgl17 = post_all_star.loc[
   #								(post_all_star['PTS'] > 25)
   #								& (post_all_star['PTS'] < 30)
   #								]

   print getGameLog(player_game_logs_2017.loc[5])

   sortedAfter = post_all_star.sort_values(by=['TSP'])
   sortedBefore = pre_all_star.sort_values(by=['TSP'])

   afterGS = np.array(pd.DataFrame(sortedAfter, columns=['GmSc']))
   afterTSP = np.array(pd.DataFrame(sortedAfter, columns=['TSP']))

   beforeGS = np.array(pd.DataFrame(sortedBefore, columns=['GmSc']))
   beforeTSP = np.array(pd.DataFrame(sortedBefore, columns=['TSP']))
   print afterGS.mean()
   print "\n"
   print beforeGS.mean()
   
   # MAKE A LINE PLOT
   # #######################
   
   # USE FOR A BASIC LINE PLOT
   # scaled_post = (pd.Series(range(1,len(after) + 1)) * len(before)/len(after)).tolist()
   # print afterTSP
   # print afterGS

   # plt.plot(afterTSP,afterGS,beforeTSP,beforeGS)
   # plt.xlabel('True Shooting %')
   # plt.ylabel('GameScore')


   # # MAKE A BOX/WHISKER
   # #######################
   
   # fig, axs = plt.subplots(1,2)

   # axs[0].boxplot(before)
   # axs[0].set_title("Before All-Star Break (PPG)")

   # axs[1].boxplot(after)
   # axs[1].set_title("After All-Star Break (PPG)")
   # axs[1].set_ylim(axs[0].get_ylim())

   # fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.9, hspace =0.4, wspace=0.3)


   # MAKE A HISTOGRAM
   # #####################
   
   fig, axs = plt.subplots(1,2, sharey=True, tight_layout=True)
   
   axs[0].hist(beforeGS, bins=15)
   axs[0].set_title('GameScore Before All-Star Break')
   axs[1].hist(afterGS, bins=15)
   axs[1].set_title('GameScore After All-Star Break')

   plt.savefig('figure.png')

# def pre_post_ASB_2016_17(playercode):
#    #playercode = 'damian_lillard'
   
#    firstName, lastName = playercode.split('_')
#    firstName = firstName.title()
#    lastName = lastName.title()


#    players = goldsberry.PlayerList(Season='2015-16')
#    players = pd.DataFrame(players.players())
#    print players
   # player_id = players2017.loc[(lastName) in players2017['DISPLAY_FIRST_LAST']]['PERSON_ID']
   # #print players2017.loc[players2017['DISPLAY_FIRST_LAST'].contains(lastName)]
   # team_id = players2017.loc[players2017['PLAYERCODE'] == playercode]['TEAM_ID']

   # player_game_logs = goldsberry.player.game_logs(player_id)
   # player_game_logs_2017 = pd.DataFrame(player_game_logs.logs())
   # post_all_star = player_game_logs_2017.loc[58:82]
   # pre_all_star = player_game_logs_2017.loc[0:57]
   # #lgl17 = post_all_star.loc[
   # #                       (post_all_star['PTS'] > 25)
   # #                       & (post_all_star['PTS'] < 30)
   # #                       ]

   # after = np.array(pd.DataFrame(post_all_star, columns=['PTS']))
   # before = np.array(pd.DataFrame(pre_all_star, columns=['PTS']))
   # print after.mean()
   # print "\n"
   # print before.mean()

   # # MAKE A LINE PLOT
   # # #######################
   # #
   # # scaled_post = (pd.Series(range(1,len(after) + 1)) * len(before)/len(after)).tolist()
   # # plt.plot(scaled_post,after,list(range(1, len(before) + 1)), before)


   # # MAKE A BOX/WHISKER
   # #######################
   
   # fig, axs = plt.subplots(1,2)

   # axs[0].boxplot(before)
   # axs[0].set_title("Before All-Star Break (PPG)")

   # axs[1].boxplot(after)
   # axs[1].set_title("After All-Star Break (PPG)")
   # axs[1].set_ylim(axs[0].get_ylim())

   # fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.9, hspace =0.4, wspace=0.3)


   # # MAKE A HISTOGRAM
   # # #####################
   # # 
   # # fig, axs = plt.subplots(1,2, sharey=True, tight_layout=True)
   # #
   # # axs[0].hist(before, bins=4)
   # # axs[1].hist(after, bins=4)

   # plt.savefig('figure.png')

def main():
   pre_post_ASB_2017_18('damian_lillard')


if __name__ == "__main__":
   main()