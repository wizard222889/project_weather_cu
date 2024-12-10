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
        try:
            api_key = 'Vuea1Za3LttfbsKANvpxf2Nm1yIAoorY'
            weather = Weather(api_key=api_key)
            code_first_point = weather.get_city_code(first_point)
            weather_first_point = weather.get_weather(code_first_point)
            temp1 = weather_first_point['temp']
            hum1 = weather_first_point['humidity']
            speed_wind1 = weather_first_point['speed_wind']
            probability1 = weather_first_point['probability']
            analysis1 = weather.weather_detection(temp1, hum1, speed_wind1, probability1)
            anaysis_weather1 = '. '.join(analysis1[:-1])
            level_weather1 = analysis1[-1]

            code_second_point = weather.get_city_code(second_point)
            weather_second_point = weather.get_weather(code_second_point)
            temp2 = weather_second_point['temp']
            hum2 = weather_second_point['humidity']
            speed_wind2 = weather_second_point['speed_wind']
            probability2 = weather_second_point['probability']
            analysis2 = weather.weather_detection(temp2, hum2, speed_wind2, probability2)
            anaysis_weather2 = '. '.join(analysis2[:-1])
            level_weather2 = analysis2[-1]

            return render_template('weather_post_html.html', temp1=temp1,
                                   hum1=hum1, speed1=speed_wind1, pr1=probability1, weather1=anaysis_weather1,
                                   level1=level_weather1, hum2=hum2, speed2=speed_wind2, pr2=probability2,
                                   weather2=anaysis_weather2,
                                   level2=level_weather2)

        except (ConnectionError, ValueError, PermissionError, Exception) as error:
            return render_template('error.html', error=str(error))


if __name__ == '__main__':
    app.run(debug=True)
