package weather.service

import org.joda.time.DateTime
import org.joda.time.DateTimeZone
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Service
import weather.domain.*
import java.util.concurrent.CompletableFuture

@Service
@ConfigurationProperties(prefix = "app.weather.open-weather-map")
class OpenWeatherMapWeatherDataProvider : WeatherDataProvider {

    lateinit var apiKey : String

    override fun getName() = "OpenWeatherMap"

    override fun getCurrentWeather(cities: Collection<City>): CompletableFuture<Collection<ActualWeather>> {
        return CompletableFuture.supplyAsync {
            cities.map { city ->
                khttp.get("http://api.openweathermap.org/data/2.5/weather", params = mapOf(
                        "lon" to city.longitude.toString(),
                        "lat" to city.latitude.toString(),
                        "apiKey" to apiKey
                )).jsonObject.let {
                    val main = it.getJSONObject("main")
                    val wind = it.getJSONObject("wind")
                    ActualWeather(
                        WeatherKey(name, city, DateTime(DateTimeZone.UTC)),
                        WeatherData(main.getDouble("temp"), main.getDouble("humidity") / 100, wind.optDouble("deg", 0.0), wind.optDouble("speed", 0.0))
                ) }
            }
        }
    }

    override fun getForecast(cities: Collection<City>): CompletableFuture<Collection<Forecast>> {
        return CompletableFuture.supplyAsync {
            cities.flatMap { city ->
                khttp.get("http://api.openweathermap.org/data/2.5/forecast", params = mapOf(
                        "lon" to city.longitude.toString(),
                        "lat" to city.latitude.toString(),
                        "apiKey" to apiKey
                )).jsonObject.getJSONArray("list").let {
                    (0 until it.length()).map { i ->
                        val item = it.getJSONObject(i)
                        val main = item.getJSONObject("main")
                        val wind = item.getJSONObject("wind")
                        Forecast(
                                ForecastKey(name, city, DateTime(item.getLong("dt") * 1000, DateTimeZone.UTC), DateTime(DateTimeZone.UTC)),
                                WeatherData(main.getDouble("temp"), main.getDouble("humidity") / 100, wind.getDouble("deg"), wind.getDouble("speed"))
                        ) }
                    }

            }
        }
    }

}


