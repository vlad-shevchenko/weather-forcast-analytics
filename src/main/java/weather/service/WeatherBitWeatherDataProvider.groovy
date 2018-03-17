package weather.service

import groovyx.net.http.HttpBuilder
import groovyx.net.http.NativeHandlers
import org.joda.time.DateTime
import org.joda.time.DateTimeZone
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Service
import weather.domain.*

import java.util.concurrent.CompletableFuture
import java.util.stream.Collectors

import static groovyx.net.http.ContentTypes.JSON

@Service
@ConfigurationProperties(prefix = "app.weather.weatherbit")
class WeatherBitWeatherDataProvider implements WeatherDataProvider {

    private Logger logger = LoggerFactory.getLogger(WeatherBitWeatherDataProvider.class)

    String apiKey

    def currentWeather = HttpBuilder.configure {
        request.uri = 'https://api.weatherbit.io/v2.0/current'
        request.contentType = JSON[0]
    }

    def forecast = HttpBuilder.configure {
        request.uri = 'https://api.weatherbit.io/v2.0/forecast/3hourly'
        request.contentType = JSON[0]
    }

    @Override
    String getName() {
        "WeatherBit"
    }

    @Override
    CompletableFuture<? extends Collection<ActualWeather>> getCurrentWeather(Collection<City> cities) {
        def dateTime = new DateTime(DateTimeZone.UTC)
        CompletableFuture.supplyAsync {
            cities.stream().map { city ->
                currentWeather.get {
                    request.uri.query = [key: getApiKey(), lat: city.latitude, lon: city.longitude]
                    response.parser(JSON[0]) { config, resp ->
                        def json = NativeHandlers.Parsers.json(config, resp)
                        def data = json.data[0]
                        new ActualWeather(
                                new WeatherKey(getName(), city, dateTime),
                                new WeatherData(data.temp + 273, data.rh / 100, data.wind_dir, data.wind_spd)
                        )
                    }
                }
            } collect(Collectors.<ActualWeather>toList())
        }
    }

    @Override
    CompletableFuture<? extends Collection<Forecast>> getForecast(Collection<City> cities) {
        def dateTime = new DateTime(DateTimeZone.UTC)
        CompletableFuture.supplyAsync {
            cities.stream().flatMap { city ->
                forecast.get {
                    request.uri.query = [key: getApiKey(), lat: city.latitude, lon: city.longitude]
                    response.parser(JSON[0]) { config, resp ->
                        def json = NativeHandlers.Parsers.json(config, resp)
                        json.data.stream().map {
                            new Forecast(
                                    new ForecastKey(getName(), city, new DateTime(it.ts.longValue() * 1000), dateTime),
                                    new WeatherData(it.temp + 273, it.rh / 100, it.wind_dir, it.wind_spd)
                            )
                        }
                    }
                }
            } collect(Collectors.toList())
        } as CompletableFuture<? extends Collection<Forecast>>
    }
}
