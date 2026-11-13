import json
import os
import urllib.request
from cs50 import SQL
from dotenv import load_dotenv


import json
import os
import urllib.request
from cs50 import SQL
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("CFBD_API_KEY")
if not api_key:
    raise RuntimeError("CFBD_API_KEY not set. Add it to your .env file.")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

db = SQL("sqlite:///cfb_database.db")


print("Wiping out old/outdated database entries...")
db.execute("DROP TABLE IF EXISTS teams")


db.execute("DROP TABLE IF EXISTS teams")

db.execute("""
            CREATE TABLE teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT NOT NULL,
                mascot TEXT NOT NULL,
                conference TEXT NOT NULL,
                logo_url TEXT NOT NULL
            )
        """)
url = "https://api.collegefootballdata.com/teams/fbs"

print("Connecting to live CFB data API")
req = urllib.request.Request(url)

req.add_header("Authorization", f"Bearer {api_key}")
req.add_header("User-Agent", "Mozilla/5.0")

try:
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error connecting to API. Verify key string. Details {e}")
    exit(1)



count = 0
for row in data:
    school = row.get("school")
    mascot = row.get("mascot")
    conference = row.get("conference")
    logos = row.get("logos")

    if logos and len(logos) > 0:
        logo_url = logos[0]
    else:
        continue

    if school and mascot and conference:
        db.execute(
            "INSERT INTO teams (school_name, mascot, conference, logo_url) VALUES (?, ?, ?, ?)",
            school,
            mascot,
            conference,
            logo_url
        )
        count += 1

print(f"\n Success! Populated your database with {count} FBS teams!")

