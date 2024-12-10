import requests

class Weather:

    api_url_city = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search' #ссылка на api для определения места
    api_url_weather = 'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/' #для определения погоды
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, lat, lon):
        try:
            params = {'apikey': self.api_key,
                      'q': f'{lat}, {lon}'}
            r = requests.get(self.api_url_city, params=params) #запрос на определения места
            if r.status_code == 200:
                data = r.json()['Key']
                params_weather = {'apikey': self.api_key,
                                  'details': 'true',
                                  'metric': 'true'}
                r_weather = requests.get(self.api_url_weather + data, params=params_weather) # на определения погоды
                if r_weather.status_code == 200:
                    weather_json = r_weather.json()
                    temp = weather_json[0]['Temperature']['Value']
                    humidity = weather_json[0]['RelativeHumidity']
                    speed_wind = weather_json[0]['Wind']['Speed']['Value']
                    probability = weather_json[0]['PrecipitationProbability']
                    print(f'Температура сейчас: {temp}°C')
                    print(f'Влажность: {humidity}%')
                    print(f'Скорость ветра: {speed_wind} км/ч')
                    print(f'Вероятность дождя: {probability}%')
                else:
                    print('Ошибка подключения')
            else:
                print('Ошибка подключения')

        except Exception as error:
            print(f'Произошла неизвестная ошибка: {error}')


api_key = 'Vuea1Za3LttfbsKANvpxf2Nm1yIAoorY'
weather = Weather(api_key)
weather.get_weather(55.7558, 37.6173) #тестовый запуск на проверку
