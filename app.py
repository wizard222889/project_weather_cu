from weather_class import Weather
from flask import Flask, request, render_template
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

app = Flask(__name__)
dict_city = dict()
day = ''
dash_app = Dash(__name__, server=app, url_base_pathname='/plot/')
dash_app.layout = html.Div([
    dcc.Dropdown(id='drop',
                 options=[{'label': 'Температура', 'value': 'temp'},
                          {'label': 'Скорость ветра', 'value': 'speed_wind'},
                          {'label': 'Влажность', 'value': 'humidity'},
                          {'label': 'Вероятность осадков', 'value': 'probability'}],
                 value='temp'),
    dcc.Graph(id='graph_weat')
])
@dash_app.callback(Output('graph_weat', 'figure'),
    Input('drop', 'value'))
def graph(param):
    fig = go.Figure()
    translate_ru = {'temp': 'Температура',
                          'speed_wind': 'Скорость ветра',
                          'humidity': 'Влажность',
                          'probability': 'Вероятность осадков'}
    global dict_city, day
    for city, weath in dict_city.items():
        if day == '1day':
            fig.add_trace(go.Bar(
                x=[city],
                y=[weath[0][param]],
                name=f'{translate_ru[param]} в {city}'
            ))
            fig.update_layout(title="Визуализация погоды для городов",
                              xaxis_title='Город',
                              yaxis_title='Значение',
                              showlegend=True,
                              barmode='group',
                              template='plotly_white')
        else:
            fig.add_trace(go.Scatter(
                x=[weath[i]['date'] for i in range(5)],
                y=[weath[i][param] for i in range(5)],
                mode='lines+markers',
                name=f'{translate_ru[param]} в {city}'
            ))
            fig.update_layout(title="Визуализация погоды для городов",
                              xaxis_title='Дата',
                              yaxis_title='Значение',
                              showlegend=True,
                              barmode='group',
                              template='plotly_white')


    return fig
@app.route('/', methods=['GET', 'POST'])
def city_weather():
    global dict_city
    if request.method == 'GET':
        return render_template('weather_html.html')
    else:
        first_point = request.form['first']
        second_point = request.form['second']
        dop_point = request.form
        global day
        day = request.form['day']
        dict_city[first_point] = []
        dict_city[second_point] = []
        for city in dop_point:
            if city[:4] == 'city':
                dict_city[dop_point[city]] = []

        try:
            api_key = 'HcL7JxdZfOgwGa0eVcJHo0omJ6S8P1gU'
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
