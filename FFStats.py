import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=['Player','Owner','Pts','Week'])

for year in range(2017, 2018):
    for week in range(1, 17):
        for slot in range(0,24): 
            for si in [0,50]:
                r = requests.get('http://games.espn.com/ffl/leaders', 
                    params={'leagueId': 307565, 'seasonId': year, 
                            'scoringPeriodID': week,
                            'slotCategoryID': slot,
                            'startIndex': si},
                    cookies={'swid': '{B0ECDF40-0753-4789-AA53-26BA42C8AF19}',
                            'espn_s2': 'AECYxtCE1RKLJg1BBuf%2F1QOsqgHluWm3PIwxamdahdUKxwdX6PZYE0LxkUY%2F8ZbA1prlhR65TsEx606AEWJCL3mnJb5z5Vr5ndHwVfJl0Z0Io5lpFuRKqPRqrtzjGm849roUrRYKKStFnGgozqGa3cDKgGg4hEC%2FUy7LIDJbTgkdS0k%2BFpcQbuAFZ4jcP4DQKAjeRjrwWkO9Uvho4EgcdzrrrMMDJGHOM2YYDWRIg4Jp1hEGmYuP%2B2EPEQeMsSf7%2FtOwmY7NPirG7XFh6Cdl8weP'})
                soup = BeautifulSoup(r,'html.parser')
                table = soup.find('table', class_='playerTableTable')
                tdf = pd.read_html(str(table), flavor='bs4')[0]

                tdf = tdf.iloc[2:, [0,2,26]].reset_index(drop=True)
                tdf.columns = ['Player', 'Owner', 'Pts']
                tdf['Pts'] = tdf['Pts'].fillna(0).astype('int')
                tdf['Player'] = tdf['Player'].str.split(',').str[0]  # keep just player name
                tdf['Week'] = week

                df = df.append(tdf)
print('Complete.')