from flask import Flask, jsonify
from scrapers import DataScraper

app = Flask(__name__)


@app.route('/')
def home():
    return ("College sports odds and scores API."
            " Path /odds for current odds."
            " Path /scores for final scores.")


@app.route('/ncaam/odds')
def get_odds():
    # Check if in season

    # Run the scraper
    url = "https://www.lines.com/betting/mlb/odds"
    ncaam_scrape = DataScraper(url)
    return ncaam_scrape.scrape_odds()


@app.route('/ncaam/scores')
def get_scores():
    # Check if in season

    # Run the scores scraper
    url = "https://www.lines.com/betting/ncaab/odds"
    ncaam_scrape = DataScraper(url)
    return ncaam_scrape.scrape_scores()


if __name__ == "__main__":
    app.run(debug=True)

