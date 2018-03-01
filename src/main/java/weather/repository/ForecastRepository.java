package weather.repository;

import org.springframework.data.repository.CrudRepository;
import weather.domain.Forecast;
import weather.domain.ForecastKey;

public interface ForecastRepository extends CrudRepository<Forecast, ForecastKey> {


}
