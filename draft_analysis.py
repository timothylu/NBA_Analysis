from scraping_stuff import *
import numpy as np

def pct_gt(series):
    count = 0
    total = 0
    for s in series:
        total +=1
        if s > 10:
            count +=1

    return count/total

def star(series):
    count = 0
    total = 0
    for s in series:
        total += 1
        if s > 60:
            count += 1
    return count/total

def starter(series):
    count = 0
    total = 0
    for s in series:
        total += 1
        if 60 >= s > 25:
            count +=1
    return count/total

def role_player(series):
    count = 0
    total = 0
    for s in series:
        total += 1
        if 25 >= s > 10:
            count += 1
    return count/total

def bench_warmer(series):
    count = 0
    total = 0
    for s in series:
        total += 1
        if 10 >= s:
            count += 1
    return count/total
    
def print_pct(dec):
    return str(round(dec * 100, 2)) + ' %'

def draft_ranks(year_range, logs = True):
    '''
    make a comparison of draft position to career production
    based off 'surplus' ~ Richard Thaler's model for NFL
       except no comparisons w/ salary -> just draft position
    goal is to analyze which picks have the most `success.` Maybe
    uncover false philosophies when it comes to drafting
    '''
    
    start = year_range[0]
    end = year_range[1]

    drafts = pd.DataFrame()
    bar = progressbar.ProgressBar(maxval=(end - start + 1))
    bar.start()
    bar_count = 1
    for i in range(start, end + 1):
        #print(i)
        bar.update(bar_count)
        bar_count += 1
        if i == start:
            drafts = get_draft(i, logs = False)
        else: 
            drafts = drafts.append(get_draft(i, logs = False))
        time.sleep(3)
    print()

    drafts = drafts[drafts['pk'] <= 60]
    
    picks = drafts.groupby(['pk'])
    return picks['ws'].agg([np.mean, np.std, pct_gt, star, starter, role_player, bench_warmer]).sort_values(by=['mean', 'pct_gt'], ascending = False)


    # sorted_ranks = (drafts.groupby(['pk'])['ws'].mean().reset_index()).sort_values(by = ['ws'], ascending = False)
    # return sorted_ranks[sorted_ranks['pk'] <= 60]


print(draft_ranks((1980, 2007)))