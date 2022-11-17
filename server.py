import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    """ Loads club from json file : clubs.json """
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    """ Loads competitions from json file : competitions.json """
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']][
        0]
    return render_template('welcome.html', club=club,
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = get_club_with_name(club)
    found_competition = get_competition_with_name(competition)

    if found_club and found_competition:
        return render_template('booking.html', club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


def get_competition_with_name(name):
    return [comp for comp in competitions if comp['name'] == name][0]


def get_club_with_name(name):
    return [club for club in clubs if club['name'] == name][0]


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = get_competition_with_name(request.form['competition'])
    club = get_club_with_name(request.form['club'])
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
