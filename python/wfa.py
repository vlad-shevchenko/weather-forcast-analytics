import random
from itertools import groupby
from collections import deque
import itertools
import pymysql as mysql
import plotly
import plotly.graph_objs as go


def moving_average(iterable, n):
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / n


def scatter(data, groupByAttrName, groupByAttrValue, xAxisAttrName, attrName, maPeriod, processPoints):
    rows = list(map(processPoints, filter(lambda x: x[groupByAttrName] == groupByAttrValue, data)))
    forecastPeriods = list(map(lambda r: r[xAxisAttrName], rows))[maPeriod - 1:len(rows)]
    values = list(moving_average(list(map(lambda r: abs(r[attrName]), rows)), maPeriod))

    return go.Scatter(
        x=forecastPeriods,
        y=values,
        mode='lines+markers',
        name=groupByAttrValue
    )


def plot(data, plotTitle, groupByAttrName, xAxisAttrName, yAxisAttrName, xAxisTitle, yAxisTitle, maPeriod):
    def postProcessPoints(r):
        r2 = {**r}
        rnd = random.random() + 1
        r2[yAxisAttrName] = r2[yAxisAttrName] * rnd * float(r2[xAxisAttrName]) / 120
        return r2

    attrValues = set(map(lambda r: r[groupByAttrName], data))
    plotData = list(map(lambda val: scatter(data, groupByAttrName, val, xAxisAttrName, yAxisAttrName, maPeriod, postProcessPoints),
                        attrValues))

    layout = dict(title=plotTitle, xaxis=dict(title=xAxisTitle), yaxis=dict(title=yAxisTitle))
    fig = dict(data=plotData, layout=layout)
    plotly.offline.iplot(fig)


def scatter_distr(data, groupByAttrName, groupByAttrValue, xAxisAttrName, roundDigits, roundFactor):
    rows = list(filter(lambda x: x[groupByAttrName] == groupByAttrValue, data))

    x = []
    y = []
    rows = sorted(rows, key=lambda r: r[xAxisAttrName])
    for k, g in groupby(rows, lambda r: round(r[xAxisAttrName] / roundFactor, roundDigits) * roundFactor):
        y.append(len(list(g)))
        x.append(k)

    return go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=groupByAttrValue
    )


def plot_distr(data, plotTitle, groupByAttrName, xAxisAttrName, xAxisTitle, roundDigits, roundFactor):
    attrValues = set(map(lambda r: r[groupByAttrName], data))
    plotData = list(
        map(lambda val: scatter_distr(data, groupByAttrName, val, xAxisAttrName, roundDigits, roundFactor),
            attrValues))

    layout = dict(title=plotTitle, xaxis=dict(title=xAxisTitle), yaxis=dict(title='Кількість прогнозів'))
    fig = dict(data=plotData, layout=layout)
    plotly.offline.iplot(fig)


plotly.offline.init_notebook_mode(connected=True)

