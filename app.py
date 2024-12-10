from weather_class import Weather
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def city_weather():
    if request.method == 'GET':
        return render_template('weather_html.html')
    else:
        first_point = request.form['first']
        second_point = request.form['second']
        dop_point = request.form
        day = request.form['day']
        dict_city = dict()
        dict_city[first_point] = []
        dict_city[second_point] = []
        for city in dop_point:
            if city[:4] == 'city':
                dict_city[dop_point[city]] = []

        try:
            api_key = 'lEuBYWRiUMyUNqDje0pym3UcVNWAXnBq'
            weather = Weather(api_key=api_key)
            for city in dict_city:
                if day == '1day':
                    code_point = weather.get_city_code(city)
                    weather_point = weather.get_weather(code_point, day=day)
                    analysis = weather.weather_detection(weather_point['temp'], weather_point['humidity'],
                                                                         weather_point['speed_wind'], weather_point['probability'])
                    weather_point['weather'] = '. '.join(analysis[:-1])
                    weather_point['level'] = analysis[-1]
                    dict_city[city].append(weather_point)
                elif day == '5day':
                    code_point = weather.get_city_code(city)
                    weather_point = weather.get_weather(code_point, day=day)
                    for dates in weather_point:
                        analysis = weather.weather_detection(dates['temp'], dates['humidity'],
                                                             dates['speed_wind'], dates['probability'])
                        dates['weather'] = '. '.join(analysis[:-1])
                        dates['level'] = analysis[-1]
                        dict_city[city].append(dates)

            return render_template('weather_post_html.html', city_weather=dict_city)
        except (ConnectionError, ValueError, PermissionError, Exception) as error:
            return render_template('error.html', error=str(error))


if __name__ == '__main__':
    app.run(debug=True)
