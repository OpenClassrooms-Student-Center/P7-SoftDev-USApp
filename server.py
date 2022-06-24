from flask import Flask, flash, redirect, render_template, request, session, url_for

from provider import get_clubs, get_competitions

app = Flask(__name__)
app.secret_key = "something_special"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    clubs = get_clubs()
    email = request.form["email"]

    club = [item for item in clubs if item["email"] == email][0]
    session["club"] = club

    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    club = session["club"]
    competitions = get_competitions()

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>")
def book(competition):
    club = session["club"]

    competitions = get_competitions()
    matching_comps = [comp for comp in competitions if comp["name"] == competition]

    found_competition = matching_comps[0]

    if found_competition:
        return render_template("booking.html", club=club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for("summary"))


@app.route("/book", methods=["POST"])
def book_spots():
    club = session["club"]
    competitions = get_competitions()

    matching_comps = [
        comp for comp in competitions if comp["name"] == request.form["competition"]
    ]

    competition = matching_comps[0]

    spots_required = int(request.form["spots"])
    competition["spotsAvailable"] = int(competition["spotsAvailable"]) - spots_required
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    del session["club"]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