# db = mysql.connect('wfa.cat0ol73r0ee.us-west-2.rds.amazonaws.com', 'wfa', 'PhACyCjHpMAnOatr', 'wfa')
db = mysql.connect('localhost', 'root', '', 'wfa')

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.wdp_name, 
        avg(aw.temperature - fc.temperature) as temp_diff,
        avg(aw.humidity - fc.humidity) as humidity_diff,
        avg(((((aw.wind_direction - fc.wind_direction) + 180) % 360 + 360) % 360) - 180) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and aw.name = fc.name 
            and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) <= 120
    group by aw.wdp_name, forecast_period
    order by forecast_period asc
    """)
    byWdp = []
    for row in cursor.fetchall():
        byWdp.append(dict(
            wdpName=row[0],
            avgTemperatureDiff=row[1],
            avgHumidityDiff=row[2],
            avgWindDirectionDiff=row[3],
            avgWindSpeedDiff=row[4],
            forecastPeriod=row[5]
        ))

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.wdp_name, 
        aw.temperature - fc.temperature as temp_diff,
        aw.humidity - fc.humidity as humidity_diff,
        ((((aw.wind_direction - fc.wind_direction) + 180) % 360 + 360) % 360) - 180 as wind_direction_diff,
        aw.wind_speed - fc.wind_speed as wind_speed_diff,
        round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and aw.name = fc.name 
            and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) = 24
    order by forecast_period asc;
    """)
    byWdp1DayForecastDistr = []
    for row in cursor.fetchall():
        byWdp1DayForecastDistr.append(dict(
            wdpName=row[0],
            temperatureDiff=row[1],
            humidityDiff=row[2],
            windDirectionDiff=row[3],
            windSpeedDiff=row[4],
            forecastPeriod=row[5]
        ))

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.wdp_name, 
        aw.temperature - fc.temperature as temp_diff,
        aw.humidity - fc.humidity as humidity_diff,
        ((((aw.wind_direction - fc.wind_direction) + 180) % 360 + 360) % 360) - 180 as wind_direction_diff,
        aw.wind_speed - fc.wind_speed as wind_speed_diff,
        round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and aw.name = fc.name 
            and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) = 110
    order by forecast_period asc;
    """)
    byWdp5DayForecastDistr = []
    for row in cursor.fetchall():
        byWdp5DayForecastDistr.append(dict(
            wdpName=row[0],
            temperatureDiff=row[1],
            humidityDiff=row[2],
            windDirectionDiff=row[3],
            windSpeedDiff=row[4],
            forecastPeriod=row[5]
        ))

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.name as city_name, 
        avg(aw.temperature - fc.temperature) as temp_diff,
        avg(aw.humidity - fc.humidity) as humidity_diff,
        avg(((((aw.wind_direction - fc.wind_direction) + 180) % 360 + 360) % 360) - 180) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) as forecast_period  
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and 
            aw.name = fc.name and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) <= 120
    group by aw.name, forecast_period
    order by forecast_period asc
    """)
    byCity = []
    for row in cursor.fetchall():
        byCity.append(dict(
            cityName=row[0],
            avgTemperatureDiff=row[1],
            avgHumidityDiff=row[2],
            avgWindDirectionDiff=row[3],
            avgWindSpeedDiff=row[4],
            forecastPeriod=row[5]
        ))

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.wdp_name as wdp_Name, 
        avg(aw.temperature - fc.temperature) as temp_diff,
        avg(aw.humidity - fc.humidity) as humidity_diff,
        avg(((((aw.wind_direction - fc.wind_direction) + 180) % 360 + 360) % 360) - 180) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        hour(aw.date_time) as hour_of_day,
        round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and 
            aw.name = fc.name and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) = 24
    group by aw.wdp_name, hour_of_day, forecast_period
    order by hour_of_day asc
    """)
    byDayHour1DayForecast = []
    for row in cursor.fetchall():
        byDayHour1DayForecast.append(dict(
            wdpName=row[0],
            avgTemperatureDiff=row[1],
            avgHumidityDiff=row[2],
            avgWindDirectionDiff=row[3],
            avgWindSpeedDiff=row[4],
            dayHour=row[5]
        ))

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.wdp_name as wdp_Name, 
        avg(aw.temperature - fc.temperature) as temp_diff,
        avg(aw.humidity - fc.humidity) as humidity_diff,
        avg(((((aw.wind_direction - fc.wind_direction) + 180) % 360 + 360) % 360) - 180) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        hour(aw.date_time) as hour_of_day,
        round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and 
            aw.name = fc.name and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60) = 110
    group by aw.wdp_name, hour_of_day, forecast_period
    order by hour_of_day asc
    """)
    byDayHour5DaysForecast = []
    for row in cursor.fetchall():
        byDayHour5DaysForecast.append(dict(
            wdpName=row[0],
            avgTemperatureDiff=row[1],
            avgHumidityDiff=row[2],
            avgWindDirectionDiff=row[3],
            avgWindSpeedDiff=row[4],
            dayHour=row[5]
        ))


defaultMaPeriod = 5


plot(byWdp, 'Помилка прогнозу температури за джерелу даних', 'wdpName', 'forecastPeriod', 'avgTemperatureDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу температури, K', defaultMaPeriod)
plot(byWdp, 'Помилка прогнозу відносної вологісті за джерелу даних', 'wdpName', 'forecastPeriod', 'avgHumidityDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу відносної вологості', defaultMaPeriod)
plot(byWdp, 'Помилка прогнозу напрямку вітру за джерелом даних', 'wdpName', 'forecastPeriod', 'avgWindDirectionDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу напрямку вітру, градуси', defaultMaPeriod * 2)
plot(byWdp, 'Помилка прогнозу швидкості вітру за джерелом даних', 'wdpName', 'forecastPeriod', 'avgWindSpeedDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу швидкості вітру, м/с', defaultMaPeriod)

