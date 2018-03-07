package weather.service;

import weather.domain.ActualWeather;
import weather.domain.City;
import weather.domain.Forecast;

import java.util.Collection;
import java.util.concurrent.CompletableFuture;

public interface WeatherDataProvider {

    String getName();

    CompletableFuture<? extends Collection<ActualWeather>> getCurrentWeather(Collection<City> cities);

    CompletableFuture<? extends Collection<Forecast>> getForecast(Collection<City> cities);

}
