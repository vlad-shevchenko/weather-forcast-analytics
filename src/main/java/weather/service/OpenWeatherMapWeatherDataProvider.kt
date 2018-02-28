package weather.service

import org.springframework.stereotype.Service
import weather.domain.ActualWeather
import weather.domain.City
import weather.domain.Forecast
import java.util.concurrent.CompletableFuture

@Service
class OpenWeatherMapWeatherDataProvider : WeatherDataProvider {

    override fun getName() = "OpenWeatherMap"

    override fun getCurrentWeather(city: MutableCollection<City>): CompletableFuture<List<ActualWeather>> {
        return CompletableFuture.completedFuture(emptyList())
    }

    override fun getForecast(city: MutableCollection<City>): CompletableFuture<List<Forecast>> {
        return CompletableFuture.completedFuture(emptyList())
    }

}


