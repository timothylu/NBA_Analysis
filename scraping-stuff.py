import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from sklearn import datasets, linear_model
import sys
import string
import requests
import datetime
import progressbar
import time
import matplotlib.pyplot as plt


def league_advanced_summary(year, logs = True):
    if logs:
        print(f'getting advanced stats from {year} ...')
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'
    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text,'lxml')
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'advanced_stats')

    if table:
        table_body = table.find('tbody')

        head = table.find('thead')

        headings = head.find('tr') 

        col_head = []
        for heading in headings.findAll('th'):
            if heading.text == 'Rk':
                pass
            else:
                col_head.append(heading.text.lower())
        

        players = []
        for row in table_body.findAll('tr' and tag.has_attr('id')):
            row_contents = row.findAll('td')
            player = {}
            for i in range(0, len(row_contents)):
                col = col_head[i]

                player[col] = row_contents[i].text
            players.append(player)

        return pd.DataFrame(players)


def get_draft(year, logs = True):
    if logs:
        print(f'getting {year} draft ...')
    url = f'https://www.basketball-reference.com/draft/NBA_{year}.html'
    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text,'lxml')
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == 'stats')

    if table:
        table_body = table.find('tbody')

        head = table.find('thead')

        headings = head.findAll('tr')[1] 

        col_head = []
        for heading in headings.findAll('th'):
            if heading.text == 'Rk':
                pass
            else:
                col_head.append(heading.text.lower())
        

        players = []
        for row in table_body.findAll('tr'):
            # print()
            # input('new row')
            # print()
            row_contents = row.findAll('td')
            player = {}
            for i in range(0, len(row_contents)):
                col = col_head[i]
                # print(col + '\t' + row_contents[i].text)
                # input()
                
                if row_contents[i].has_attr('href'):
                    player[col + '_link'] = row_contents[i].get('href')
                try:
                    player[col] = float(row_contents[i].text)
                except:
                    try:
                        player[col] = int(row_contents[i].text)
                    except:
                        player[col] = row_contents[i].text
            players.append(player)

        return pd.DataFrame(players)

        


def player_logs_season(first_name, last_name, season, logs = True):
    if logs:
        print(f'Getting data from {int(season) - 1}-{season[-2:]} season...')
    games = []
    url = f'https://www.basketball-reference.com/players/' \
        f'{last_name[0]}/{last_name[:5]}{first_name[:2]}01/gamelog/{season}/'.lower()

    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text,"lxml")
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="pgl_basic")

    if table:
        table_body = table.find('tbody')

        head = table.find('thead')

        headings = head.find('tr')

        col_head = []
        empt_idx = 0
        for heading in headings.findAll('th'):
            if heading.text != '\xa0':
                if heading.text == 'Rk':
                    pass
                else:
                    col_head.append(heading.text.lower())
            else:
                if empt_idx == 0:
                    col_head.append('h/a')
                elif empt_idx == 1:
                    col_head.append('w/l')
                    col_head.append('dif')
                else:
                    col_head.append(empt_idx)
                empt_idx += 1

        bar = progressbar.ProgressBar(maxval=len(table_body.findAll(lambda tag: tag.name=='tr' and tag.has_attr('id'))))
        bar.start()
        bar_count = 1
        for row in table_body.findAll(lambda tag: tag.name=='tr' and tag.has_attr('id')):
            bar.update(bar_count)
            bar_count += 1
            count = 0
            game = {}
            for cell in row.findAll('td'):
                col = col_head[count]
                txt = cell.text

                #print(f'{col}\t{txt}')

                if col == 'h/a':
                    game[col] = ('@' not in txt)
                elif col == 'w/l':
                    game[col] = txt[0]
                    count += 1
                    col = col_head[count]
                    game[col] = txt[txt.find("(") + 1:int(txt.find(")"))]
                elif col == 'mp':
                    min_sec = [txt[:txt.find(':')], txt[txt.find(':') + 1:]]
                    game[col] = int(min_sec[0]) * 60 + int(min_sec[1])
                else:
                    try:
                        game[col] = float(txt)
                    except:
                        try:
                            game[col] = int(txt)
                        except:
                            game[col] = txt
                count += 1
            game['season'] = season
            games.append(game)
        print()
        
    return pd.DataFrame(games)

def player_logs_career(first_name, last_name):
    seasons = []
    all_games = pd.DataFrame()
    url = f'https://www.basketball-reference.com/players/' \
        f'{last_name[0]}/{last_name[:5]}{first_name[:2]}01.html'.lower()

    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text,"lxml")
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="per_game")

    table_body = table.find('tbody')

    for row in table_body.findAll(lambda tag: tag.name=='tr' and tag.has_attr('id')):
        data = row.find('th')
        txt = data.find('a').text
        seasons.append(txt[:2]+txt[-2:])
    
    time.sleep(1)
    logs = {}
    first = True

    bar = progressbar.ProgressBar(maxval=len(seasons))
    season_num = 1
    bar.start()
    for season in seasons:
        bar.update(season_num)
        print()
        season_num += 1
        result = player_logs_season(first_name,last_name,season)
        if first:
            all_games = result
            first = False
        else:
            all_games = all_games.append(result)
        #print(result.head())
        time.sleep(1)
    return all_games

def sec_to_mp(sec):
    minutes = int(round(sec/60))
    sec = sec%60
    return f'{minutes}:{sec}'

#now = datetime.datetime.now()

# print(player_logs_career('Mugsy', 'Bogues'))

# col = 'blk'

# lillard_2015 = player_logs_season('Damian', 'Lillard','2018')
# win_pts = lillard_2015.loc[lillard_2015['w/l'] == 'W'][col].values
# win_min = lillard_2015.loc[lillard_2015['w/l'] == 'W'].mp.values
# w_min = win_min/60
# w_pp36 = win_pts/(w_min)
# plt.scatter(w_min, w_pp36, label = 'win', color = 'orange')

# los_pts = lillard_2015.loc[lillard_2015['w/l'] == 'L'][col].values
# los_min = lillard_2015.loc[lillard_2015['w/l'] == 'L'].mp.values
# l_min = los_min/60
# l_pp36 = los_pts/l_min
# plt.scatter(l_min, l_pp36, label = 'loss', color = 'blue')


# fit_w = np.polyfit(w_min, w_pp36, 1)
# fit_w_fn = np.poly1d(fit_w)
# fit_l = np.polyfit(l_min, l_pp36, 1)
# fit_l_fn = np.poly1d(fit_l)

# plt.plot(w_min, fit_w_fn(w_min), color='orange', linewidth=1)
# plt.plot(l_min, fit_l_fn(l_min), color='blue', linewidth=1)

# plt.xlabel('minutes')
# plt.ylabel(f'{col} per 36 ({col}/36)')

# plt.legend(loc='upper left')
# plt.show()


draft_2015 = get_draft(2015)
print(draft_2015[draft_2015['pk'] == 31].player.values[0])
