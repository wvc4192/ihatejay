import requests
import pandas
import json

scores = {}
for year in range(2016, 2019):
    for week in range(1, 17):
        r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard', 
            params={'leagueId': 307565, 'seasonId': year, 'matchupPeriodId': week},
            cookies={'swid': '{B0ECDF40-0753-4789-AA53-26BA42C8AF19}',
                    'espn_s2': 'AECYxtCE1RKLJg1BBuf%2F1QOsqgHluWm3PIwxamdahdUKxwdX6PZYE0LxkUY%2F8ZbA1prlhR65TsEx606AEWJCL3mnJb5z5Vr5ndHwVfJl0Z0Io5lpFuRKqPRqrtzjGm849roUrRYKKStFnGgozqGa3cDKgGg4hEC%2FUy7LIDJbTgkdS0k%2BFpcQbuAFZ4jcP4DQKAjeRjrwWkO9Uvho4EgcdzrrrMMDJGHOM2YYDWRIg4Jp1hEGmYuP%2B2EPEQeMsSf7%2FtOwmY7NPirG7XFh6Cdl8weP'})
        scores[(str(year)+'-'+str(week))] = r.json()

print(json.dumps(scores, indent=4))
data = json.dumps(scores, indent=4)
with open("scores.json","w") as f: 
    f.write(data)

df=[]
for key in scores:
    temp = scores[key]['scoreboard']['matchups']
    for match in temp:
        df.append([key,
            scores[key]['metadata']['seasonId'],
            scores[key]['scoreboard']['matchupPeriodId'],
            match['teams'][0]['team']['teamAbbrev'],
            match['teams'][1]['team']['teamAbbrev'],
            match['teams'][0]['teamId'],
            match['teams'][1]['teamId'],
            match['teams'][0]['score'],
            match['teams'][1]['score'],
            scores[key]['scoreboard']['dateFirstProGameOfScoringPeriod']])


df = pandas.DataFrame(df, columns=['WeekID','Year','Period','Team','Opp','TeamID','OppID','Score1', 'Score2','Date'])
print(df)

df = (df[['WeekID','Year','Period','Team','TeamID','Score1','Date']]
    .rename(columns={'Score1': 'Score'})
    .append(df[['WeekID','Year','Period','Opp','OppID','Score2','Date']]
        .rename(columns={'Opp': 'Team','OppID': 'TeamID','Score2': 'Score'}))
    )
df.to_csv("Scores.csv")