plot(byCity, 'Помилка прогнозу температури за місцевістю прогнозу', 'cityName', 'forecastPeriod', 'avgTemperatureDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу температури, K', defaultMaPeriod)
plot(byCity, 'Помилка прогнозу відносної вологісті за місцевістю прогнозу', 'cityName', 'forecastPeriod', 'avgHumidityDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу відносної вологості', defaultMaPeriod)
plot(byCity, 'Помилка прогнозу напрямку вітру за місцевістю прогнозу', 'cityName', 'forecastPeriod', 'avgWindDirectionDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу напрямку вітру, градуси', defaultMaPeriod)
plot(byCity, 'Помилка прогнозу швидкості вітру за місцевістю прогнозу', 'cityName', 'forecastPeriod', 'avgWindSpeedDiff',
     'Період прогнозу, год', 'Середня похибка прогнозу швидкості вітру, м/с', defaultMaPeriod)


plot(byDayHour1DayForecast, 'Помилка прогнозу температура на 1 день за часом доби', 'wdpName', 'dayHour', 'avgTemperatureDiff',
     'Година доби', 'Середня похибка прогнозу температури, K', 1)
plot(byDayHour5DaysForecast, 'Помилка прогнозу температура на 5 днів за часом доби', 'wdpName', 'dayHour', 'avgTemperatureDiff',
     'Година доби', 'Середня похибка прогнозу температури, K', 1)

plot(byDayHour1DayForecast, 'Помилка прогнозу відносної вологості на 1 день за часом доби', 'wdpName', 'dayHour', 'avgHumidityDiff',
     'Година доби', 'Середня похибка прогнозу відносної вологості', 1)
plot(byDayHour5DaysForecast, 'Помилка прогнозу відносної вологості на 5 днів за часом доби', 'wdpName', 'dayHour', 'avgHumidityDiff',
     'Година доби', 'Середня похибка прогнозу відносної вологості', 1)

plot(byDayHour1DayForecast, 'Помилка прогнозу напрямку вітру на 1 день за часом доби', 'wdpName', 'dayHour', 'avgWindDirectionDiff',
     'Година доби', 'Середня похибка прогнозу напрямку вітру, градуси', 1)
plot(byDayHour5DaysForecast, 'Помилка прогнозу напрямку вітру на 5 днів за часом доби', 'wdpName', 'dayHour', 'avgWindDirectionDiff',
     'Година доби', 'Середня похибка прогнозу напрямку вітру, градуси', 1)

plot(byDayHour1DayForecast, 'Помилка прогнозу швидкості вітру на 1 день за часом доби', 'wdpName', 'dayHour', 'avgWindSpeedDiff',
     'Година доби', 'Середня похибка прогнозу швидкості вітру, м/с', 1)
plot(byDayHour5DaysForecast, 'Помилка прогнозу швидкості вітру на 5 днів за часом доби', 'wdpName', 'dayHour', 'avgWindSpeedDiff',
     'Година доби', 'Середня похибка прогнозу швидкості вітру, м/с', 1)


plot_distr(byWdp1DayForecastDistr, 'Розподіл помилки прогнозу температури на 1 день', 'wdpName', 'temperatureDiff',
           'Середня похибка прогнозу температури, K', 1, 1)
plot_distr(byWdp5DayForecastDistr, 'Розподіл помилки прогнозу температури на 5 днів', 'wdpName', 'temperatureDiff',
           'Середня похибка прогнозу температури, K', 1, 5)

plot_distr(byWdp1DayForecastDistr, 'Розподіл помилки прогнозу відносної вологості на 1 день', 'wdpName', 'humidityDiff',
           'Середня похибка прогнозу відносної вологості', 2, 1)
plot_distr(byWdp5DayForecastDistr, 'Розподіл помилки прогнозу відносної вологості на 5 днів', 'wdpName', 'humidityDiff',
           'Середня похибка прогнозу відносної вологості', 2, 3)

plot_distr(byWdp1DayForecastDistr, 'Розподіл помилки прогнозу напрямку вітру на 1 день', 'wdpName', 'windDirectionDiff',
           'Середня похибка прогнозу напрямку вітру, градуси', 0, 3)
plot_distr(byWdp5DayForecastDistr, 'Розподіл помилки прогнозу напрямку вітру на 5 днів', 'wdpName', 'windDirectionDiff',
           'Середня похибка прогнозу напрямку вітру, градуси', 0, 8)

plot_distr(byWdp1DayForecastDistr, 'Розподіл помилки прогнозу швидкості вітру на 1 день', 'wdpName', 'windSpeedDiff',
           'Середня похибка прогнозу швидкості вітру, м/с', 1, 1)
plot_distr(byWdp5DayForecastDistr, 'Розподіл помилки прогнозу швидкості вітру на 5 днів', 'wdpName', 'windSpeedDiff',
           'Середня похибка прогнозу швидкості вітру, м/с', 1, 2.5)
