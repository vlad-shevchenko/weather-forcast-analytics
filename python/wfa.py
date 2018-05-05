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


def scatter(data, groupByAttrName, groupByAttrValue, xAxisAttrName, attrName, maPeriod):
    rows = list(filter(lambda x: x[groupByAttrName] == groupByAttrValue, data))
    forecastPeriods = list(map(lambda r: r[xAxisAttrName], rows))[maPeriod - 1:len(rows)]
    values = list(moving_average(list(map(lambda r: abs(r[attrName]), rows)), maPeriod))

    return go.Scatter(
        x=forecastPeriods,
        y=values,
        mode='lines+markers',
        name=groupByAttrValue
    )


def plot(data, plotTitle, groupByAttrName, valueAttrName, xAxisAttrName, maPeriod):
    attrValues = set(map(lambda r: r[groupByAttrName], data))
    plotData = list(map(lambda val: scatter(data, groupByAttrName, val, xAxisAttrName, valueAttrName, maPeriod), attrValues))

    layout = dict(title=plotTitle, xaxis=dict(title=xAxisAttrName), yaxis=dict(title=valueAttrName))
    fig = dict(data=plotData, layout=layout)
    plotly.offline.iplot(fig)


def scatter_distr(data, groupByAttrName, groupByAttrValue, xAxisAttrName, maPeriod, roundDigits, roundFactor):
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


def plot_distr(data, plotTitle, groupByAttrName, xAxisAttrName, maPeriod, roundDigits, roundFactor):
    attrValues = set(map(lambda r: r[groupByAttrName], data))
    plotData = list(
        map(lambda val: scatter_distr(data, groupByAttrName, val, xAxisAttrName, maPeriod, roundDigits, roundFactor),
            attrValues))

    layout = dict(title=plotTitle, xaxis=dict(title=xAxisAttrName), yaxis=dict(title='Number of forecasts'))
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
        avg(aw.wind_direction - fc.wind_direction) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60 as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and aw.name = fc.name 
            and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) < 120 * 60
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
        aw.name as city_name, 
        avg(aw.temperature - fc.temperature) as temp_diff,
        avg(aw.humidity - fc.humidity) as humidity_diff,
        avg(aw.wind_direction - fc.wind_direction) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) / 60 as forecast_period  
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and 
            aw.name = fc.name and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and round(timestampdiff(minute, fc.forecast_creation_time, fc.target_time), -1) < 120 * 60
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
        avg(aw.wind_direction - fc.wind_direction) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        hour(aw.date_time) as hour_of_day
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and 
            aw.name = fc.name and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and timestampdiff(minute, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
    group by aw.wdp_name, hour_of_day
    order by hour_of_day asc
    """)
    byDayHour = []
    for row in cursor.fetchall():
        byDayHour.append(dict(
            wdpName=row[0],
            avgTemperatureDiff=row[1],
            avgHumidityDiff=row[2],
            avgWindDirectionDiff=row[3],
            avgWindSpeedDiff=row[4],
            dayHour=row[5]
        ))


defaultMaPeriod = 5

plot(byWdp, 'Temperature by WDP', 'wdpName', 'avgTemperatureDiff', 'forecastPeriod', defaultMaPeriod)
plot(byWdp, 'Humidity by WDP', 'wdpName', 'avgHumidityDiff', 'forecastPeriod', defaultMaPeriod)
plot(byWdp, 'Wind Direction by WDP', 'wdpName', 'avgWindDirectionDiff', 'forecastPeriod', defaultMaPeriod)
plot(byWdp, 'Wind Speed by WDP', 'wdpName', 'avgWindSpeedDiff', 'forecastPeriod', defaultMaPeriod)

plot(byCity, 'Temperature by City', 'cityName', 'avgTemperatureDiff', 'forecastPeriod', defaultMaPeriod)
plot(byCity, 'Humidity by City', 'cityName', 'avgHumidityDiff', 'forecastPeriod', defaultMaPeriod)
plot(byCity, 'Wind Direction by City', 'cityName', 'avgWindDirectionDiff', 'forecastPeriod', defaultMaPeriod)
plot(byCity, 'Wind Speed by City', 'cityName', 'avgWindSpeedDiff', 'forecastPeriod', defaultMaPeriod)

plot(byDayHour, 'Temperature by Hour of Day', 'wdpName', 'avgTemperatureDiff', 'dayHour', 1)
plot(byDayHour, 'Humidity by Hour of Day', 'wdpName', 'avgHumidityDiff', 'dayHour', 1)
plot(byDayHour, 'Wind Direction by Hour of Day', 'wdpName', 'avgWindDirectionDiff', 'dayHour', 1)
plot(byDayHour, 'Wind Speed by Hour of Day', 'wdpName', 'avgWindSpeedDiff', 'dayHour', 1)

plot_distr(byWdp, 'Temperature distribution', 'wdpName', 'avgTemperatureDiff', 1, 2, 6)
plot_distr(byWdp, 'Humidity distribution', 'wdpName', 'avgHumidityDiff', 1, 2, 0.5)
plot_distr(byWdp, 'Wind direction distribution', 'wdpName', 'avgWindDirectionDiff', 1, 1, 8)
plot_distr(byWdp, 'Wind speed distribution', 'wdpName', 'avgWindSpeedDiff', 1, 2, 2)
