"""
This script gets data from the National Weather Service and sends it to the database

Author: Max Marshall
Hack RPI 2019
"""
from lxml import html
import requests
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_cities(city_ref):
    cities_data = []
    docs = city_ref.stream()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        cities_data.append((doc.id, doc.to_dict()))
    return cities_data


def get_weather(city_data):
    url = "https://forecast.weather.gov/MapClick.php?lat=18.464&lon=-66.1128".format()
    page = requests.get(url)
    tree = html.fromstring(page.content)

    warnings = (tree.xpath('//div[@class="headline-title"]/text()'))
    for warning in warnings:
        if "Flood" in warning:
            print("True")

    return new_city_data


def send_weather(c_data):
    pass


cities_data = []
new_cities_data = []


if __name__ == '__main__':
    cred = firebase_admin.credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': "intricate-yew-257819"
    })
    db = firestore.client()

    for x in range(5):
        city_ref = db.collection(u'flood alerts')
        cities_data = get_cities(city_ref)
        for city_data in cities_data:
            new_city_data = get_weather(city_data)
        send_weather(new_cities_data)
        time.sleep(5)
