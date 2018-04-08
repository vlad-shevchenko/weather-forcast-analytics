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


plotly.offline.init_notebook_mode(connected=True)

db = mysql.connect('url', 'user', 'password', 'db')

with db.cursor() as cursor:
    cursor.execute("""
    select 
        aw.wdp_name, 
        avg(aw.temperature - fc.temperature) as temp_diff,
        avg(aw.humidity - fc.humidity) as humidity_diff,
        avg(aw.wind_direction - fc.wind_direction) as wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) as wind_speed_diff,
        ROUND(TIMESTAMPDIFF(MINUTE, fc.forecast_creation_time, fc.target_time), -1) / 60 as forecast_period
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and aw.name = fc.name 
            and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and TIMESTAMPDIFF(MINUTE, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
        and ROUND(TIMESTAMPDIFF(MINUTE, fc.forecast_creation_time, fc.target_time), -1) < 120 * 60
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
    SELECT 
        aw.name AS city_name, 
        avg(aw.temperature - fc.temperature) AS temp_diff,
        avg(aw.humidity - fc.humidity) AS humidity_diff,
        avg(aw.wind_direction - fc.wind_direction) AS wind_direction_diff,
        avg(aw.wind_speed - fc.wind_speed) AS wind_speed_diff,
        ROUND(TIMESTAMPDIFF(MINUTE, fc.forecast_creation_time, fc.target_time), -1) / 60 AS forecast_period,  
        count(*) AS data_points_count
        FROM actual_weather AS aw
            INNER JOIN forecast AS fc
            ON aw.wdp_name = fc.wdp_name AND 
            aw.name = fc.name AND aw.latitude = fc.latitude AND aw.longitude = fc.longitude 
            AND TIMESTAMPDIFF(MINUTE, aw.date_time, fc.target_time) BETWEEN -15 AND 15
    WHERE fc.forecast_creation_time < fc.target_time
        and ROUND(TIMESTAMPDIFF(MINUTE, fc.forecast_creation_time, fc.target_time), -1) < 120 * 60
    GROUP BY aw.name, forecast_period
    ORDER BY forecast_period ASC
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
            and TIMESTAMPDIFF(MINUTE, aw.date_time, fc.target_time) between -15 and 15
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


maPeriod = 5

plot(byWdp, 'Temperature by WDP', 'wdpName', 'avgTemperatureDiff', 'forecastPeriod', maPeriod)
plot(byWdp, 'Humidity by WDP', 'wdpName', 'avgHumidityDiff', 'forecastPeriod', maPeriod)
plot(byWdp, 'Wind Direction by WDP', 'wdpName', 'avgWindDirectionDiff', 'forecastPeriod', maPeriod)
plot(byWdp, 'Wind Speed by WDP', 'wdpName', 'avgWindSpeedDiff', 'forecastPeriod', maPeriod)

plot(byCity, 'Temperature by City', 'cityName', 'avgTemperatureDiff', 'forecastPeriod', maPeriod)
plot(byCity, 'Humidity by City', 'cityName', 'avgHumidityDiff', 'forecastPeriod', maPeriod)
plot(byCity, 'Wind Direction by City', 'cityName', 'avgWindDirectionDiff', 'forecastPeriod', maPeriod)
plot(byCity, 'Wind Speed by City', 'cityName', 'avgWindSpeedDiff', 'forecastPeriod', maPeriod)

plot(byDayHour, 'Temperature by Hour of Day', 'wdpName', 'avgTemperatureDiff', 'dayHour', 1)
plot(byDayHour, 'Humidity by Hour of Day', 'wdpName', 'avgHumidityDiff', 'dayHour', 1)
plot(byDayHour, 'Wind Direction by Hour of Day', 'wdpName', 'avgWindDirectionDiff', 'dayHour', 1)
plot(byDayHour, 'Wind Speed by Hour of Day', 'wdpName', 'avgWindSpeedDiff', 'dayHour', 1)
