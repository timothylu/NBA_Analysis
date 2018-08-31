from scraping_stuff import *

def col_to_str(col):
    dict = {
        'ws'   : 'Win-Shares',
        'mp'   : 'Minutes Played',
        'gs'   : 'Games Started',
        'fg'   : 'Field Goals Made',
        'fga'  : 'Field Goals Attempted',
        'fg%'  : 'Field Goal %',
        '3p'   : '3-Pointers Made',
        '3pa'  : '3-Pointers Attempted',
        '3p%'  : '3-Point %',
        'ft'   : 'Free-Throws Made',
        'fta'  : 'Free-Throws Attempted',
        'ft%'  : 'Free-Throw %',
        'orb'  : 'Offensive Rebounds',
        'drb'  : 'Defensive Rebounds',
        'trb'  : 'Total Rebounds',
        'ast'  : 'Assists',
        'stl'  : 'Steals',
        'blk'  : 'Blocks',
        'tov'  : 'Turnovers',
        'pf'   : 'Personal Fouls',
        'pts'  : 'Points',
        'gmsc' : 'GameScore',
        '+/-'  : 'Plus-Minus'
    }
    return dict[col]

def compare_win_loss(first_name, last_name, year, col = 'gmsc', graph=True, per36=False):
    '''
    Compares value of col in wins and losses
    
    Args:
    =====
        * col: a stat to measure differences across
    '''

    # get values in wins
    player_year = player_logs_season(first_name, last_name, year)
    win_pts = player_year.loc[player_year['w/l'] == 'W'][col].values
    win_min = player_year.loc[player_year['w/l'] == 'W'].mp.values
    w_min = win_min/60
    if per36:
        w_pp36 = win_pts/(w_min)
        plt.scatter(w_min, w_pp36, label = 'win', color = 'orange')
    else:
        plt.scatter(w_min, win_pts, label = 'win', color = 'orange')

    # get values in losses
    los_pts = player_year.loc[player_year['w/l'] == 'L'][col].values
    los_min = player_year.loc[player_year['w/l'] == 'L'].mp.values
    l_min = los_min/60
    if per36:
        l_pp36 = los_pts/l_min
        plt.scatter(l_min, l_pp36, label = 'loss', color = 'blue')
    else:
        plt.scatter(l_min, los_pts, label = 'loss', color = 'blue')


    # make lines of fit for values in wins and in losses
    if per36:
        fit_w = np.polyfit(w_min, w_pp36, 1)
        fit_l = np.polyfit(l_min, l_pp36, 1)
    else:
        fit_w = np.polyfit(w_min, win_pts, 1)
        fit_l = np.polyfit(l_min, los_pts, 1)
    fit_w_fn = np.poly1d(fit_w)
    fit_l_fn = np.poly1d(fit_l)

    plt.plot(w_min, fit_w_fn(w_min), color='orange', linewidth=1)
    plt.plot(l_min, fit_l_fn(l_min), color='blue', linewidth=1)

    # set the labeling
    plt.xlabel('minutes')
    if per36:
        plt.ylabel(f'{col} per 36 ({col}/36)')
    else:
        plt.ylabel(f'{col}')

    plt.title(f'Comparing {col_to_str(col)} for {first_name} {last_name} Across Wins/Losses in the {year - 1}-{str(year)[-2:]} Season')

    # configure other graph stuff
    plt.legend(loc='upper left')

    plt.grid(True)

    if graph:
        plt.show()

    return ((w_min, w_pp36), (l_min, l_pp36))
    
    
compare_win_loss('Damian', 'Lillard', 2016, col = 'gmsc', per36=False)