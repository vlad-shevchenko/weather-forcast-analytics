package weather.service;

import weather.domain.ActualWeather;
import weather.domain.Forecast;

import java.util.List;

public interface WeatherDataProvider {

    ActualWeather getCurrentWeather(String city);

    List<Forecast> getForecast(String city);

}
