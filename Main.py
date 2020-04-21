from config import years_data, api_key
from DataPullController import LoadSalesByYear, LoadPopularCars

for year in years_data:
    LoadSalesByYear(api_key, year)

LoadPopularCars(api_key)
