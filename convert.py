
import pandas as pd

df = pd.read_csv("./9ModifiedHomeGames.csv")



new_dates = []
for date in df['span.first']:
    try:
        new_dates.append( pd.to_datetime(date, format='%m/%d/%Y').strftime('%Y-%m-%d'))
    except Exception:
        new_dates.append( date )

df['span.first'] = new_dates


new_dates = []
for date in df['span.last']:
    try:
        new_dates.append( pd.to_datetime(date, format='%m/%d/%Y').strftime('%Y-%m-%d'))
    except Exception:
        new_dates.append( date )

df['span.last'] = new_dates


#df['span.first'] = pd.to_datetime(df["span.first"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
#df['span.last'] = pd.to_datetime(df["span.last"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")


df.to_csv("./9ModifiedHomeGames.csv", index=False, columns=[ 'team.key','park.key','year.key','span.first','span.last','games','openings','attendance' ])



