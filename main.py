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

    def weather_detection(self, temp, humidity, speed_wind, probability): #ключевые параметры
        analysis_weather = []
        if temp > 30:
            analysis_weather.append('На улице очень жарко! Риск перегреться')
        elif 15 <= temp <= 30:
            analysis_weather.append('На улице оптимальная температура')
        elif 0 <= temp < 15:
            analysis_weather.append('На улице прохладно')
        elif -10 <= temp < 0:
            analysis_weather.append('На улице холодно, будь осторожен!')
        else:
            analysis_weather.append('На улице очень холодно! Риск замерзнуть')

        if humidity > 85:
            if temp > 30:
                analysis_weather.append('При такой влажности и температуры есть риск теплового удара')
            elif temp < 0:
                analysis_weather.append('Риск гололеда, будь осторожен')
        elif humidity < 30:
            analysis_weather.append('Низкая влажность. Будь осторожен: есть риск сухости в горле, глазах, носу')

        if speed_wind > 40:
            if probability > 80:
                analysis_weather.append('Сильный ветер и осадки. Возможен ураган')
            else:
                analysis_weather.append('Сильный ветер')

        if probability > 80:
            if temp > 25:
                analysis_weather.append('На улице жарко и высокая вероятность осадков. Будь осторожен, возможен ураган')
            elif temp < 0:
                analysis_weather.append('На улице холодно и высокая вероятность осадков. Возможен гололед и град')
        elif probability > 50:
            analysis_weather.append('Вероятность дождя большая')
        elif probability > 20:
            analysis_weather.append('Возможен дождь')

        for idx, weather_pr in enumerate(analysis_weather):
            print(f'{idx + 1}. {weather_pr}')




api_key = 'Vuea1Za3LttfbsKANvpxf2Nm1yIAoorY'
weather = Weather(api_key)
#weather.get_weather(55.7558, 37.6173) #тестовый запуск на проверку


#тестовые запуски
weather.weather_detection(20, 80, 20, 50)
weather.weather_detection(31, 80, 20, 50)
weather.weather_detection(10, 20, 60, 80)