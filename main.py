import requests

class Weather:

    api_url = 'http://dataservice.accuweather.com /forecasts/v1/daily/1day/' #ссылка на api

    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, lon, lat):
        try:
            params = {'apikey': self.api_key,
                      'metric': "true"}
            r = requests.get(self.api_url, params=params)
            if r.status_code == 200:
                data = r.json()
                print(data)

        except Exception as error:
            print(f'Произошла неизвестная ошибка: {error}')

api_key = 'ojGASKnNCYYltlryGObfRVaoRkjGCwPe'
weather = Weather(api_key)
weather.get_weather(55.7558, 37.6173)
