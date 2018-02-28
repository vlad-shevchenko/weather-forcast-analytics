package weather.service;

import weather.domain.ActualWeather;
import weather.domain.Forecast;

import java.util.Collection;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public interface WeatherDataProvider {

    String getName();

    CompletableFuture<List<ActualWeather>> getCurrentWeather(Collection<String> city);

    CompletableFuture<List<Forecast>> getForecast(Collection<String> city);

}
