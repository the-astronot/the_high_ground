"""
This script gets data from the National Weather Service and sends it to the database

Author: Max Marshall
Hack RPI 2019
"""
import firebase_admin
from firebase_admin import firestore
import requests
import time
from lxml import html


def get_cities(city_ref):
    cities_data = []
    docs = city_ref.stream()

    for doc in docs:
        cities_data.append((doc.id, doc.to_dict()))
    return cities_data


def get_weather(city_data):
    for item in city_data[1]:
        if item == "Latitude":
            lat = city_data[1]["Latitude"]
        elif item == "Longitude":
            lon = city_data[1]["Longitude"]
        elif item == "Flood":
            flood = city_data[1]["Flood"]

    url = "https://forecast.weather.gov/MapClick.php?lat={}&lon=-{}".format(lat, lon)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    warnings = (tree.xpath('//div[@class="headline-title"]/text()'))
    for warning in warnings:
        if "Flood" in warning:
            print("True")
            flood = True
        else:
            flood = False

    city_data[1]["Flood"] = flood
    new_city_data = city_data

    return new_city_data


def send_weather(c_data):
    for item in c_data:
        new_data_ref = db.collection(u'{}'.format(database)).document(u'{}'.format(item[0]))
        new_data = dict()
        for dict_item in item[1]:
            new_data[u'{}'.format(dict_item)] = u'{}'.format(item[1][dict_item])
        new_data_ref.set(new_data)


cities_data = []
new_cities_data = []
database = "flood alerts"


if __name__ == '__main__':
    cred = firebase_admin.credentials.Certificate("..\\the_high_ground\\keys\\"
                                                  "intricate-yew-257819-firebase-adminsdk-20d4l-42b875fcc5.json")
    firebase_admin.initialize_app(cred)
    db = firebase_admin.firestore.client()

    for x in range(5):
        city_ref = db.collection(u'{}'.format(database))
        cities_data = get_cities(city_ref)
        for city_data in cities_data:
            new_city_data = get_weather(city_data)
            new_cities_data.append(new_city_data)
        send_weather(new_cities_data)
        time.sleep(5)
