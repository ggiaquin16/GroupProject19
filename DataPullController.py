import json
import requests
import pandas as pd
import pymongo as mongo
from config import api_key, mongo_db, mongo_url, mongo_collections, test_mode

client = mongo.MongoClient(mongo_url)
MongoDB = client[mongo_db]
collections = []

if test_mode:
    for collection in mongo_collections:
        MongoDB.drop_collection(collection)
        collections.append(MongoDB[collection])
elif not test_mode:
    for collection in mongo_collections:
        collections.append(MongoDB[collection])


def LoadSalesByYear(api_key, year):
    kiaCarApi = f"https://marketcheck-prod.apigee.net/v2/sales/car?api_key={api_key}&ymm={year}|kia|optima&car_type=new"
    chevyCarApi = f"https://marketcheck-prod.apigee.net/v2/sales/car?api_key={api_key}&ymm={year}|chevrolet|malibu&car_type=new"
    hondaCarApi = f"https://marketcheck-prod.apigee.net/v2/sales/car?api_key={api_key}&ymm={year}|honda|accord&car_type=new"
    toyotaCarApi = f"https://marketcheck-prod.apigee.net/v2/sales/car?api_key={api_key}&ymm={year}|toyota|camry&car_type=new"
    lexusCarApi = f"https://marketcheck-prod.apigee.net/v2/sales/car?api_key={api_key}&ymm={year}|lexus|es&car_type=new"
    mercedesCarApi = f"https://marketcheck-prod.apigee.net/v2/sales/car?api_key={api_key}&ymm={year}|mercedes-benz|s-class&car_type=new"

    responses = []
    apiUrls = [kiaCarApi, chevyCarApi, hondaCarApi,
               toyotaCarApi, lexusCarApi, mercedesCarApi]

    for url in apiUrls:
        response = requests.get(url).json()
        responses.append(response)

    carSales = collections[0]
    for response in responses:
        carSales.insert_one(response)


def LoadPopularCars(api_key):
    newNationalApi = f"https://marketcheck-prod.apigee.net/v2/popular/cars?api_key={api_key}&car_type=new"
    usedNationalApi = f"https://marketcheck-prod.apigee.net/v2/popular/cars?api_key={api_key}&car_type=used"
    caStateApi = f"https://marketcheck-prod.apigee.net/v2/popular/cars?api_key={api_key}&car_type=new&state=CA"
    nyStateApi = f"https://marketcheck-prod.apigee.net/v2/popular/cars?api_key={api_key}&car_type=new&state=NY"
    responses = []
    apiUrls = [newNationalApi, usedNationalApi, caStateApi,
               nyStateApi]

    for url in apiUrls:
        response = requests.get(url).json()
        responses.append(response)

    carPopularity = collections[1]
    for response in responses:
        carPopularity.insert_many(response)
