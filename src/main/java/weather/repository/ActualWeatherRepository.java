package weather.repository;

import org.springframework.data.repository.CrudRepository;
import weather.domain.ActualWeather;
import weather.domain.WeatherKey;

public interface ActualWeatherRepository extends CrudRepository<ActualWeather, WeatherKey> {


}
