# FBS College Football Logo Quiz

**CS50x Final Project**
**Video Demo:** [Video Demo URL Here](https://youtu.be/zXDxvJ1HGiE?si=Wy7H2k3D0W5gudJ5)

## Overview
The **FBS College Football Logo Quiz** is a responsive, web-based trivia application that tests users' knowledge of all 138 NCAA Division I Football Bowl Subdivision (FBS) programs. Players can choose between a quick **10-question sprint** or an **endurance 138-question challenge** covering every current FBS team (excluding FCS, Division II, and Division III schools).

## Key Features
* **Two Game Modes:** Offers a 10-question quick play mode and a full 138-question marathon mode.
* **Searchable Type-Ahead Dropdown:** Combines a dropdown menu with live text filtering across all 138 teams.
Because schools often go by multiple aliases (e.g., *Texas*, *UT*, *University of Texas*, or *University of Texas at Austin*), a searchable dropdown prevents unfair penalties caused by strict string-matching or naming conventions.
* **Randomized Question Order:** Dynamically shuffles teams and logos on every playthrough so that no two quizzes are the same.
* **Live Score & Session Tracking:** Uses Flask stateful cookie sessions to track user progress, right answers, and wrong answers throughout an active game.
* **Automated API Data Pipeline:** Uses a custom `seed.py` script to authenticate with a Bearer token and populate the local SQL database with live FBS team and logo data.

## Tech Stack
* **Backend:** Python, Flask, SQL (SQLite)
* **Frontend:** HTML, CSS, Jinja2, JSON
* **Data Source:** [CollegeFootballData.com API](https://collegefootballdata.com/)

## Design & Engineering Decisions
* **Selecting the Data Source:** Early in development, I evaluated ESPN's open API endpoints, which proved overly complex and tedious for extracting clean, FBS-only rosters. Switching to the **CollegeFootballData.com API** provided a cleaner, structured JSON schema that reliably filters strictly for current FBS teams.
* **Handling Logo Asset Variations:** Each team object in the API returns an array of multiple logo URLs in inconsistent orders—some featuring only a mascot or symbol, and others including school wordmarks (such as UCLA). Rather than manually curating and hosting 138 separate image files locally, I programmatically indexed the primary image (`logos[0]`) for each team. This kept the pipeline automated and scalable while naturally mixing a few accessible wordmark questions into the quiz.

## Project Structure
* `app.py` — Main Flask application handling routes, `GET`/`POST` quiz logic, randomization, and session state management.
* `seed.py` — Data pipeline script that sends authenticated requests to the CollegeFootballData API and seeds the SQL database.
* `templates/` — Jinja2 HTML templates for the home screen, quiz interface, and score display.
* `static/` — Custom CSS stylesheets for responsive layout and design.

## Setup & Installation
1. Clone this repository to your local machine.
2. Obtain a free API key from [CollegeFootballData.com](https://collegefootballdata.com/).
3. Set your API key as an environment variable (or add it to your local `.env` file).
4. Run `python seed.py` to fetch the latest FBS teams and populate the database.
5. Run `flask run` and open the local server URL in your browser.

## Future Improvements
* **Post-Quiz Summary Page:** Add a detailed breakdown screen at the end of each quiz showing every logo presented, the user's submitted guess, and whether each answer was correct or incorrect.
* **Conference Filtering:** Allow users to filter quizzes by specific conferences (e.g., SEC, Big Ten, ACC, Big 12).
