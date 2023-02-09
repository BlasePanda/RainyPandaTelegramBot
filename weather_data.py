import geocoder as geocoder
import requests
from datetime import date
from geopy.geocoders import Nominatim




def access_last_city():
    with open("country_codes.txt", "r") as myfile:
        return myfile.readlines()[-1]




def lat_and_lon():
    geolocator = Nominatim(user_agent="geoapiExercises")
    university = access_last_city()
    address = geolocator.geocode(university)
    lat = address.latitude
    lon = address.longitude
    return lat, lon


# in this block we split data into time rain and weather codes
def weather_codes():
    # this block gets data from api
    r = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat_and_lon()[0]}&longitude={lat_and_lon()[1]}&hourly=rain,weathercode&start_date={date.today()}&end_date={date.today()}&current_weather")
    r_data = r.json()
    hourly = r_data["hourly"]
    # This splits time,rain and codes
    hourly_time = hourly["time"]
    hourly_rain = hourly["rain"]
    hourly_code = hourly["weathercode"]
    # combine time and rain into dictionary
    combined_rain = {k: v for k, v in zip(hourly_time, hourly_rain)}
    # combine time and weather codes into dictionary
    combined_codes = {k: v for k, v in zip(hourly_time, hourly_code)}
    return combined_rain, combined_codes





