import os
import pandas as pd
import urllib.request
import zipfile
import sqlite3
import matplotlib.pyplot as plt

link = "https://www.dropbox.com/scl/fi/3stdjxxmk3gimkwmy6rkp/database.zip?rlkey=2yhgx5fpbimbx582uy076wesi&st=hvchgqj5&dl=1"
data_dir = os.path.join("..", "data")
data_path = os.path.join(data_dir, "database.zip")
extracted_path = os.path.join(data_dir, "database")

try:
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(data_path):
        urllib.request.urlretrieve(link, data_path)
        print(f"File downloaded and saved to {data_path}")

    if not os.path.exists(extracted_path):
        with zipfile.ZipFile(data_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_path)
        print("File unzipped to the data directory")

except Exception as e:
    print(f"An error occurred: {e}")


db_path = os.path.join(extracted_path, "database.sqlite")

conn = sqlite3.connect(db_path)

def get_query(apiID, teamNameShort, seasonID):
    query = f"""
    SELECT tt.team_long_name, SUM(tt.points) points, tt.season
    FROM (

    SELECT mm.team_long_name, mm.home_team_api_id, mm.home_team_goal, mm.away_team_goal, mm.season,
    CASE 
    	WHEN mm.home_team_api_id = {apiID} AND mm.home_team_goal > mm.away_team_goal THEN 3
    	WHEN mm.home_team_api_id = {apiID} AND mm.home_team_goal < mm.away_team_goal THEN 0
    	WHEN mm.home_team_api_id != {apiID} AND mm.home_team_goal < mm.away_team_goal THEN 3
    	WHEN mm.home_team_api_id != {apiID} AND mm.home_team_goal > mm.away_team_goal THEN 0
    	WHEN mm.home_team_goal = mm.away_team_goal THEN 1
    END AS points
    FROM
    (
        SELECT *
        FROM match m
        LEFT JOIN team t ON t.team_api_id = m.home_team_api_id
        WHERE t.team_short_name = "{teamNameShort}"

        UNION ALL

        SELECT *
        FROM match m
        LEFT JOIN team t ON t.team_api_id = m.away_team_api_id
        WHERE t.team_short_name = "{teamNameShort}"
    ) AS mm
    WHERE mm.season = "{seasonID}" 
    ) AS tt;
    """
    return query


result = []

seasons = ["2013/2014", "2014/2015", "2015/2016"]

for season in seasons:

    result.append(pd.read_sql_query(get_query(8654, "WHU", season), conn))
    result.append(pd.read_sql_query(get_query(9826, "CRY", season), conn))

df = pd.concat(result)

conn.close()

teams = df.values.tolist()

print(*teams)

team_names = [entry[0] for entry in teams]
points = [entry[1] for entry in teams]
seasons = [entry[2] for entry in teams]

unique_seasons = sorted(list(set(seasons)))
unique_teams = sorted(list(set(team_names)))

data_by_team = {team: {season: 0 for season in unique_seasons} for team in unique_teams}
for entry in teams:
    team, point, season = entry
    data_by_team[team][season] = point

fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.2
index = range(len(unique_teams))

for i, season in enumerate(unique_seasons):
    season_points = [data_by_team[team][season] for team in unique_teams]
    ax.bar([p + i * bar_width for p in index], season_points, bar_width, label=season)

ax.set_xlabel('Teams')
ax.set_ylabel('Points')
ax.set_title('Points by Teams across Different Seasons')
ax.set_xticks([p + bar_width for p in index])
ax.set_xticklabels(unique_teams)
ax.yaxis.set_visible(False)
ax.legend(title='Seasons')
plt.xticks(rotation=0)

plt.show()


