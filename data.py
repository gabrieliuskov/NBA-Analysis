import pandas as pd
from nba_api.stats.static import teams
from datetime import datetime

equipes = teams.get_teams()
teams_final = {}

for i in equipes:
    teams_final[str(i["id"])] = i["full_name"]

today = datetime.now().date()

if today.month < 8:
    dict_season = range(today.year, today.year - 6, -1)
else:
    dict_season = range(today.year + 1, today.year - 5, -1)

dict_season_final = {}

i = 0
for valor in dict_season:
    ano = str(valor-1) + '-' + str(valor)[2:4]
    dict_season_final[ano] = ano


