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
app.config.from_object('config')

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = get_club_with('email', request.form['email'])
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


def get_object_with(objects: list[dict], criteria: str, value: str) -> dict:
    """Return first club or competition with value corresponding to criteria"""
    for element in objects:
        if criteria in element.keys() and element[criteria] == value:
            return element
    else:
        return None


def get_club_with(criteria: str, value):
    """short cut for getting a club with get_object_with function"""
    return get_object_with(clubs, criteria, value)


def get_club_with_name(name):
    """Returns first club found where name corresponds to name in db
    (shortcut for get_club_with function)"""
    return get_club_with('name', name)


def get_competition_with_name(name):
    """short cut for getting a competition with get_object_with function"""
    return get_object_with(competitions, 'name', name)


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
