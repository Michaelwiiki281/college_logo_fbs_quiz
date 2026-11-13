from flask import Flask, render_template, request, session, redirect
from cs50 import SQL
import random


app = Flask(__name__)

app.secret_key = "fbs_quiz_secret_key_123"

db = SQL("sqlite:///cfb_database.db")

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/start")
def start():
    mode = request.args.get("mode")

    all_fbs_teams = db.execute("SELECT id FROM teams ORDER BY RANDOM()")
    max_teams = len(all_fbs_teams)

    if mode not in ["10", str(max_teams)]:
        return redirect("/")

    limit = int(mode)

    session["quiz_pool"] = [team["id"] for team in all_fbs_teams[:limit]]
    session["total_questions"] = limit
    session["current_index"] = 0
    session["score"] = 0

    return redirect("/quiz")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "quiz_pool" not in session or session["current_index"] >= session["total_questions"]:
        return redirect("/")

    pool = session["quiz_pool"]
    idx = session["current_index"]
    correct_team_id = pool[idx]

    #extract the exact target team's data row from db
    correct_team = db.execute("SELECT * FROM teams WHERE id = ?", correct_team_id)[0]

    #user submits answer
    if request.method == "POST":
        user_guess = request.form.get("answer")

        if user_guess == correct_team["school_name"]:
            session["score"] += 1

        session["current_index"] += 1

        #check to see if there's any question left or to proceed
        if session["current_index"] >= session["total_questions"]:
            return render_template(
                "results.html",
                score=session["score"],
                total=session["total_questions"]
            )

        return redirect("/quiz")

    else:
        all_teams = db.execute("SELECT school_name FROM teams ORDER BY school_name ASC")

        return render_template(
            "quiz.html",
            team=correct_team,
            all_teams=all_teams,
            current_num= idx + 1,
            total_num=session["total_questions"]
        )

if __name__ == "__main__":
    app.run(debug=True)
