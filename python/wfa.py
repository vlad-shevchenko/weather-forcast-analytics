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


def scatter(wdpName, attrName, maPeriod):
    rows = list(filter(lambda x: x['wdpName'] == wdpName, resultRows))
    forecastPeriods = list(map(lambda r: r['forecastPeriod'], rows))[maPeriod - 1:len(rows)]
    values = list(moving_average(list(map(lambda r: abs(r[attrName]), rows)), maPeriod))

    return go.Scatter(
        x=forecastPeriods,
        y=values,
        mode='lines+markers',
        name=wdpName
    )


def plot(attribute, maPeriod):
    plotData = [
        scatter('OpenWeatherMap', attribute, maPeriod),
        scatter('DarkSky', attribute, maPeriod),
        scatter('WeatherBit', attribute, maPeriod),
    ]

    layout = dict(title=attribute)
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
        ROUND(TIMESTAMPDIFF(MINUTE, fc.forecast_creation_time, fc.target_time), -1) as forecast_period,  
        count(*) as data_points_count
        from actual_weather as aw
            inner join forecast as fc
            on aw.wdp_name = fc.wdp_name and aw.name = fc.name 
            and aw.latitude = fc.latitude and aw.longitude = fc.longitude 
            and TIMESTAMPDIFF(MINUTE, aw.date_time, fc.target_time) between -15 and 15
    where fc.forecast_creation_time < fc.target_time
    group by aw.wdp_name, forecast_period
    order by forecast_period asc
    """)
    resultRows = []
    for row in cursor.fetchall():
        resultRows.append(dict(
            wdpName=row[0],
            avgTemperatureDiff=row[1],
            avgHumidityDiff=row[2],
            avgWindDirectionDiff=row[3],
            avgWindSpeedDiff=row[4],
            forecastPeriod=row[5]
        ))

plot('avgTemperatureDiff', 5)
plot('avgHumidityDiff', 5)
plot('avgWindDirectionDiff', 5)
plot('avgWindSpeedDiff', 5)
