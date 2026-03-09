import pandas as pd
import sqlite3
import json

# Step 1: Load JSON safely
with open("jobs.json", "r", encoding="utf-8") as f:
    text = f.read()

# find the last valid JSON array
start = text.rfind('[')
data = json.loads(text[start:])

df = pd.DataFrame(data)

# Step 2: Clean data
df['title'] = df['title'].str.strip()
df['company'] = df['company'].str.strip()
df['location'] = df['location'].str.strip()
df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
df['salary'] = df['salary'].fillna('Not Specified')
df['apply_link'] = df['apply_link'].str.strip()

# remove duplicates
df = df.drop_duplicates(subset=['title', 'company', 'location'])

# Step 3: Save cleaned JSON
df.to_json("clean_jobs.json", orient="records", indent=2)

# Step 4: Save to SQLite
conn = sqlite3.connect("jobs.db")
df.to_sql("jobs", conn, if_exists="replace", index=False)
conn.close()

print("Data cleaned and saved successfully!")