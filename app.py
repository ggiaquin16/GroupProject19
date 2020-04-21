import pandas as pd
from flask import Flask, jsonify, request, url_for, render_template
from flask_pymongo import PyMongo
from flask_googlecharts import GoogleCharts, BarChart
from flask_cors import CORS
from collections import defaultdict

# Flask init
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'CarPopularity'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/CarPopularity'

mongo = PyMongo(app)
CORS(app)

GoogleCharts(app)


@app.route("/")
def welcome():
    return (
        f"Available endpoints:<br/>"
        f"/GetCarStatsByYear:<br/>"
        f"/PopularCars:<br/>"
    )


@app.route("/GetCarStatsByYear", methods=['GET', 'POST'])
def GetCarStatsByYear():
    carMongoList = list(mongo.db.CarSalesByYear.find())
    carSalesDF = pd.DataFrame(carMongoList)
    carSalesDF = carSalesDF[['year', 'make', 'model', 'count']]
    carSalesDict = carSalesDF.to_dict(orient='records')
    return jsonify(carSalesDict)


@app.route("/GetPopularCars", methods=['GET', 'POST'])
def GetPopularCars():
    carMongoList = list(mongo.db.PopularcarsByRegion.find())
    carPopularityDF = pd.DataFrame(carMongoList)
    carPopularityDF = carPopularityDF[['country', 'state', 'make', 'model', 'count']]
    carPopularityDict = carPopularityDF.to_dict(orient='records')
    return jsonify(carPopularityDict)


if __name__ == '__main__':
    app.run(debug=True)
