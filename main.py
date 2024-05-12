from flask import Flask
from scrapers import DataScraper
from utils import SeasonDates

app = Flask(__name__)


@app.route('/')
def home():
    return ("College sports odds and scores API."
            "Use the path /sport to access three different sports. Valid sports are: "
            "ncaaf, ncaab, mlb."
            " Path /sport/odds for current odds."
            " Path /sport/scores for final scores.")


@app.route('/<sport>/odds')
def get_odds(sport):

    # Check if in season
    season_date = SeasonDates()
    in_season = season_date.is_in_season(sport)
    if not in_season:
        return f"Sorry. {sport} is not in season."

    # Run the scraper
    url = "https://www.lines.com/betting/" + sport + "/odds"
    scraped = DataScraper(url)
    return scraped.scrape_odds()


@app.route('/<sport>/scores')
def get_scores(sport):

    # Check if in season
    season_date = SeasonDates()
    in_season = season_date.is_in_season(sport)
    if not in_season:
        return f"Sorry. {sport} is not in season."

    # Set correct URL
    url = "https://www.lines.com/betting/" + sport + "/odds"

    # Run the scores scraper
    scraped = DataScraper(url)
    return scraped.scrape_scores()


if __name__ == "__main__":
    app.run(debug=True)

