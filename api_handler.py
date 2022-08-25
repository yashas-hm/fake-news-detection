from flask import Flask, request
from flask_restful import Resource, Api
from web_scraper import WebScraper
from ML_Model.fake_news_detector import FactChecker

app = Flask(__name__)
api = Api(app)


class ApiHandler(Resource):
    @staticmethod
    def get():
        try:
            data = request.args.get('webUrl')
            value = WebScraper.economic_times_scraper(data)
            value = FactChecker.check_fact(value)
            return str(value), 200
        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(ApiHandler, "/fakeNewsDetector/search")
