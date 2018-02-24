package weather.service;

import weather.domain.ActualWeather;
import weather.domain.Forecast;

import java.util.List;
import java.util.concurrent.CompletableFuture;

public interface WeatherDataProvider {

    CompletableFuture<ActualWeather> getCurrentWeather(String city);

    CompletableFuture<List<Forecast>> getForecast(String city);

}
