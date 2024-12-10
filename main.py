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
        weather_level = 1
        if temp > 30:
            analysis_weather.append('На улице очень жарко! Риск перегреться')
            weather_level = 3
        elif 15 <= temp <= 30:
            analysis_weather.append('На улице оптимальная температура')
            weather_level = 1
        elif 0 <= temp < 15:
            analysis_weather.append('На улице прохладно')
            weather_level = 2
        elif -10 <= temp < 0:
            analysis_weather.append('На улице холодно, будь осторожен!')
            weather_level = 2
        else:
            analysis_weather.append('На улице очень холодно! Риск замерзнуть')
            weather_level = 3

        if humidity > 85:
            if temp > 30:
                analysis_weather.append('При такой влажности и температуры есть риск теплового удара')
                weather_level = 3
            elif temp < 0:
                analysis_weather.append('Риск гололеда, будь осторожен')
                weather_level = max(weather_level, 2)
        elif humidity < 30:
            analysis_weather.append('Низкая влажность. Будь осторожен: есть риск сухости в горле, глазах, носу')
            weather_level = max(weather_level, 2)

        if speed_wind > 40:
            if probability > 80:
                analysis_weather.append('Сильный ветер и осадки. Возможен ураган')
                weather_level = 3
            else:
                analysis_weather.append('Сильный ветер')
                weather_level = max(weather_level, 2)
        elif 20 < speed_wind <= 40:
            analysis_weather.append('На улице ветер')
            weather_level = max(weather_level, 2)

        if probability > 80:
            if temp > 25:
                analysis_weather.append('На улице жарко и высокая вероятность осадков. Будь осторожен, возможен ураган')
                weather_level = 3
            elif temp < 0:
                analysis_weather.append('На улице холодно и высокая вероятность осадков. Возможен гололед и град')
                weather_level = 3
        elif probability > 50:
            analysis_weather.append('Вероятность дождя большая')
            weather_level = max(weather_level, 2)
        elif probability > 20:
            analysis_weather.append('Возможен дождь')
            weather_level = max(weather_level, 1)

        for idx, weather_pr in enumerate(analysis_weather):
            print(f'{idx + 1}. {weather_pr}')

        if weather_level == 3:
            print('Уровень погоды: плохая')
        elif weather_level == 2:
            print('Уровень погоды: умеренная')
        else:
            print('Уровень погоды: нормальная')




api_key = 'Vuea1Za3LttfbsKANvpxf2Nm1yIAoorY'
weather = Weather(api_key)
#weather.get_weather(55.7558, 37.6173) #тестовый запуск на проверку


#тестовые запуски
weather.weather_detection(20, 80, 20, 50)
weather.weather_detection(31, 80, 20, 50)
weather.weather_detection(10, 20, 60, 80)
weather.weather_detection(10, 20, 30, 10)
weather.weather_detection(-17, 20, 60, 80)