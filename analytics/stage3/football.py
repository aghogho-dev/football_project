import os
import pandas as pd
import urllib.request
import zipfile
import sqlite3

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

query = """
SELECT tt.team_long_name, SUM(tt.points) points
FROM (

SELECT mm.team_long_name, mm.home_team_api_id, mm.home_team_goal, mm.away_team_goal,
CASE 
	WHEN mm.home_team_api_id = 8654 AND mm.home_team_goal > mm.away_team_goal THEN 3
	WHEN mm.home_team_api_id = 8654 AND mm.home_team_goal < mm.away_team_goal THEN 0
	WHEN mm.home_team_api_id != 8654 AND mm.home_team_goal < mm.away_team_goal THEN 3
	WHEN mm.home_team_api_id != 8654 AND mm.home_team_goal > mm.away_team_goal THEN 0
	WHEN mm.home_team_goal = mm.away_team_goal THEN 1
END AS points
FROM
(
    SELECT *
    FROM match m
    LEFT JOIN team t ON t.team_api_id = m.home_team_api_id
    WHERE t.team_short_name = "WHU"

    UNION ALL

    SELECT *
    FROM match m
    LEFT JOIN team t ON t.team_api_id = m.away_team_api_id
    WHERE t.team_short_name = "WHU"
) AS mm
WHERE mm.season = "2014/2015" 
) AS tt;
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(*(df.head().values.tolist()))
