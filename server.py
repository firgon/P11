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
MAX_BOOKING = 12


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


def get_club_with(criteria: str, value):
    """Returns first club found where value corresponds to criteria"""
    return [club for club in clubs if club[criteria] == value][0]


def get_club_with_name(name):
    """Returns first club found where name corresponds to name in db
    (shortcut for get_club_with function)"""
    return get_club_with('name', name)


def get_competition_with_name(name):
    """Returns first competition where name corresponds to name in params"""
    return [comp for comp in competitions if comp['name'] == name][0]


class OverbookingError(ValueError):
    """Personnalized class generated when a club try
    to book more places than possible"""

    def __init__(self, available, required):
        self.available = available
        self.required = required

    def __str__(self):
        if self.required > MAX_BOOKING:
            explanation = f"alors que vous ne pouvez en réserver " \
                          f"que {MAX_BOOKING} maximum."
        else:
            explanation = f"alors qu'il n'y en a que " \
                          f"{self.available} disponibles."
        return f"Vous demandez {self.required} places, {explanation}"


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = get_competition_with_name(request.form['competition'])
    club = get_club_with_name(request.form['club'])
    try:
        places_required = int(request.form['places'])
        if places_required <= min(competition['numberOfPlaces'], 12):
            competition['numberOfPlaces'] = \
                int(competition['numberOfPlaces']) - places_required
            flash('Great-booking complete!')
        else:
            raise OverbookingError(competition['numberOfPlaces'],
                                   places_required)
    except OverbookingError() as e:
        flash(e)
    except ValueError():
        flash(f"BAD REQUEST: {request.form['places']} seems to be "
              f"an incorrect value")
    finally:
        return render_template('welcome.html', club=club,
                               competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
