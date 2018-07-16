import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import sys
import string
import requests
import datetime
import progressbar
import time

def player_logs_season(first_name, last_name, season):
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
                    col_head.append('is_home')
                elif empt_idx == 1:
                    col_head.append('w/l')
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

                if col == 'is_home':
                    game[col] = ('@' not in txt)
                elif col == 'w/l':
                    game[col] = (txt[0], txt[txt.find("(") + 1:int(txt.find(")"))])
                elif col == 'mp':
                    min_sec = [txt[:txt.find(':')], txt[txt.find(':') + 1:]]
                    game[col] = int(min_sec[0]) * 60 + int(min_sec[1])
                elif col == '+/-':
                    game[col] = int(txt)
                else:
                    game[col] = cell.text
                count += 1
            game['season'] = season
            games.append(game)
        
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
    for season in seasons:
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

print(player_logs_career('Damian', 'Lillard'))
# dame_lillard_2015 = player_logs_season('Damian', 'Lillard','2015')
# print(dame_lillard_2015['+/-'])
        
        


