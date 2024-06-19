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
SELECT 
    team_name,
    COUNT(*) AS wins
FROM (
    SELECT 
        t.team_long_name AS team_name
    FROM 
        match m
    JOIN 
        team t ON m.home_team_api_id = t.team_api_id
    WHERE 
        m.home_team_goal > m.away_team_goal
    UNION ALL
    SELECT 
        t.team_long_name AS team_name
    FROM 
        match m
    JOIN 
        team t ON m.away_team_api_id = t.team_api_id
    WHERE 
        m.away_team_goal > m.home_team_goal
) AS all_wins
GROUP BY 
    team_name
ORDER BY 
    wins DESC
LIMIT 10;
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df.head().values.tolist())
