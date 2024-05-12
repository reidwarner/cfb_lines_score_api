from flask import Flask
from flask_restful import Api, Resource
from scrapers import DataScraper
from utils import SeasonDates

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return ("College sports odds and scores API."
            " Path /odds for current odds."
            " Path /scores for final scores."
            " Use the path /odds/sport or /scores/sport to access three different sports. Valid sports are: "
            " ncaaf, ncaab, mlb."
            )


class Odds(Resource):
    def get(self, sport):
        # Check if in season
        season_date = SeasonDates()
        in_season = season_date.is_in_season(sport)
        if not in_season:
            return f"Sorry. {sport} is not in season."

        # Run the scraper
        url = "https://www.lines.com/betting/" + sport + "/odds"
        scraped = DataScraper(url)
        return scraped.scrape_odds()


class Scores(Resource):
    def get(self, sport):
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



api.add_resource(Odds, "/odds/<sport>")
api.add_resource(Scores, "/scores/<sport>")

if __name__ == "__main__":
    app.run(debug=True)

