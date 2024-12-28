from datetime import datetime
from tempfile import template

import requests
from time import strftime


parametrs = {
    'appid': 'c1d6d5594713c4801b2bb915c8fa5343',
    'units': 'metric',
    'lang': 'eng'
}

def get_weather_country(city):
    parametrs['q'] = city

    weather = requests.get('http://api.openweathermap.org/data/2.5/forecast?', params=parametrs).json()
    # city = weather['city']['name']
    # timezone = weather['timezone']
    # sunrise = datetime.utcfromtimestamp(weather['sys']['sunrise'] +
    #                                         timezone).strftime('%Y.%m.%d %H.%M.%S')
    # sunset = datetime.utcfromtimestamp(weather['sys']['sunrise'] +
    #                                         timezone).strftime('%Y.%m.%d %H.%M.%S')
    # degree = weather['main']['temp']
    # description = weather[0]['description']
    # wind_speed = weather['wind']['speed']
    return weather


    # except:
    #     return 'Wrong country! Try again'
print(get_weather_country(city='Tashkent'))