import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def cfb_lines_scores_api():

    # Web Scraper for upcoming week of games
    url = "https://www.lines.com/betting/ncaaf/odds/best-line/0?week=5"
    soup = requests.get(url)
    doc = BeautifulSoup(soup.text, "html.parser")

    # odds is a list with a bunch of the betting values staggered in the following way: P/S away, P/S payout away, P/S home,
    # P/S payout home, etc.
    odds = doc.find_all('div', {'class': "odds-list-val"})
    teams = doc.find_all('div', {'class': "odds-list-team-title"})
    game_date_times = doc.find_all('div', {'class': "odds-list-section-title"})

    # Loop through to establish all of our variable and add them to the database
    data_dict = {}
    j = 0
    k = 0

    for i in range(0, len(odds), 6):

        # gets team (index 0) and record (index -1)
        team_away = teams[j].text.strip()[:-6].strip()
        team_home = teams[j + 1].text.strip()[:-6].strip()
        game = f'{team_away} vs. {team_home}'
        game_time = game_date_times[k].text.strip()
        j += 2
        k += 1

        ps_away = odds[i].text.rsplit('(')
        ps_line_away = ps_away[0].strip()
        ps_payout_away = "(" + ps_away[1].strip()

        ps_home = odds[i + 1].text.rsplit('(')
        ps_line_home = ps_home[0].strip()
        ps_payout_home = "(" + ps_home[1].strip()

        ou_away = odds[i + 2].text.rsplit('(')
        ou_line_away = ou_away[0].strip()
        ou_payout_away = "(" + ou_away[1].strip()

        ou_home = odds[i + 3].text.rsplit('(')
        ou_line_home = ou_home[0].strip()
        ou_payout_home = "(" + ou_home[1].strip()

        ml_away = odds[i + 4].text
        ml_home = odds[i + 5].text

        data_dict[game] = {'date and time': game_time,
                           'away team': team_away,
                           'home team': team_home,
                           'spread away': ps_line_away,
                           'spread away payout': ps_payout_away,
                           'spread home': ps_line_home,
                           'spread home payout': ps_payout_home,
                           'total points away': ou_line_away,
                           'total points away payout': ou_payout_away,
                           'total points home': ou_line_home,
                           'total points home payout': ou_payout_home,
                           'money line away': ml_away,
                           'money line home': ml_home,
                           }
    return jsonify(data_dict)


if __name__ == "__main__":
    app.run(debug=True)

