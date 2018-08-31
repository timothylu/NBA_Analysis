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

headers = {'user-agent' : 'Timothy Lu/University of Washington/timlu@uw.edu'}

def league_advanced_summary(year, logs = True):
    if logs:
        print(f'getting advanced stats from {year} ...')
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'
    page_request = requests.get(url, headers=headers)
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
    page_request = requests.get(url, headers=headers)
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
            if (row.has_attr('class')
                and 'thead' in row.get('class')
                ):
                continue

            for i in range(0, len(row_contents)):
                col = col_head[i]
                tag = row_contents[i]
                val = row_contents[i].text
                # print(col + '\t' + row_contents[i].text)
                # input()

                if tag.has_attr('href'):
                    player[col + '_link'] = tag.get('href')
                if (val == '' 
                    and (col != 'tm' 
                        and col != 'player' 
                        and col != 'college')
                    ):
                    player[col] = 0 
                else:
                    try:
                        player[col] = float(val)
                        if player[col].is_integer():
                            player[col] = int(player[col])
                    except:
                        try:
                            player[col] = int(val)
                        except:
                            player[col] = val
            player['year'] = year
            players.append(player)

        return pd.DataFrame(players)

        


def player_logs_season(first_name, last_name, season, logs = True):
    season = str(season)
    if logs:
        print(f'Getting data from {int(season) - 1}-{season[-2:]} season...')
    games = []
    url = f'https://www.basketball-reference.com/players/' \
        f'{last_name[0]}/{last_name[:5]}{first_name[:2]}01/gamelog/{season}/'.lower()

    page_request = requests.get(url, headers=headers)
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




